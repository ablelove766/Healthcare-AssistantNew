#!/usr/bin/env python3
"""
Groq LLM Integration Service
Handles communication with Groq API for fast natural language processing
"""

import os
from groq import Groq
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class GroqService:
    """Service class for integrating with Groq LLM."""
    
    def __init__(self, model_name: str = "llama3-8b-8192", api_key: Optional[str] = None):
        """
        Initialize Groq service.
        
        Args:
            model_name: Name of the Groq model to use (default: llama3-8b-8192)
            api_key: Groq API key (if not provided, will look for GROQ_API_KEY env var)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            print("⚠️  Warning: No Groq API key found. Please set GROQ_API_KEY environment variable.")
            print("   You can get a free API key from: https://console.groq.com/")
        
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.conversation_history = []
        self.system_prompt = self._get_system_prompt()
        
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the healthcare chatbot."""
        return """You are a helpful healthcare chatbot assistant. Your primary function is to help users find and filter patient information.

AVAILABLE TOOLS:
- getpatientlist: Get a list of patients filtered by patient name and limit

PATIENT DATA STRUCTURE:
Each patient record contains:
- PatientId: Unique identifier
- Name: Patient's full name
- Age: Patient's age
- Diagnosis: Medical conditions and diagnoses
- Medications: List of current medications with dosages
- Allergies: List of known allergies
- LastUpdated: When the record was last modified

CAPABILITIES:
1. Help users search for patients by name
2. Filter patient lists with specific criteria
3. Provide information about patient medical details
4. Answer questions about medications, allergies, and diagnoses
5. Provide information about available commands

IMPORTANT GUIDELINES:
- Always be professional and respectful when discussing patient information
- If a user asks for patient information, guide them to use the patient search functionality
- Keep responses concise but informative and friendly
- If you're unsure about a request, ask for clarification
- Always maintain patient privacy and confidentiality
- Only provide information through the available tools
- Be conversational and helpful, not robotic

RESPONSE FORMAT:
- For patient searches: Clearly indicate when you're searching and what parameters you're using
- For help requests: Provide clear, actionable guidance
- For general questions: Be helpful but redirect to available functionality when appropriate
- Use a friendly, professional tone suitable for healthcare settings

Remember: You can only access patient data through the getpatientlist tool. Do not make up or hallucinate patient information."""

    def add_to_conversation(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 messages to manage context length
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

    def _prepare_messages(self, user_message: str) -> List[Dict[str, str]]:
        """Prepare messages for Groq API call."""
        messages = [{'role': 'system', 'content': self.system_prompt}]
        
        # Add conversation history
        for msg in self.conversation_history[-6:]:  # Last 6 messages for context
            if msg['role'] in ['user', 'assistant']:
                messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        # Add current user message
        messages.append({'role': 'user', 'content': user_message})
        
        return messages

    async def generate_response(self, user_message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate a response using Groq LLM.
        
        Args:
            user_message: User's input message
            context: Optional context information (e.g., available tools, previous results)
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            if not self.client:
                return {
                    'response': "❌ Sorry, I'm not properly configured. Please set up the Groq API key.",
                    'intent': 'error',
                    'confidence': 0.0,
                    'requires_tool': False,
                    'setup_required': True
                }
            
            # Add context to user message if provided
            enhanced_message = user_message
            if context:
                if context.get('tool_result'):
                    enhanced_message = f"User query: {user_message}\n\nTool result: {context['tool_result']}\n\nPlease provide a helpful, friendly response based on this information. Format the patient data nicely if applicable."
                elif context.get('available_tools'):
                    enhanced_message = f"{user_message}\n\nAvailable tools: {', '.join(context['available_tools'])}"
            
            # Prepare messages
            messages = self._prepare_messages(enhanced_message)
            
            # Generate response using Groq
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=0.9,
                stream=False
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add to conversation history
            self.add_to_conversation('user', user_message)
            self.add_to_conversation('assistant', assistant_response)
            
            # Analyze intent and determine if tool is needed
            intent_analysis = await self._analyze_intent(user_message, assistant_response)
            
            return {
                'response': assistant_response,
                'intent': intent_analysis['intent'],
                'confidence': intent_analysis['confidence'],
                'requires_tool': intent_analysis['requires_tool'],
                'tool_params': intent_analysis.get('tool_params', {}),
                'raw_response': response,
                'model_used': self.model_name
            }
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(error_msg)
            
            # Check if it's an API key issue
            if "api_key" in str(e).lower() or "unauthorized" in str(e).lower():
                return {
                    'response': "❌ API authentication failed. Please check your Groq API key configuration.",
                    'intent': 'error',
                    'confidence': 0.0,
                    'requires_tool': False,
                    'setup_required': True,
                    'error': str(e)
                }
            
            return {
                'response': "❌ I'm experiencing technical difficulties. Please try again or contact support if the problem persists.",
                'intent': 'error',
                'confidence': 0.0,
                'requires_tool': False,
                'error': str(e)
            }

    async def _analyze_intent(self, user_message: str, assistant_response: str) -> Dict[str, Any]:
        """Analyze user intent to determine if tools are needed."""
        user_lower = user_message.lower()
        
        # Check for patient-related queries
        patient_keywords = ['patient', 'patients', 'find', 'search', 'list', 'show', 'get']
        name_keywords = ['named', 'called', 'name', 'with name']
        medical_keywords = ['diagnosis', 'medication', 'allergy', 'allergies', 'condition', 'treatment', 'medicine']
        
        requires_tool = False
        tool_params = {}
        intent = 'general'
        confidence = 0.5
        
        if any(keyword in user_lower for keyword in patient_keywords) or any(keyword in user_lower for keyword in medical_keywords):
            intent = 'patient_search'
            requires_tool = True
            confidence = 0.8
            
            # Extract patient name if mentioned
            if any(keyword in user_lower for keyword in name_keywords):
                # Simple name extraction
                words = user_message.split()
                for i, word in enumerate(words):
                    if word.lower() in name_keywords and i + 1 < len(words):
                        # Get the next word as potential name
                        potential_name = words[i + 1].strip('.,!?')
                        if potential_name and not potential_name.lower() in ['is', 'are', 'the', 'a', 'an']:
                            tool_params['patient_name'] = potential_name
                        break
            
            # Extract limit if mentioned
            import re
            limit_match = re.search(r'(\d+)\s*patient', user_lower)
            if limit_match:
                tool_params['limit'] = int(limit_match.group(1))
        
        elif any(keyword in user_lower for keyword in ['help', 'what', 'how', 'command']):
            intent = 'help'
            confidence = 0.9
        
        return {
            'intent': intent,
            'confidence': confidence,
            'requires_tool': requires_tool,
            'tool_params': tool_params
        }

    def clear_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []

    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation."""
        if not self.conversation_history:
            return "No conversation history."
        
        summary = f"Conversation with {len(self.conversation_history)} messages:\n"
        for msg in self.conversation_history[-3:]:  # Last 3 messages
            role = msg['role'].title()
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            summary += f"- {role}: {content}\n"
        
        return summary

    def get_available_models(self) -> List[str]:
        """Get list of available Groq models."""
        return [
            "llama3-8b-8192",      # Fast, good for most tasks
            "llama3-70b-4096",     # More capable, slower
            "mixtral-8x7b-32768",  # Good balance of speed and capability
            "gemma-7b-it"          # Alternative model
        ]

    def set_model(self, model_name: str):
        """Change the model being used."""
        if model_name in self.get_available_models():
            self.model_name = model_name
            print(f"✅ Model changed to: {model_name}")
        else:
            print(f"❌ Model {model_name} not available. Available models: {', '.join(self.get_available_models())}")

    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        return self.client is not None and self.api_key is not None
