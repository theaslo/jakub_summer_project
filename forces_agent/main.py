"""
Forces Agent - Main Entry Point
Comprehensive Physics Force Calculation Agent compatible with Google A2A
"""

import asyncio
from forces_agent import ForcesAgent

async def main():
    """Main entry point for Forces Agent"""
    print("🚀 Starting Comprehensive Forces Agent...")
    print("🤝 Google A2A Framework Compatible")
    print("🔬 Physics Force Calculation Specialist")
    
    # Create and run the forces agent
    forces_agent = ForcesAgent(agent_id="forces_agent_main")
    
    # Initialize the agent
    await forces_agent.initialize()
    
    # Start interactive mode
    from forces_agent import interactive_chat
    await interactive_chat()

if __name__ == "__main__":
    asyncio.run(main())
