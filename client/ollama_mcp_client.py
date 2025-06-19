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


# class Server:
#     """Manages MCP server connections and tool execution."""

#     def __init__(self, name: str, config: dict[str, Any]) -> None:
#         self.name: str = name
#         self.config: dict[str, Any] = config
#         self.stdio_context: Any | None = None
#         self.session: ClientSession | None = None
#         self._cleanup_lock: asyncio.Lock = asyncio.Lock()
#         self.exit_stack: AsyncExitStack = AsyncExitStack()

#     async def initialize(self) -> None:
#         """Initialize the server connection."""
#         command = (
#             shutil.which("npx")
#             if self.config["command"] == "npx"
#             else self.config["command"]
#         )
#         if command is None:
#             raise ValueError("The command must be a valid string and cannot be None.")

#         server_params = StdioServerParameters(
#             command=command,
#             args=self.config["args"],
#             env={**os.environ, **self.config["env"]}
#             if self.config.get("env")
#             else None,
#         )
#         try:
#             stdio_transport = await self.exit_stack.enter_async_context(
#                 stdio_client(server_params)
#             )
#             read, write = stdio_transport
#             session = await self.exit_stack.enter_async_context(
#                 ClientSession(read, write)
#             )
#             await session.initialize()
#             self.session = session
#         except Exception as e:
#             logging.error(f"Error initializing server {self.name}: {e}")
#             await self.cleanup()
#             raise

#     async def list_tools(self) -> list[Any]:
#         """List available tools from the server.

#         Returns:
#             A list of available tools.

#         Raises:
#             RuntimeError: If the server is not initialized.
#         """
#         if not self.session:
#             raise RuntimeError(f"Server {self.name} not initialized")

#         tools_response = await self.session.list_tools()
#         tools = []

#         for item in tools_response:
#             if isinstance(item, tuple) and item[0] == "tools":
#                 tools.extend(
#                     Tool(tool.name, tool.description, tool.inputSchema)
#                     for tool in item[1]
#                 )

#         return tools

#     async def execute_tool(
#         self,
#         tool_name: str,
#         arguments: dict[str, Any],
#         retries: int = 2,
#         delay: float = 1.0,
#     ) -> Any:
#         """Execute a tool with retry mechanism.

#         Args:
#             tool_name: Name of the tool to execute.
#             arguments: Tool arguments.
#             retries: Number of retry attempts.
#             delay: Delay between retries in seconds.

#         Returns:
#             Tool execution result.

#         Raises:
#             RuntimeError: If server is not initialized.
#             Exception: If tool execution fails after all retries.
#         """
#         if not self.session:
#             raise RuntimeError(f"Server {self.name} not initialized")

#         attempt = 0
#         while attempt < retries:
#             try:
#                 logging.info(f"Executing {tool_name}...")
#                 result = await self.session.call_tool(tool_name, arguments)

#                 return result

#             except Exception as e:
#                 attempt += 1
#                 logging.warning(
#                     f"Error executing tool: {e}. Attempt {attempt} of {retries}."
#                 )
#                 if attempt < retries:
#                     logging.info(f"Retrying in {delay} seconds...")
#                     await asyncio.sleep(delay)
#                 else:
#                     logging.error("Max retries reached. Failing.")
#                     raise

#     async def cleanup(self) -> None:
#         """Clean up server resources."""
#         async with self._cleanup_lock:
#             try:
#                 await self.exit_stack.aclose()
#                 self.session = None
#                 self.stdio_context = None
#             except Exception as e:
#                 logging.error(f"Error during cleanup of server {self.name}: {e}")


# class Tool:
#     """Represents a tool with its properties and formatting."""

#     def __init__(
#         self, name: str, description: str, input_schema: dict[str, Any]
#     ) -> None:
#         self.name: str = name
#         self.description: str = description
#         self.input_schema: dict[str, Any] = input_schema

#     def format_for_llm(self) -> str:
#         """Format tool information for LLM.

#         Returns:
#             A formatted string describing the tool.
#         """
#         args_desc = []
#         if "properties" in self.input_schema:
#             for param_name, param_info in self.input_schema["properties"].items():
#                 arg_desc = (
#                     f"- {param_name}: {param_info.get('description', 'No description')}"
#                 )
#                 if param_name in self.input_schema.get("required", []):
#                     arg_desc += " (required)"
#                 args_desc.append(arg_desc)

#         return f"""
# Tool: {self.name}
# Description: {self.description}
# Arguments:
# {chr(10).join(args_desc)}
# """


class OllamaMCPClient:
    def __init__(self, ollama_model="llama3.2", ollama_host="http://localhost:11434"):
        self.ollama_model = ollama_model
        self.ollama_host = ollama_host
        self.mcp_session = None
        self.exit_stack = AsyncExitStack()


    async def connect_to_server_from_dict(self, config:dict):
        pass
        
        # for k,v in config:
        #     print(f"{k} ====== {v}")
        #await self.mcp_session.initialize()


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
        print("🤖 Weather Assistant ready. Type 'quit' to exit.\n")
        my_servers = {
            "mcpServers": {
                "weather": {
                    "command": "uvx",
                    "args": [
                        "--directory",
                        "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/weather",
                        "run",
                        "weather.py"
                    ]
                    },
                "current_location": {
                    "command": "uvx",
                    "args": [
                        "--directory",
                        "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/location_mcp",
                        "run",
                        "main.py"
                    ]
                    }
                }
            }

        #await self.connect_to_server_from_dict(my_servers)
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
