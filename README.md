# Simple MCP Server

A basic Model Context Protocol (MCP) server implementation that provides tools and resources for AI assistants.

## Features

### Tools
- **list_tools**: List all available tools in this MCP server
- **getpatientlist**: Get a list of patients filtered by patient name

## Architecture

The MCP server is organized into separate modules:

- **`mcp_server.py`** - Main MCP server with tool definitions
- **`api_client.py`** - API client for making HTTP requests to patient management system
- **`config.py`** - Configuration for API endpoints, authentication, and field mappings

### Resources
- **Server Information**: Basic information about the server and its capabilities

### Prompts
- **greeting**: A friendly greeting prompt with optional name parameter

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your API endpoint:
   - Open `config.py`
   - Update `API_CONFIG["base_url"]` with your actual API endpoint URL
   - Configure authentication if required
   - Adjust field mappings if your API uses different field names

## Usage

### Running the Server

The server uses stdio transport for communication:

```bash
python mcp_server.py
```

### Configuration for Claude Desktop

Add this configuration to your Claude Desktop config file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "simple-mcp-server": {
      "command": "python",
      "args": ["path/to/your/mcp_server.py"],
      "env": {}
    }
  }
}
```

Replace `path/to/your/mcp_server.py` with the actual path to your mcp_server.py file.

### Testing Tools

Once connected, you can test the tools:

**1. List Tools:**
- Input: `{}` (no parameters)
- Output: List of all available tools with descriptions and usage examples

**2. Get Patient List Tool** (calls your API endpoint):
- Input: `{}` (no filters - returns all patients)
- Input: `{"patient_name": "John"}` (filter by patient name)
- Input: `{"patient_name": "Smith", "limit": 5}` (filter by name with limit)
- Output: Formatted list of patients with their details from your API

## API Configuration

The `getpatientlist` tool calls your actual API endpoint. Configure it in `config.py`:

### Basic Configuration
```python
API_CONFIG = {
    "base_url": "http://localhost:5001",  # Your API base URL
    "endpoints": {
        "patients": "/patients",  # Your patients endpoint
    },
    "timeout": 30,
    "defaults": {
        "limit": 10,
    }
}
```

### Authentication
The server supports multiple authentication methods:

**Bearer Token:**
```python
"auth": {
    "type": "bearer",
    "token": "your-bearer-token-here",
}
```

**API Key:**
```python
"auth": {
    "type": "api_key",
    "token": "your-api-key-here",
    "header_name": "X-API-Key",  # or whatever header your API uses
}
```

### Field Mapping
If your API uses different field names, update the `FIELD_MAPPING` in `config.py`:

```python
FIELD_MAPPING = {
    "id": ["id", "patient_id", "patientId"],  # Maps to your API's ID field
    "name": ["name", "patient_name", "fullName"],  # Maps to your API's name field
    # ... add more mappings as needed
}
```

### Supported API Response Formats
The server can handle various API response formats:
- Direct array: `[{patient1}, {patient2}]`
- Wrapped in data: `{"data": [{patient1}, {patient2}]}`
- Wrapped in patients: `{"patients": [{patient1}, {patient2}]}`

## API Client

The `api_client.py` module provides a clean interface for API interactions:

### PatientAPIClient Class
- **`get_patient_list(patient_name, limit)`** - Main method for fetching patient data
- **`_get_headers()`** - Handles authentication headers
- **`_get_field_value()`** - Maps API field names to standard names
- **`_format_patient_list()`** - Formats patient data for display

### Usage
```python
from api_client import patient_api_client

# Get all patients
result = await patient_api_client.get_patient_list(limit=10)

# Filter by patient name
result = await patient_api_client.get_patient_list(patient_name="John", limit=5)
```

## Development

### Adding New Tools

To add a new tool:

1. Add the tool definition in `handle_list_tools()`
2. Add the tool implementation in `handle_call_tool()`

### Adding New Resources

To add a new resource:

1. Add the resource definition in `handle_list_resources()`
2. Add the resource implementation in `handle_read_resource()`

### Adding New Prompts

To add a new prompt:

1. Add the prompt definition in `handle_list_prompts()`
2. Add the prompt implementation in `handle_get_prompt()`

## Security Notes

- The calculator tool uses `eval()` for simplicity. In production, use a proper math parser.
- Always validate and sanitize inputs in production environments.
- Consider implementing proper error handling and logging.

## License

This is a simple example implementation. Modify as needed for your use case.
