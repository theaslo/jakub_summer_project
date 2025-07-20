"""
Forces Agent - Comprehensive Physics Force Calculation Agent
Compatible with Google A2A (Agent-to-Agent) Framework

This agent handles ALL force calculations including:
- 1D and 2D force addition and resolution
- Force components and resultants  
- Free body diagrams and equilibrium analysis
- Spring forces, friction, weight, tension
- Inclined plane analysis
- Vector operations
"""

import asyncio
from contextlib import AsyncExitStack

import json
from typing import Dict, Any, Optional
from langchain_ollama.chat_models import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools
class ForcesAgent:
    """
    Comprehensive Forces Agent compatible with Google A2A framework
    
    This agent serves as a complete force calculation specialist that can:
    - Handle any physics force problem
    - Integrate with A2A host agents
    - Provide detailed step-by-step solutions
    - Work with all force types and scenarios
    """
    
    def __init__(self, 
                 agent_id: str = "forces_agent", 
                 llm_base_url: str = "http://ds.stat.uconn.edu:11434", 
                 model: str = "qwen3:8b-q8_0"):
        
        self.agent_id = agent_id
        self.llm_base_url = llm_base_url
        self.model = model
        self.agent = None
        self.tools = None
        self.initialized = False
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        
        """Set parameters for the  agent"""
        if self.agent_id == "forces_agent":
            from prompts.force_agent_prompt import get_user_message, get_system_message, get_metadata
            self.get_system_message = get_system_message
            self.get_user_message = get_user_message
            self.mcp_port = 10100  # Default MCP port for forces agent
            self.metadata = get_metadata()
        elif self.agent_id == "kinematics_agent":
            from prompts.kinematics_agent_prompt import get_user_message, get_system_message, get_metadata
            self.get_user_message = get_user_message
            self.mcp_port = 10101  # Default MCP port for forces agent
            self.metadata = get_metadata()
        else:
            raise ValueError("Agent Prompt not available. Please check your agent initialization.")
        # Agent metadata for A2A compatibility
        self.metadata.update({
            "input_types": ["text", "json"],
            "output_types": ["text", "analysis"],
            "version": "1.0.0"
        })

    async def connect_to_streamable_http_server(self, server_url: str, headers: Optional[dict] = None):
        """Connect to an MCP server running with HTTP Streamable transport"""
        self._streams_context = streamablehttp_client(  # pylint: disable=W0201
            url=server_url,
            headers=headers or {},
        )
        read_stream, write_stream, _ = await self._streams_context.__aenter__()  # pylint: disable=E1101

        self._session_context = ClientSession(read_stream, write_stream)  # pylint: disable=W0201
        self.session: ClientSession = await self._session_context.__aenter__()  # pylint: disable=C2801

        await self.session.initialize()

    async def initialize(self):
        """Initialize the forces agent with MCP tools"""
        if self.initialized:
            return
            
        print(f"🚀 Initializing Forces Agent (ID: {self.agent_id})...")
        
        # Connect to forces MCP server
        client = MultiServerMCPClient({
            # "forces": {
            #     "command": "uv",
            #     "args": [
            #         "--directory",
            #         "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/forces_mcp",
            #         "run",
            #         "main.py"
            #     ],
            #     "transport": "stdio",
            # }
            "forces": 
            {
            "transport": "streamable_http",
            #"url": f"http://localhost:{self.mcp_port}/mcp/"
            #"url": f"http://137.99.146.29:{self.mcp_port}/mcp/",
            "url": f"http://htfd-physics.grove.ad.uconn.edu:{self.mcp_port}/mcp/",
            },
        })
        self.tools = await client.get_tools()

        # self.tools = await self.session.list_tools()
        # available_tools = [
        #     {
        #         "name": tool.name,
        #         "description": tool.description,
        #         "input_schema": tool.inputSchema,
        #     }
        #     for tool in self.tools.tools
        # ]
        
        # Initialize LLM
        llm = ChatOllama(
            model=self.model,
            temperature=0,
            base_url=self.llm_base_url,
        )
        
        # Create agent with all tools
        self.agent = create_react_agent(llm, self.tools)
        
        self.initialized = True
        print(f"✅ Forces Agent ready with {len(self.tools)} tools:")
        for tool in self.tools:
            print(f"  - {tool.name}")
        print()

    # def get_system_message(self):
    #     """Get system message for the forces agent"""
    #     return self.get_system_message()

    async def solve_force_problem(self, problem: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Main method to solve any force problem
        
        Args:
            problem: Text description of the physics problem
            context: Optional context from A2A framework or other agents
            
        Returns:
            Dict with solution, reasoning, and metadata
        """
        if not self.initialized:
            await self.initialize()
            
        try:
            # Prepare input with context if provided
            if context:
                full_input = f"Context: {json.dumps(context)}\n\nProblem: {problem}"
            else:
                full_input = problem
                
            # Solve using the agent
            response = await self.agent.ainvoke({
                "messages": [
                    SystemMessage(content=self.get_system_message()),
                    ("human", full_input)
                ]
            }, config={"recursion_limit": 15})
            
            solution = response['messages'][-1].content
            
            # Return structured response for A2A compatibility
            return {
                "success": True,
                "agent_id": self.agent_id,
                "problem": problem,
                "solution": solution,
                "reasoning": "Completed force analysis using specialized MCP tools",
                "tools_used": [tool.name for tool in self.tools],
                "metadata": self.metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "agent_id": self.agent_id,
                "problem": problem,
                "error": str(e),
                "reasoning": f"Error in force calculation: {str(e)}"
            }

    async def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities for A2A framework"""
        return {
            "agent_id": self.agent_id,
            "metadata": self.metadata,
            "available_tools": [tool.name for tool in self.tools] if self.tools else [],
            "status": "ready" if self.initialized else "not_initialized"
        }

    async def health_check(self) -> Dict[str, Any]:
        """Health check for A2A framework"""
        return {
            "agent_id": self.agent_id,
            "status": "healthy" if self.initialized else "not_ready",
            "tools_count": len(self.tools) if self.tools else 0,
            "ready": self.initialized
        }
    # async def cleanup(self):
    #     """Properly clean up the session and streams"""
    #     if self._session_context:
    #         await self._session_context.__aexit__(None, None, None)
    #     if self._streams_context:  # pylint: disable=W0125
    #         await self._streams_context.__aexit__(None, None, None) 

# Interactive chat interface
async def interactive_chat():
    """Interactive chat interface for the Forces Agent"""
    forces_agent = ForcesAgent(agent_id = "forces_agent")
    await forces_agent.initialize()
    
    forces_agent.get_user_message()
    while True:
        try:
            user_input = input("🧮 Physics Problem: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("👋 Goodbye from Forces Agent!")
                break
                
            if not user_input:
                continue
                
            print("\n🤖 Analyzing and solving...")
            result = await forces_agent.solve_force_problem(user_input)
            
            if result["success"]:
                print("📊 SOLUTION:")
                print(result["solution"])
            else:
                print(f"❌ ERROR: {result['error']}")
                
            print("\n" + "-"*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye from Forces Agent!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

# A2A Integration Example
async def a2a_integration_example():
    """Example of how this agent integrates with A2A framework"""
    forces_agent = ForcesAgent(agent_id="forces_specialist_v1")
    await forces_agent.initialize()
    
    print("\n🤖 A2A INTEGRATION EXAMPLE")
    print("="*50)
    
    # Example A2A calls
    capabilities = await forces_agent.get_capabilities()
    print("📋 Capabilities:", json.dumps(capabilities, indent=2))
    
    health = await forces_agent.health_check()
    print("\n🏥 Health Check:", json.dumps(health, indent=2))
    
    # Example problem with context
    context = {
        "requesting_agent": "physics_tutor_agent",
        "student_level": "introductory",
        "previous_problems": ["basic_vector_addition"]
    }
    
    problem = "A student pushes a 10kg box with 50N force at 30° up a frictionless ramp"
    result = await forces_agent.solve_force_problem(problem, context)
    
    print(f"\n🎯 A2A Problem Solution:")
    print(f"Success: {result['success']}")
    print(f"Solution: {result['solution'][:200]}...")  # Truncated for example

# Test function
async def test_forces_agent():
    """Test the comprehensive forces agent"""
    forces_agent = ForcesAgent()
    await forces_agent.initialize()
    
    test_problems = [
        "Add 1D forces: 15N, -8N, 20N, -5N",
        "Find resultant of 12N at 45° and 16N at 135°", 
        "Create free body diagram for 8kg block with weight, normal, and 25N applied force",
        "Calculate spring force with k=300 N/m and compression of 0.04m",
        "Analyze 6kg mass on 35° incline with friction coefficient 0.25"
    ]
    
    print("\n🧪 TESTING COMPREHENSIVE FORCES AGENT")
    print("="*60)
    
    for i, problem in enumerate(test_problems, 1):
        print(f"\n📋 Test {i}: {problem}")
        print("-" * 50)
        result = await forces_agent.solve_force_problem(problem)
        
        if result["success"]:
            print("✅ SUCCESS")
            print(f"📊 Solution: {result['solution'][:300]}...")  # Truncated
        else:
            print("❌ FAILED")
            print(f"Error: {result['error']}")
        print()

if __name__ == "__main__":
    # Default: Run interactive chat
    asyncio.run(interactive_chat())
    
    # Uncomment to run A2A integration example
    # asyncio.run(a2a_integration_example())
    
    # Uncomment to run tests
    # asyncio.run(test_forces_agent())
