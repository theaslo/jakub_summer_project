import asyncio
from langchain_ollama.chat_models import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

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
    print(f"tools --------- {tools}")
    
    llm = ChatOllama(
        model="qwen3:8b", #"llama3.2",
        temperature=0,
        # Removed format="json" as it might cause issues
        #tools=tools
    )
    
    # Add system instructions
    # system_message = """You are a helpful assistant with access to location and weather MCP servers.

    # CRITICAL WORKFLOW for weather at current location:
    # 1. Call get_current_location → this returns JSON like '{"latitude": 41.6862, "longitude": -72.5451}'
    # 2. Call get_forecast_from_mcp_location with parameter 'location_data' set to that EXACT JSON string

    # PARAMETER FORMAT EXAMPLE:
    # get_forecast_from_mcp_location(location_data='{"latitude": 41.6862, "longitude": -72.5451}')

    # NOT: separate latitude/longitude parameters
    # YES: single location_data parameter with JSON string

    # Do not ask for additional location information."""

    system_message = """You are a helpful assistant that coordinates between independent services.

    CRITICAL RULES - NEVER BREAK THESE:
    1. NEVER ask users for location information when get_current_location exists
    2. ALWAYS use get_current_location first for any location query
    3. ALWAYS extract latitude/longitude numbers from get_current_location result
    4. ALWAYS use those numbers with get_forecast(latitude, longitude)
    5. NEVER ask for city, zip code, or manual location input
    6. After providing weather forecast, STOP. Do not ask for additional information.

    ABSOLUTE PROHIBITION: 
    - DO NOT ask for alternative locations
    - DO NOT offer to help with different cities
    - DO NOT suggest manual location input
    - PROVIDE WEATHER AND STOP IMMEDIATELY

    IF YOU PROVIDE ANY WEATHER DATA, YOUR JOB IS COMPLETE. STOP THERE AND DO NOT SAY ANYTHING ELSE."""

    agent = create_react_agent(llm, tools)

    #agent = create_react_agent("anthropic:claude-3-7-sonnet-latest", tools)
    
    print("=== Testing Simple Tool Usage ===")
    try:
        simple_tool_test = await agent.ainvoke({
            "messages": [
                SystemMessage(content=system_message),
                ("human", "Use the get_current_location tool now")
            ]
        }, config={"recursion_limit": 4})
        
        print("Simple tool test result:")
        #print(alltogether["messages"][-1].content)
        print(simple_tool_test["messages"][-1].content)
        print("--------------------------------------------------------------------------------")
        
    except Exception as e:
        print(f"Simple tool test failed: {e}")
        print("--------------------------------------------------------------------------------")

    print("=== Debug Location Server Output ===")
    try:
        location_debug = await agent.ainvoke({
            "messages": "Call get_current_location and show me exactly what it returns"
        }, config={"recursion_limit": 8})
        
        print("Location debug result:")
        print(location_debug["messages"][-1].content)
        print("--------------------------------------------------------------------------------")
        
    except Exception as e:
        print(f"Location debug failed: {e}")
        print("--------------------------------------------------------------------------------")
    # Other tests
    try:
        weather_response = await agent.ainvoke({"messages": "What's the weather in Glastonbury Connecticut?"})
        print("--------------------------------------------------------------------------------")
        print(weather_response["messages"][-1].content)
        print("--------------------------------------------------------------------------------")
    except Exception as e:
        print(f"Weather test failed: {e}")
        print("--------------------------------------------------------------------------------")

    try:
        location_response = await agent.ainvoke({"messages": "whats my current location?"})
        print(location_response["messages"][-1].content)
        print("--------------------------------------------------------------------------------")
    except Exception as e:
        print(f"Location test failed: {e}")
        print("--------------------------------------------------------------------------------")

    # try:
    #     alltogether = await agent.ainvoke({
    #         "messages": [
    #             SystemMessage(content="Use get_current_location first, then get_forecast_from_mcp_location with that data. Do not ask for additional location information."),
    #             ("human", "What's the forecast for my current location?")
    #         ]
    #     }, config={"recursion_limit": 8})
    try:
        alltogether = await agent.ainvoke({
            "messages": [
                SystemMessage(content="""
                Step 1: Call get_current_location  
                Step 2: Extract latitude and longitude numbers from the result
                Step 3: Call get_forecast(latitude=number, longitude=number) with those numbers
                Do not ask for additional location information.
                """),
                ("human", "What's the forecast for my current location?")
            ]
        }, config={"recursion_limit": 8})
        
        print(alltogether["messages"][-1].content)
        print("--------------------------------------------------------------------------------")
    except Exception as e:
        print(f"Combined test failed: {e}")
        print("--------------------------------------------------------------------------------")

if __name__ == "__main__":
    asyncio.run(main())
