from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

    
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a given location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

# @mcp.tool()
# async def get_forecast_from_mcp_location(location_data: str) -> str:
#     """Get weather forecast using RAW JSON from location server.

#     IMPORTANT: Pass the EXACT JSON string returned by get_current_location.
#     Do not reformat, interpret, or modify the JSON data.
    
#     Args:
#         location_data: The raw JSON string from get_current_location (e.g. '{"latitude": 41.6862, "longitude": -72.5451}')
    
#     Returns:
#         str: Detailed weather forecast
#     """
#     import json
    
#     try:
#         # Parse the JSON from location server
#         coords = json.loads(location_data)
#         latitude = coords["latitude"]
#         longitude = coords["longitude"]
        
#         # Use your existing get_forecast function
#         return await get_forecast(latitude, longitude)
        
#     except (json.JSONDecodeError, KeyError) as e:
#         return f"Error parsing location data: {str(e)}"
# @mcp.tool()
# async def get_forecast_from_coordinates(latitude: float, longitude: float) -> str:
#     """Get weather forecast from individual latitude and longitude values.
    
#     This tool accepts separate latitude and longitude parameters.
    
#     Args:
#         latitude: Latitude coordinate as a number
#         longitude: Longitude coordinate as a number
    
#     Returns:
#         str: Weather forecast for the coordinates
#     """
#     # Use your existing forecast logic
#     return await get_forecast(latitude, longitude)    
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')