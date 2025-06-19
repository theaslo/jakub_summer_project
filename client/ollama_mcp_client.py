#!/usr/bin/env python3
import asyncio
import json
import requests
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import logging

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='error.log',
    filemode='a'
)

class OllamaMCPClient:
    def __init__(self, ollama_model="llama3.2", ollama_host="http://localhost:11434"):
        self.ollama_model = ollama_model
        self.ollama_host = ollama_host
        self.mcp_session = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str, cwd: str):
        """Connect to MCP-compatible Python/Node script"""
        command = "uv" if server_script_path.endswith(".py") else "node"
        args = ["run", server_script_path] if command == "uv" else [server_script_path]

        server_params = StdioServerParameters(
            command=command,
            args=args,
            cwd=cwd
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.mcp_session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.mcp_session.initialize()

        tools = await self.mcp_session.list_tools()
        print("✅ Connected to MCP. Available tools:")
        for tool in tools.tools:
            print(f"  • {tool.name}: {tool.description}")

    async def call_ollama(self, prompt, system_prompt=None):
        def _make_request():
            url = f"{self.ollama_host}/api/generate"
            data = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False
            }
            if system_prompt:
                data["system"] = system_prompt

            print("📡 Calling Ollama...")
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                logging.error(f"Ollama error: Status code {response.status_code}, Response: {response.text}")
                return f"[Ollama Error] Status code {response.status_code}"

        return await asyncio.to_thread(_make_request)

    async def call_mcp_tool(self, tool_name, args):
        if not self.mcp_session:
            return "[MCP Error] MCP session not started"
        try:
            result = await self.mcp_session.call_tool(tool_name, args)
            print(result)
            return result.content
        except Exception as e:
            logging.error(f"Error calling MCP tool {tool_name} with args {args}: {e}", exc_info=True)
            return f"[MCP Exception] {e}"

    async def process_weather_request(self, user_query):
        print(f"📥 User query: {user_query}")

        system_prompt = """You are a helpful weather assistant. You have access to weather tools:
1. get_forecast(latitude, longitude)
2. get_alerts(state)
3. get_current_location()

Return responses like:
TOOL: get_forecast
ARGS: {"latitude": 41.76, "longitude": -72.68}
or
TOOL: get_alerts
ARGS: {"state": "CT"}
"""

        llm_response = await self.call_ollama(user_query, system_prompt)
        print(f"🧠 LLM suggested:\n{llm_response}")

        tool_name, args = None, {}
        for line in llm_response.splitlines():
            if line.startswith("TOOL:"):
                tool_name = line.split("TOOL:")[1].strip()
                print(tool_name)
            elif line.startswith("ARGS:"):
                # try:
                args = json.loads(line.split("ARGS:")[1].strip())
                # except json.JSONDecodeError:
                #     return "[Parse Error] Could not decode ARGS."

        # if not tool_name or not args:
        #     return "[Error] Could not parse tool or arguments."
        if not tool_name:
            return "[Error] Could not parse tool or arguments."

        print(f"🔧 Calling MCP tool: {tool_name} with args {args}")
        mcp_result = await self.call_mcp_tool(tool_name, args)
        print(f"📦 MCP returned:\n{mcp_result}")

        final_prompt = f"""User asked: {user_query}

Tool result: {mcp_result}

Respond naturally to the user based on the result."""
        final_response = await self.call_ollama(final_prompt)
        return final_response

    async def chat_loop(self):
        print("🤖 Assistant ready. Type 'quit' to exit.\n")
        #await self.connect_to_server("weather.py", cwd="/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/weather")
        await self.connect_to_server("main.py", cwd="/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/location_mcp")

        while True:
            user_input = input("🌤️ Ask about the weather: ").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                print("👋 Exiting. Stay dry!")
                break
            if not user_input:
                continue
            try:
                response = await self.process_weather_request(user_input)
                print(f"\n🗣️ Assistant: {response}\n")
            except Exception as e:
                logging.error(f"Error during chat loop processing for input '{user_input}': {e}", exc_info=True)
                print(f"[Error] {e}")


async def main():
    client = OllamaMCPClient()
    await client.chat_loop()


if __name__ == "__main__":
    asyncio.run(main())
