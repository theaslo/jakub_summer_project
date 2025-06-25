from typing import Any, List
import httpx
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("location")

# @mcp.tool()
# async def get_current_location() -> List[str]:
#     """Current location. Returns the users current location.

#     Args:
#         None
#     Return:
#         List[Longitude, Lattitude]    
#     """
#     coordinates=  ["41.6862", "72.5451"]
#     return "\n---\n".join(coordinates)


@mcp.tool()
async def get_current_location() -> str:
    """Get current location coordinates.

    Args:
        None
    Returns:
        str: Location data for weather forecast
    """
    # Return in the exact format your weather tool expects
    return json.dumps({
        "latitude": 41.6862,
        "longitude": -72.5451
    })


def main():
    print("Hello from location-mcp!")

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
# if __name__ == "__main__":
#     main()
