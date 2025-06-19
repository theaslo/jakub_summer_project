# Setup
## Installation
Make sure uv is installed. See [this link](https://docs.astral.sh/uv/getting-started/installation/) for installation instructions.

## Running Ollama
### Installation
Ensure Ollama is installed on your machine. See [this link](https://ollama.com) for installation instructions.

### Running
Once installed run

`ollama serve`

You'll also need to pull a model. For this project we recommend:
```bash
ollama pull llama3.2
```

## Using Client
### Environment setup
If first time running set up the virtual environment. Go to the [client](client) directory and run 
`uv venv` . 
Then, `uv pip install .`

### Running
Go to the [client](client) directory and run 
`source .venv/bin/activate`
and then
`uv run ollama_mcp_client.py`

This will start the interactive weather assistant. You can ask questions like:
- "What's the weather in Connecticut?"
- "Are there any weather alerts for CT?"
- "What's the forecast for my current location?"

Type 'quit' to exit the application.

# MCP servers
## Using MCP Server Inspector to debug MCP servers

The MCP Server Inspector is a helpful tool for debugging and testing MCP servers. To use it:

1. **Install the MCP Inspector** (if not already installed):
   ```bash
   npx @modelcontextprotocol/inspector@latest
   ```

2. **Test the Weather Server**:
   ```bash
   # Navigate to the weather server directory
   cd weather
   
   # Run the inspector with the weather server
   npx @modelcontextprotocol/inspector@latest uv run weather.py
   ```

3. **Test the Location Server**:
   ```bash
   # Navigate to the location server directory
   cd location_mcp
   
   # Run the inspector with the location server
   npx @modelcontextprotocol/inspector@latest uv run main.py
   ```

The inspector will open a web interface where you can:
- View available tools and their schemas
- Test tool execution with different parameters
- Debug server responses and errors
- Verify server initialization

## Weather Server

The weather server provides weather forecasting and alert services using the National Weather Service API.

### Available Tools

#### `get_forecast(latitude: float, longitude: float) -> str`
Returns a detailed weather forecast for the specified coordinates.

**Parameters:**
- `latitude` (float, required): Latitude of the location
- `longitude` (float, required): Longitude of the location

**Example usage:**
```json
{
  "latitude": 41.6862,
  "longitude": -72.5451
}
```

**Returns:** A formatted string containing the next 5 forecast periods with temperature, wind, and detailed forecast information.

#### `get_alerts(state: str) -> str`
Retrieves active weather alerts for any US state.

**Parameters:**
- `state` (string, required): Two-letter US state code (e.g., "CT", "NY", "CA")

**Example usage:**
```json
{
  "state": "CT"
}
```

**Returns:** A formatted string containing active weather alerts including event type, affected areas, severity, description, and instructions.

### Running the Weather Server Standalone

To run the weather server independently for testing:

```bash
cd weather
uv run weather.py
```

The server will start and listen for MCP requests via stdio. You can test it using the MCP Inspector or integrate it with other MCP clients.

### Configuration

The weather server uses the following configuration:
- **API Base URL**: `https://api.weather.gov`
- **User Agent**: `weather-app/1.0`
- **Timeout**: 30 seconds for HTTP requests
- **Transport**: stdio (standard input/output)

## Location Server

The location server provides the user's current location coordinates. Currently, it returns hardcoded coordinates for Connecticut.

### Available Tools

#### `get_current_location() -> List[str]`
Returns the user's current location coordinates.

**Parameters:** None

**Returns:** A list containing longitude and latitude as strings: `["41.6862", "72.5451"]`

### Running the Location Server Standalone

To run the location server independently:

```bash
cd location_mcp
uv run main.py
```

### Customizing Location

To change the default location, edit the `get_current_location` function in `location_mcp/main.py`:

```python
@mcp.tool()
async def get_current_location() -> List[str]:
    """Current location. Returns the users current location."""
    # Update these coordinates to your desired location
    coordinates = ["YOUR_LATITUDE", "YOUR_LONGITUDE"]
    return "\n---\n".join(coordinates)
```

# Troubleshooting

## Common Issues

### Ollama Connection Issues
If you get connection errors to Ollama:
1. Verify Ollama is running: `ollama serve`
2. Check if the model is available: `ollama list`
3. Pull the required model: `ollama pull llama3.2`
4. Verify the Ollama host URL in the client (default: `http://localhost:11434`)

### MCP Server Connection Issues
If MCP servers fail to start:
1. Ensure you're in the correct directory when running servers
2. Check that all dependencies are installed: `uv sync`
3. Verify the server paths in `ollama_mcp_client.py` match your file system
4. Use the MCP Inspector to test servers individually

### Virtual Environment Issues
If you encounter Python environment issues:
1. Recreate the virtual environment: `rm -rf .venv && uv venv`
2. Reinstall dependencies: `uv pip install .`
3. Activate the environment: `source .venv/bin/activate`

### Weather API Issues
If weather data is unavailable:
1. Check your internet connection
2. Verify coordinates are within the US (NWS API limitation)
3. Try different coordinates if one location fails
4. Check the error logs in `client/error.log`

## Logs and Debugging

Error logs are written to `client/error.log`. To monitor logs in real-time:

```bash
cd client
tail -f error.log
```

For more verbose logging, modify the logging level in `ollama_mcp_client.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from ERROR to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='error.log',
    filemode='a'
)
```

# Development

## Project Structure
```
jakub_summer_project/
├── client/                     # Ollama client application
│   ├── ollama_mcp_client.py   # Main client implementation
│   ├── main.py                # Client entry point
│   ├── pyproject.toml         # Client dependencies
│   └── error.log              # Error logs
├── weather/                   # Weather MCP server
│   ├── weather.py             # Weather server implementation
│   ├── main.py                # Entry point
│   └── pyproject.toml         # Weather server dependencies
├── location_mcp/              # Location MCP server
│   ├── main.py                # Location server implementation
│   └── pyproject.toml         # Location server dependencies
├── HOW_TO.md                  # This file
├── README.md                  # Project documentation
├── main.py                    # Project root entry point
└── pyproject.toml             # Root project configuration
```

## Adding New Tools

### Adding Weather Tools
To add new weather-related functionality, extend the weather server:

```python
@mcp.tool()
async def your_new_weather_tool(param: str) -> str:
    """Description of your new weather tool.
    
    Args:
        param: Description of the parameter
    """
    # Implementation here
    return result
```

### Adding Location Features
To enhance location services, modify the location server:

```python
@mcp.tool()
async def get_location_by_city(city: str, state: str) -> List[str]:
    """Get coordinates for a specific city.
    
    Args:
        city: City name
        state: State code
    """
    # Implementation to geocode city/state to coordinates
    return coordinates
```

### Updating the Client
After adding new tools, update the client's system prompt in `ollama_mcp_client.py` to include the new tools:

```python
system_prompt = """You are a helpful weather assistant. You have access to weather tools:
1. get_forecast(latitude, longitude)
2. get_alerts(state)
3. get_current_location()
4. your_new_tool(parameters)  # Add your new tool here

Return responses like:
TOOL: your_new_tool
ARGS: {"param": "value"}
"""
```

## Testing

### Unit Testing
To add tests for your MCP tools, create test files in each server directory:

```python
# weather/test_weather.py
import pytest
from weather import get_forecast, get_alerts

@pytest.mark.asyncio
async def test_get_forecast():
    result = await get_forecast(41.6862, -72.5451)
    assert "Temperature:" in result
    assert "Wind:" in result
```

### Integration Testing
Test the full client flow by running the client and verifying responses to sample queries.

## Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test your changes with the MCP Inspector
5. Update documentation if needed
6. Submit a pull request

## Next Steps
- Add support for international weather services
- Implement real GPS location detection
- Add more weather data types (radar, satellite imagery)
- Create a web interface for the weather assistant
- Add support for weather history and trends
