# Jakub Summer Project

A weather assistant application built with MCP (Model Context Protocol) servers and Ollama integration. This project demonstrates how to create modular AI-powered tools using MCP servers for weather forecasting and location services, integrated with a local LLM via Ollama.

## Overview

This project consists of three main components:

1. **Weather MCP Server** - Provides weather forecasts and alerts using the National Weather Service API
2. **Location MCP Server** - Returns the user's current location (currently hardcoded to Connecticut coordinates)  
3. **Client Application** - An Ollama-powered chat interface that connects to the MCP servers to provide weather information

## Project Structure

```
jakub_summer_project/
├── weather/                    # Weather MCP server
│   ├── weather.py             # Main weather server implementation
│   ├── main.py                # Entry point
│   └── pyproject.toml         # Weather server dependencies
├── location_mcp/              # Location MCP server
│   ├── main.py                # Location server implementation
│   └── pyproject.toml         # Location server dependencies
├── client/                    # Ollama client application
│   ├── ollama_mcp_client.py   # Main client implementation
│   ├── main.py                # Client entry point
│   └── pyproject.toml         # Client dependencies
├── main.py                    # Project root entry point
└── pyproject.toml             # Root project configuration
```

## Features

### Weather Server (`weather/`)
- **Weather Forecasts**: Get detailed weather forecasts for any location using latitude/longitude coordinates
- **Weather Alerts**: Retrieve active weather alerts for any US state
- **NWS Integration**: Uses the National Weather Service API for accurate, government-sourced weather data

### Location Server (`location_mcp/`)
- **Current Location**: Provides user's current location coordinates
- **Hardcoded Coordinates**: Currently returns Connecticut coordinates (41.6862, -72.5451)

### Client Application (`client/`)
- **Natural Language Interface**: Chat with an AI assistant about weather
- **Ollama Integration**: Uses local Ollama LLM for natural language processing
- **MCP Tool Orchestration**: Automatically calls appropriate weather/location tools based on user queries
- **Conversational Flow**: Processes user questions, calls tools, and provides natural language responses

## Requirements

- Python 3.11+
- [Ollama](https://ollama.ai) installed and running locally
- `uv` package manager (for running MCP servers)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/theaslo/jakub_summer_project.git
   cd jakub_summer_project
   ```

2. **Install dependencies for each component**:
   ```bash
   # Weather server
   cd weather && uv sync && cd ..
   
   # Location server  
   cd location_mcp && uv sync && cd ..
   
   # Client
   cd client && uv sync && cd ..
   ```

3. **Install and start Ollama**:
   ```bash
   # Install Ollama (follow instructions at https://ollama.ai)
   # Pull a compatible model
   ollama pull llama3.2
   ```

## Usage

### Running the Weather Assistant

1. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

2. **Run the client application**:
   ```bash
   cd client
   uv run ollama_mcp_client.py
   ```

3. **Chat with the weather assistant**:
   ```
   🌤️ Ask about the weather: What's the forecast for Connecticut?
   🌤️ Ask about the weather: Are there any weather alerts for CT?
   🌤️ Ask about the weather: quit
   ```

### Running Individual MCP Servers

You can test the MCP servers individually:

```bash
# Weather server
cd weather
uv run weather.py

# Location server
cd location_mcp  
uv run main.py
```

## API Reference

### Weather Server Tools

#### `get_forecast(latitude: float, longitude: float) -> str`
Returns a detailed weather forecast for the specified coordinates.

**Example**:
```python
get_forecast(41.6862, -72.5451)
```

#### `get_alerts(state: str) -> str`  
Returns active weather alerts for a US state (two-letter state code).

**Example**:
```python
get_alerts("CT")
```

### Location Server Tools

#### `get_current_location() -> List[float]`
Returns the user's current location as [longitude, latitude].

**Returns**: `[41.6862, 72.5451]` (Connecticut coordinates)

## Configuration

### Ollama Configuration
The client is configured to use:
- **Model**: `llama3.2` (configurable in `OllamaMCPClient.__init__`)
- **Host**: `http://localhost:11434` (default Ollama endpoint)

### MCP Server Paths
Update the server paths in `ollama_mcp_client.py` if you move the project:

```python
my_servers = {
    "mcpServers": {
        "weather": {
            "command": "uvx",
            "args": ["--directory", "/path/to/weather", "run", "weather.py"]
        },
        "current_location": {
            "command": "uvx", 
            "args": ["--directory", "/path/to/location_mcp", "run", "main.py"]
        }
    }
}
```

## Dependencies

### Core Dependencies
- **mcp**: Model Context Protocol implementation
- **httpx**: HTTP client for API requests
- **requests**: HTTP library for Ollama communication

### Weather Server
- `mcp>=1.0.0` - MCP server framework
- `requests>=2.31.0` - HTTP requests
- `httpx>=0.24.0` - Async HTTP client

### Location Server  
- `httpx>=0.28.1` - HTTP client
- `mcp[cli]>=1.9.3` - MCP with CLI tools

### Client
- `httpx>=0.28.1` - HTTP client
- `mcp[cli]>=1.9.3` - MCP client libraries
- `requests>=2.32.4` - Ollama communication

## Development

### Adding New Weather Features
Extend the weather server by adding new tools in `weather/weather.py`:

```python
@mcp.tool()
async def your_new_tool(param: str) -> str:
    """Tool description."""
    # Implementation
    return result
```

### Customizing Location
Update the hardcoded coordinates in `location_mcp/main.py`:

```python
@mcp.tool()
async def get_current_location() -> List[float]:
    return [your_longitude, your_latitude]
```

### Using Different LLM Models
Change the Ollama model in the client:

```python
client = OllamaMCPClient(ollama_model="your-preferred-model")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is available under the MIT License.

## Acknowledgments

- Built with [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol)
- Weather data provided by the [National Weather Service API](https://www.weather.gov/documentation/services-web-api)
- Powered by [Ollama](https://ollama.ai) for local LLM inference