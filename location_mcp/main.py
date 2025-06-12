from typing import Any, List
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("location")

@mcp.tool()
async def get_current_location(x:int) -> List[float]:
    """Current location. Returns the users current location.

    Args:
        x: A useless arg. Placeholder, if not supplied make it 0
    Return:
        List[Longitude, Lattitude]    
    """
    coordinates = [41.6862, 72.5451]
    return "\n---\n".join(coordinates)

def main():
    print("Hello from location-mcp!")

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
# if __name__ == "__main__":
#     main()
