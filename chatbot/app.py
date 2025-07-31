#!/usr/bin/env python3
"""
Healthcare Chatbot Flask Application
Integrates with MCP server to provide healthcare-related chat functionality.
"""

import os
import sys
import asyncio
import json
from flask import Flask, render_template, request, jsonify, make_response
from flask_socketio import SocketIO, emit
from groq_service import GroqService
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path to import MCP server modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from mcp_server import mcp
    from api_client import patient_api_client
    MCP_AVAILABLE = True
    print("✅ MCP server modules imported successfully")
except ImportError as e:
    print(f"❌ Error importing MCP server modules: {e}")
    print("Make sure you're running from the correct directory and MCP server files exist in parent directory")
    MCP_AVAILABLE = False
    # Create dummy objects for testing
    class DummyMCP:
        pass
    mcp = DummyMCP()
    patient_api_client = DummyMCP()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.after_request
def add_security_headers(response):
    """Add security headers for Teams integration."""
    # Allow embedding in Teams iframe
    response.headers['X-Frame-Options'] = 'ALLOW-FROM https://teams.microsoft.com'
    response.headers['Content-Security-Policy'] = (
        "frame-ancestors 'self' https://teams.microsoft.com https://*.teams.microsoft.com "
        "https://*.skype.com https://*.microsoft.com; "
        "default-src 'self' https:; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.socket.io "
        "https://res.cdn.office.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https:; "
        "connect-src 'self' ws: wss: https:;"
    )
    # Add CORS headers for Teams
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

class ChatbotMCPIntegration:
    """Integration layer between chatbot, Groq LLM, and MCP server."""

    def __init__(self):
        self.groq_service = GroqService(model_name="llama3-8b-8192")
        self.available_tools = {
            'getpatientlist': self.get_patient_list
        }
    

    
    async def get_patient_list(self, patient_name=None, limit=10):
        """Get patient list using MCP server."""
        if not MCP_AVAILABLE:
            return "❌ MCP server is not available. Please check the setup."

        try:
            # Import the getpatientlist function from mcp_server
            from mcp_server import getpatientlist
            result = await getpatientlist(patient_name=patient_name, limit=limit)
            return result
        except Exception as e:
            return f"Error getting patient list: {str(e)}"

    async def process_message(self, message):
        """Process user message using Ollama LLM and execute tools if needed."""
        try:
            # First, get LLM response and intent analysis
            llm_result = await self.groq_service.generate_response(
                message,
                context={'available_tools': list(self.available_tools.keys())}
            )

            # Check if setup is required
            if llm_result.get('setup_required'):
                return llm_result['response'] + "\n\n💡 To set up Groq API:\n1. Get free API key from https://console.groq.com/\n2. Set environment variable: GROQ_API_KEY=your_key_here\n3. Restart the chatbot"

            # If LLM determines a tool is needed, execute it
            if llm_result.get('requires_tool') and llm_result.get('intent') == 'patient_search':
                tool_params = llm_result.get('tool_params', {})

                # Execute patient search tool
                tool_result = await self.get_patient_list(
                    patient_name=tool_params.get('patient_name'),
                    limit=tool_params.get('limit', 10)
                )

                # Generate final response with tool result
                final_result = await self.groq_service.generate_response(
                    message,
                    context={'tool_result': tool_result}
                )

                return final_result['response']

            # Return LLM response directly
            return llm_result['response']

        except Exception as e:
            error_msg = f"An error occurred while processing your request: {str(e)}"
            print(f"Error in process_message: {e}")
            return error_msg

    def clear_conversation(self):
        """Clear conversation history."""
        self.groq_service.clear_conversation()

    def get_conversation_summary(self):
        """Get conversation summary."""
        return self.groq_service.get_conversation_summary()

    def is_llm_configured(self):
        """Check if LLM service is properly configured."""
        return self.groq_service.is_configured()



# Initialize MCP integration
mcp_integration = ChatbotMCPIntegration()

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/teams')
def teams_index():
    """Render Teams-optimized chat interface."""
    return render_template('teams.html')

@app.route('/teams/config')
def teams_config():
    """Teams app configuration page."""
    return render_template('teams_config.html')

@app.route('/privacy')
def privacy():
    """Privacy policy page for Teams app."""
    return """
    <html>
    <head><title>Privacy Policy - Healthcare Assistant</title></head>
    <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
        <h1>Privacy Policy</h1>
        <p>This Healthcare Assistant application processes healthcare-related queries to provide information assistance.</p>
        <h2>Data Collection</h2>
        <p>We collect minimal data necessary for the service:</p>
        <ul>
            <li>Chat messages for processing and response generation</li>
            <li>Basic usage analytics</li>
        </ul>
        <h2>Data Usage</h2>
        <p>Your data is used solely to provide healthcare assistance and is not shared with third parties.</p>
        <h2>Data Retention</h2>
        <p>Chat sessions are temporary and not permanently stored.</p>
        <p>Last updated: January 2024</p>
    </body>
    </html>
    """

@app.route('/terms')
def terms():
    """Terms of use page for Teams app."""
    return """
    <html>
    <head><title>Terms of Use - Healthcare Assistant</title></head>
    <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
        <h1>Terms of Use</h1>
        <p>By using this Healthcare Assistant application, you agree to the following terms:</p>
        <h2>Service Description</h2>
        <p>This application provides AI-powered assistance for healthcare-related information queries.</p>
        <h2>Limitations</h2>
        <ul>
            <li>This service is for informational purposes only</li>
            <li>Not a substitute for professional medical advice</li>
            <li>Always consult healthcare professionals for medical decisions</li>
        </ul>
        <h2>Acceptable Use</h2>
        <p>Users must use this service responsibly and in compliance with applicable laws and regulations.</p>
        <p>Last updated: January 2024</p>
    </body>
    </html>
    """

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """REST API endpoint for chat messages."""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Process message asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(mcp_integration.process_message(message))
        loop.close()
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/clear-chat', methods=['POST'])
def clear_chat():
    """Clear conversation history."""
    try:
        mcp_integration.clear_conversation()
        return jsonify({
            'message': 'Conversation history cleared',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': f'Error clearing chat: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status including LLM configuration."""
    try:
        return jsonify({
            'mcp_available': MCP_AVAILABLE,
            'llm_configured': mcp_integration.is_llm_configured(),
            'llm_service': 'Groq',
            'model': mcp_integration.groq_service.model_name,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': f'Error getting status: {str(e)}',
            'status': 'error'
        }), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('status', {'message': 'Connected to Healthcare Chatbot'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle incoming chat messages via WebSocket."""
    try:
        message = data.get('message', '').strip()
        
        if not message:
            emit('chat_response', {'error': 'Message cannot be empty'})
            return
        
        # Process message asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(mcp_integration.process_message(message))
        loop.close()
        
        emit('chat_response', {
            'response': response,
            'original_message': message,
            'status': 'success'
        })
    
    except Exception as e:
        emit('chat_response', {
            'error': f'Server error: {str(e)}',
            'status': 'error'
        })

if __name__ == '__main__':
    print("🏥 Starting Healthcare Chatbot with Groq LLM...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📂 Parent directory: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
    print(f"🔧 MCP Available: {MCP_AVAILABLE}")
    print(f"🤖 Groq LLM Configured: {mcp_integration.is_llm_configured()}")
    if not mcp_integration.is_llm_configured():
        print("⚠️  Warning: Groq API key not found. Set GROQ_API_KEY environment variable.")
        print("   Get free API key from: https://console.groq.com/")
    print(f"🧠 Model: {mcp_integration.groq_service.model_name}")
    print("🌐 Available at: http://localhost:5000")
    print("🚀 Starting server...")

    try:
        # socketio.run(app, debug=True, host='0.0.0.0', port=5000)
        # Only runs when you run locally: `python app.py`
      port = int(os.environ.get("PORT", 5000))
      socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
      print("🚀 Starting server...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()


