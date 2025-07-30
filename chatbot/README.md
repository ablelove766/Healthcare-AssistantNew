# Healthcare Chatbot

A modern web-based chatbot interface that integrates with the MCP (Model Context Protocol) server to provide healthcare-related functionality through a responsive Bootstrap UI.

## Features

- 🏥 **Healthcare Focus**: Integrates with existing MCP server for patient management
- 🤖 **AI-Powered**: Uses Groq LLM for ultra-fast natural language understanding and responses
- 💬 **Real-time Chat**: WebSocket-based communication with fallback to AJAX
- 📱 **Responsive Design**: Bootstrap-powered UI that works on all devices
- 🚀 **Easy Integration**: Seamlessly connects to your existing MCP server
- 🎨 **Modern UI**: Clean, professional interface with smooth animations
- 🧠 **Context Aware**: Maintains conversation history for better responses

## Available Commands

The chatbot uses **Groq LLM** for ultra-fast natural language understanding and supports:

- **Patient Management**:
  - "get patient list" or "show patients"
  - "find patients named John"
  - "show patients with diabetes"
  - "get patient medication information"
  - "find patients with allergies to penicillin"
  - "show patient diagnosis details"

- **Natural Language Queries**:
  - "help" or "what can you do?"
  - "how do I search for patients?"
  - "tell me about the available features"

## Project Structure

```
chatbot/
├── app.py                 # Flask application with MCP integration
├── groq_service.py        # Groq LLM integration service
├── setup_groq.py          # Groq setup and testing script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main chat interface
└── static/
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── chat.js       # Frontend JavaScript
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- **Groq API key** (free at https://console.groq.com/)
- The parent MCP server project should be working
- All MCP server dependencies installed in the parent directory

### Step 1: Install Dependencies

Navigate to the chatbot directory and install requirements:

```bash
cd chatbot
pip install -r requirements.txt
```

### Step 2: Set up Groq

Set up Groq API for ultra-fast LLM inference:

```bash
# Run the setup script
python setup_groq.py
```

This script will:
- Guide you through getting a free Groq API key
- Test the API connection
- Show available models
- Help configure environment variables

### Step 3: Verify MCP Server

Ensure your MCP server is working by testing it from the parent directory:

```bash
cd ..
python test_mcp_calls.py
```

### Step 4: Run the Chatbot

Start the Flask application:

```bash
cd chatbot
python app.py
```

The chatbot will be available at: `http://localhost:5000`

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the chatbot directory for custom configuration:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=5000
```

### MCP Server Integration

The chatbot automatically imports and uses:
- `mcp_server.py` - Main MCP server functions
- `api_client.py` - Patient API client
- `config.py` - Configuration settings

## Usage

1. **Start the Application**: Run `python app.py`
2. **Open Browser**: Navigate to `http://localhost:5000`
3. **Start Chatting**: 
   - Use the sidebar quick actions
   - Type natural language queries
   - Try commands like "help", "list tools", or "get patient list"

## API Endpoints

### REST API
- `GET /` - Main chat interface
- `POST /api/chat` - Send chat message (JSON)

### WebSocket Events
- `connect` - Client connection
- `disconnect` - Client disconnection  
- `chat_message` - Send message to bot
- `chat_response` - Receive bot response

## Customization

### Adding New Commands

1. **Backend**: Add new methods to `ChatbotMCPIntegration` class in `app.py`
2. **Parser**: Update `parse_user_message()` method to recognize new patterns
3. **Frontend**: Add quick action buttons in `templates/index.html`

### Styling

- **CSS**: Modify `static/css/style.css` for visual changes
- **Bootstrap**: The UI uses Bootstrap 5.3.0 classes
- **Icons**: Bootstrap Icons are included for UI elements

### MCP Integration

The chatbot integrates with MCP server through:
- Direct function imports from parent directory
- Async function calls using asyncio
- Error handling and response formatting

## 📊 API Response Format

The system now supports comprehensive patient data with the following structure:

### Recommended Format
```json
{
  "PatientId": "P001",
  "Name": "John Doe",
  "Age": 45,
  "Diagnosis": "Hypertension, Type 2 Diabetes",
  "Medications": ["Metformin 500mg", "Lisinopril 10mg", "Atorvastatin 20mg"],
  "Allergies": ["Penicillin", "Shellfish"],
  "LastUpdated": "2024-01-15T10:30:00Z"
}
```

### Supported Fields
- **PatientId**: Unique patient identifier
- **Name**: Patient's full name
- **Age**: Patient's age
- **Diagnosis**: Medical conditions and diagnoses
- **Medications**: Array or string of current medications
- **Allergies**: Array or string of known allergies
- **LastUpdated**: When the record was last modified

### Alternative Formats
The system also supports legacy formats and different field naming conventions. See `config.py` for complete field mapping details.

### Testing
Run the test script to see format handling in action:
```bash
python test_patient_api_format.py
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure parent directory is in Python path
2. **MCP Server Not Found**: Verify MCP server files exist in parent directory
3. **Port Conflicts**: Change port in `app.py` if 5000 is in use
4. **WebSocket Issues**: The app falls back to AJAX if WebSocket fails

### Debug Mode

Run with debug enabled:
```bash
FLASK_DEBUG=True python app.py
```

### Testing MCP Integration

Test MCP functions directly:
```python
import asyncio
from app import mcp_integration

async def test():
    result = await mcp_integration.process_message("help")
    print(result)

asyncio.run(test())
```

## 🚀 Why Groq?

**Groq provides ultra-fast LLM inference with several advantages:**

- ⚡ **Lightning Fast**: Sub-second response times (vs minutes with local models)
- 🆓 **Free Tier**: Generous free usage limits for development
- 🧠 **Multiple Models**: Choose from llama3-8b, llama3-70b, mixtral, and more
- 🔒 **Secure**: Enterprise-grade API security
- 🌐 **Cloud-based**: No local GPU or storage requirements
- 📈 **Scalable**: Handles multiple concurrent requests efficiently

**Performance Comparison:**
- Local Ollama3: 30-60 seconds per response
- Groq API: 0.5-2 seconds per response
- Better user experience with real-time chat feel

## Production Deployment

For production deployment:

1. **Use Gunicorn**:
   ```bash
   gunicorn --worker-class eventlet -w 1 app:app
   ```

2. **Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   ```

3. **Reverse Proxy**: Configure nginx or Apache as reverse proxy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the MCP Server healthcare system.
