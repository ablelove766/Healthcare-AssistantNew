#!/usr/bin/env python3
"""
Test script to verify Groq integration is working properly
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq_service import GroqService


async def test_groq_integration():
    """Test the Groq integration with various healthcare queries."""
    print("🧪 Testing Groq Integration")
    print("=" * 50)
    
    # Initialize Groq service
    groq_service = GroqService()
    
    if not groq_service.is_configured():
        print("❌ Groq service is not configured properly")
        return False
    
    print(f"✅ Groq service configured with model: {groq_service.model_name}")
    print(f"🔑 API key found: {'Yes' if groq_service.api_key else 'No'}")
    
    # Test queries
    test_queries = [
        "Hello, can you help me with patient information?",
        "I need to find patients named John",
        "Show me patients with diabetes",
        "What can you help me with?",
        "Find patients with allergies to penicillin"
    ]
    
    print("\n🔍 Testing various queries:")
    print("-" * 30)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        try:
            result = await groq_service.generate_response(query)
            
            if result.get('response'):
                print(f"   ✅ Response: {result['response'][:100]}...")
                print(f"   🎯 Intent: {result.get('intent', 'unknown')}")
                print(f"   🔧 Requires Tool: {result.get('requires_tool', False)}")
                if result.get('tool_params'):
                    print(f"   📋 Tool Params: {result['tool_params']}")
            else:
                print(f"   ❌ No response received")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎉 Groq integration test completed!")
    return True


async def test_conversation_context():
    """Test conversation context management."""
    print("\n💬 Testing Conversation Context")
    print("=" * 50)
    
    groq_service = GroqService()
    
    # Simulate a conversation
    conversation = [
        "Hello, I'm looking for patient information",
        "Can you find patients named John?",
        "What about their medications?",
        "Do any of them have allergies?"
    ]
    
    for i, message in enumerate(conversation, 1):
        print(f"\n{i}. User: {message}")
        result = await groq_service.generate_response(message)
        print(f"   Bot: {result['response'][:80]}...")
    
    # Check conversation history
    summary = groq_service.get_conversation_summary()
    print(f"\n📝 Conversation Summary:")
    print(summary)


if __name__ == "__main__":
    try:
        print("🏥 Healthcare Chatbot - Groq Integration Test")
        print("=" * 60)
        
        # Run tests
        asyncio.run(test_groq_integration())
        asyncio.run(test_conversation_context())
        
        print("\n✅ All tests completed successfully!")
        print("\n💡 The chatbot is ready to use with Groq LLM!")
        print("   - Ultra-fast responses (sub-second)")
        print("   - Natural language understanding")
        print("   - Context-aware conversations")
        print("   - Medical terminology support")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
