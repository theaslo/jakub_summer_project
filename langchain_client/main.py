import asyncio
from langchain_ollama.chat_models import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

async def interactive_chat(agent, system_message):
    """Interactive chat loop for user queries"""
    print("\n" + "="*60)
    print("🤖 Multi-MCP Weather Assistant ready!")
    print("Available commands:")
    print("- Ask about weather: 'What's the weather in [city]?'")
    print("- Ask about current location: 'What's my current location?'")
    print("- Ask for forecast: 'What's the forecast for my current location?'")
    print("Type 'quit' to exit.")
    print("="*60 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
                
            print("🤖 Thinking...")
            
            # Call agent with user input and system instructions
            response = await agent.ainvoke({
                "messages": [
                    SystemMessage(content=system_message),
                    ("human", user_input)
                ]
            }, config={"recursion_limit": 8})
            
            print(f"\nAssistant: {response['messages'][-1].content}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

async def main():

    client = MultiServerMCPClient(
        {
            "weather": {
                "command": "uv",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": [
                    "--directory",
                    "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/weather",
                    "run",
                    "weather.py"
                ],
                "transport": "stdio",
            },
            "location": {
                "command": "uv",
                "args": [
                    "--directory",
                    "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/location_mcp",
                    "run",
                    "main.py"
                ],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    print(f"🔧 Connected to {len(tools)} MCP tools")
    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    print()  # Empty line

    print(f"🔧 Connected to {len(tools)} MCP tools")
    llm = ChatOllama(
        model="qwen3:8b", #"llama3.2",
        temperature=0,
        # Removed format="json" as it might cause issues
        #tools=tools
    )
    
    # system_message = """You are a helpful assistant that coordinates between independent services.

    # CRITICAL RULES - NEVER BREAK THESE:
    # 1. NEVER ask users for location information when get_current_location exists
    # 2. ALWAYS use get_current_location first for any location query
    # 3. ALWAYS extract latitude/longitude numbers from get_current_location result
    # 4. ALWAYS use those numbers with get_forecast(latitude, longitude)
    # 5. NEVER ask for city, zip code, or manual location input
    # 6. After providing weather forecast, STOP. Do not ask for additional information.

    # ABSOLUTE PROHIBITION: 
    # - DO NOT ask for alternative locations
    # - DO NOT offer to help with different cities
    # - DO NOT suggest manual location input
    # - PROVIDE WEATHER AND STOP IMMEDIATELY

    # IF YOU PROVIDE ANY WEATHER DATA, YOUR JOB IS COMPLETE. STOP THERE AND DO NOT SAY ANYTHING ELSE."""
    
    # USE this below, if new one fails!!!!
    # system_message = """You are a helpful assistant that coordinates between independent services.

    # SMART LOCATION HANDLING:
    # 1. IF user asks about a SPECIFIC city/location (like "weather in Boston" or "forecast for Miami"):
    # - Use the weather tools directly with that location
    # - DO NOT call get_current_location
    
    # 2. IF user asks about "my location", "current location", "here", or "where I am":
    # - Call get_current_location first
    # - Extract latitude/longitude numbers from result
    # - Use those numbers with get_forecast(latitude, longitude)
    
    # 3. NEVER ask for additional location information

    # EXAMPLES:
    # - "Weather in Boston" → Use weather tools with Boston directly
    # - "What's my current location weather?" → Use get_current_location → get_forecast
    # - "Forecast for Miami" → Use weather tools with Miami directly
    # - "Weather here" → Use get_current_location → get_forecast

    system_message = """You are a helpful assistant that coordinates between independent services.

    LOCATION HANDLING:
    1. For "my location" or "current location": Use get_current_location then get_forecast

    2. For SPECIFIC CITIES: Use your built-in knowledge of world geography to determine the latitude and longitude coordinates, then call get_forecast(latitude, longitude)

    WORKFLOW EXAMPLES:
    - User: "Weather in Boston" → You: Look up Boston coordinates from your knowledge → Call get_forecast(lat, lng)
    - User: "Weather in Paris" → You: Look up Paris coordinates from your knowledge → Call get_forecast(lat, lng)  
    - User: "My location weather" → You: Call get_current_location → Extract coordinates → Call get_forecast

    Use your existing geographical knowledge to find coordinates for any city worldwide.
    NEVER ask for additional location information."""

    # After providing weather data, STOP. Do not ask for alternatives or additional info."""
    agent = create_react_agent(llm, tools)

    # Skip all tests and go directly to interactive mode
    print("🚀 Starting Multi-MCP Weather Assistant...")
    await interactive_chat(agent, system_message)

if __name__ == "__main__":
    asyncio.run(main())
