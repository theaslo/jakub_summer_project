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
import json
from typing import Dict, Any, Optional
from langchain_ollama.chat_models import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

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
        
        # Agent metadata for A2A compatibility
        self.metadata = {
            "id": agent_id,
            "name": "Forces Agent",
            "description": "Comprehensive physics force calculation specialist",
            "capabilities": [
                "1D_force_addition",
                "2D_force_addition", 
                "force_components",
                "resultant_calculations",
                "free_body_diagrams",
                "equilibrium_analysis",
                "spring_forces",
                "friction_forces",
                "weight_calculations",
                "tension_analysis",
                "inclined_planes",
                "vector_operations"
            ],
            "input_types": ["text", "json"],
            "output_types": ["text", "analysis"],
            "version": "1.0.0"
        }
        
    async def initialize(self):
        """Initialize the forces agent with MCP tools"""
        if self.initialized:
            return
            
        print(f"🚀 Initializing Forces Agent (ID: {self.agent_id})...")
        
        # Connect to forces MCP server
        client = MultiServerMCPClient({
            "forces": {
                "command": "uv",
                "args": [
                    "--directory",
                    "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/forces_mcp",
                    "run",
                    "main.py"
                ],
                "transport": "stdio",
            }
        })
        
        self.tools = await client.get_tools()
        
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

    def get_system_message(self):
        """Get comprehensive system message for the forces agent"""
        return """You are a COMPREHENSIVE FORCES AGENT - the ultimate specialist in physics force calculations. You MUST ALWAYS first consider using a MCP tool. Use the actual MCP tools and return their real results.

🎯 YOUR COMPLETE EXPERTISE:

📐 VECTOR OPERATIONS:
- 1D force addition: Forces along a single axis
- 2D force addition: Multiple forces with magnitude and angle
- Force component resolution: Breaking forces into x/y components  
- Resultant calculations: Combining components into magnitude/direction
- Vector operations: Addition, subtraction, dot product, cross product

⚖️ EQUILIBRIUM & ANALYSIS:
- Free body diagrams: Complete force identification and visualization
- Equilibrium checking: Determining if forces are balanced
- Balancing forces: Calculating forces needed for equilibrium
- Static equilibrium: Systems at rest or constant velocity

🔧 APPLIED FORCES:
- Spring forces: Hooke's Law (F = -kx)
- Friction forces: Static and kinetic friction (f = μN) 
- Weight forces: Gravitational force (W = mg)
- Tension forces: Ropes, cables, pulleys, Atwood machines
- Normal forces: Perpendicular contact forces
- Inclined planes: Complete force analysis on slopes

🔧 AVAILABLE MCP TOOLS:
- add_forces_1d: 1D force addition
- add_forces_2d: 2D force addition with magnitude/angle
- resolve_force_components: Break force into x/y components
- find_resultant_force: Get magnitude/angle from components
- create_free_body_diagram: Generate FBD with analysis
- check_equilibrium: Determine balance + suggest balancing force
- calculate_spring_force_tool: Hooke's Law calculations
- calculate_friction_force_tool: Static/kinetic friction
- calculate_weight_force: Gravitational force calculations
- analyze_forces_on_incline: Complete inclined plane analysis
- analyze_tension_forces: Rope/pulley systems
- force_vector_operations: Advanced vector mathematics

📋 CRITICAL REQUIREMENTS:
1. ALWAYS ACTUALLY CALL the MCP tools - you will see "Processing request of type CallToolRequest" when this works correctly
2. Use DOUBLE QUOTES in JSON parameters: "[{\"magnitude\": 10, \"angle\": 30}]"
3. All angles in DEGREES (never radians): 0°=right, 90°=up, 180°=left, 270°=down
4. WAIT for the tool result and present the complete output to the user
5. Never just show the JSON call format - actually execute the tool and show results
6. Include units in all calculations (N, kg, m/s², etc.)

💡 PROBLEM-SOLVING WORKFLOW:
1. ANALYZE: Identify what type of force problem this is
2. GATHER: Extract all given values and parameters
3. TOOL SELECTION: Choose the appropriate MCP tool
4. EXECUTE: Actually call the MCP tool and wait for complete results
5. PRESENT: Show the complete calculation results from the tool
6. INTERPRET: Explain what the results mean physically

🚫 NEVER DO THESE:
- Don't just show the JSON format without calling the tool
- Don't make up calculations manually
- Don't give generic responses about physics laws
- Don't skip calling the actual MCP tools
- Don't cut off tool results or give incomplete answers

✅ ALWAYS DO THESE:
- Actually call the appropriate MCP tool for every problem
- Wait for and present the tool's complete result
- Explain the physical meaning of the calculation results
- Use the exact tool output rather than summarizing

EXAMPLE WORKFLOWS:

For "Add forces: 10N at 30°, 15N at 120°":
1. Recognize this is 2D force addition
2. Call add_forces_2d with proper JSON format
3. Present the complete calculation results from the tool
4. Explain what the resultant force means

For "Calculate spring force with k=200 N/m, compressed by 0.05m":
1. Recognize this is a spring force problem  
2. Call calculate_spring_force_tool with k=200, displacement=-0.05
3. Present the complete Hooke's Law calculation from the tool
4. Explain the physical meaning (restoring force direction, etc.)

REMEMBER: You are the COMPLETE FORCES SPECIALIST. Use the actual tools and present their real, complete results!"""

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

# Interactive chat interface
async def interactive_chat():
    """Interactive chat interface for the Forces Agent"""
    forces_agent = ForcesAgent()
    await forces_agent.initialize()
    
    print("\n" + "="*70)
    print("🤖 COMPREHENSIVE FORCES AGENT")
    print("🔬 Physics Force Calculation Specialist")
    print("🤝 Compatible with Google A2A Framework")
    print("="*70)
    print("\n🎯 CAPABILITIES:")
    print("📐 Vector Operations: 1D/2D forces, components, resultants, vector math")
    print("⚖️ Equilibrium Analysis: Free body diagrams, force balance, static equilibrium")
    print("🔧 Applied Forces: Springs, friction, weight, tension, inclined planes")
    print("\n💡 EXAMPLE PROBLEMS:")
    print("• 'Add forces: 10N at 30°, 15N at 120°, 8N at 270°'")
    print("• 'Create free body diagram for 5kg box on 30° incline with friction'")
    print("• 'Calculate spring force: k=200 N/m, compressed by 0.05m'")
    print("• 'Analyze tension in Atwood machine with 3kg and 7kg masses'")
    print("• 'Find equilibrium: Check if forces 12N right, 8N left, 15N up, 15N down balance'")
    print("• 'Break down 25N force at 135° into components'")
    print("\nType 'quit' to exit")
    print("="*70 + "\n")
    
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
