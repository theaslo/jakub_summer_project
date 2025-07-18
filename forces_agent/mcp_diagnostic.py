"""
MCP Server Comprehensive Diagnostic
Enhanced version to identify the exact tool invocation issue
"""

import asyncio
import subprocess
import sys
import os

async def test_mcp_server_direct():
    """Test MCP server by running it directly"""
    print("🔍 TESTING MCP SERVER DIRECTLY")
    print("="*50)
    
    # Test 1: Check if MCP server file exists
    mcp_server_path = "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/forces_mcp/main.py"
    
    if os.path.exists(mcp_server_path):
        print(f"✅ MCP server file exists: {mcp_server_path}")
    else:
        print(f"❌ MCP server file NOT found: {mcp_server_path}")
        return
    
    # Test 2: Try to run MCP server directly
    print("\n🚀 Attempting to run MCP server directly...")
    try:
        # Change to the MCP directory
        mcp_dir = "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/forces_mcp"
        
        print(f"📁 Changing to directory: {mcp_dir}")
        os.chdir(mcp_dir)
        
        # Try to run the server
        print("🔧 Running: uv run main.py")
        result = subprocess.run(
            ["uv", "run", "main.py"], 
            capture_output=True, 
            text=True, 
            timeout=5  # 5 second timeout
        )
        
        if result.returncode == 0:
            print("✅ MCP server started successfully")
            print(f"Output: {result.stdout[:200]}...")
        else:
            print("❌ MCP server failed to start")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ MCP server started but didn't exit (normal for servers)")
    except Exception as e:
        print(f"❌ Error running MCP server: {e}")

async def check_langchain_versions():
    """Check LangChain package versions"""
    print("\n🔍 CHECKING LANGCHAIN VERSIONS")
    print("="*40)
    
    try:
        import langchain_mcp_adapters
        print(f"✅ langchain-mcp-adapters: {langchain_mcp_adapters.__version__}")
    except ImportError:
        print("❌ langchain-mcp-adapters not installed")
    except AttributeError:
        print("⚠️ langchain-mcp-adapters version not available")
    
    try:
        import langchain_core
        print(f"✅ langchain-core: {langchain_core.__version__}")
    except ImportError:
        print("❌ langchain-core not installed")
    except AttributeError:
        print("⚠️ langchain-core version not available")
    
    try:
        import langgraph
        print(f"✅ langgraph: {langgraph.__version__}")
    except ImportError:
        print("❌ langgraph not installed")
    except AttributeError:
        print("⚠️ langgraph version not available")

async def test_mcp_server_imports():
    """Test if MCP server imports work"""
    print("\n🔍 TESTING MCP SERVER IMPORTS")
    print("="*40)
    
    try:
        # Test if we can import the MCP server module
        sys.path.append("/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/forces_mcp")
        
        # Try importing main module
        import main
        print("✅ Can import MCP server main module")
        
        # Check if FastMCP is available
        from mcp.server.fastmcp import FastMCP
        print("✅ FastMCP available")
        
        # Check if tools are defined
        if hasattr(main, 'mcp'):
            print("✅ MCP server object found")
        else:
            print("❌ MCP server object not found")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Other error: {e}")

async def test_agent_mcp_connection():
    """Test the agent's MCP connection specifically"""
    print("\n🔍 TESTING AGENT MCP CONNECTION")
    print("="*40)
    
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        # Test the exact configuration the agent uses
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
        
        print("🔧 Attempting to get tools from MCP client...")
        tools = await client.get_tools()
        
        print(f"✅ Successfully connected! Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description[:50]}...")
            
        # Test calling a tool directly with enhanced error handling
        if tools:
            print("\n🧪 Testing direct tool call...")
            add_forces_tool = None
            for tool in tools:
                if "add_forces_2d" in tool.name:
                    add_forces_tool = tool
                    break
            
            if add_forces_tool:
                print("🔧 Calling add_forces_2d tool directly...")
                print(f"🔍 Tool type: {type(add_forces_tool)}")
                print(f"🔍 Tool class: {add_forces_tool.__class__.__name__}")
                
                # Check available methods
                available_methods = [method for method in dir(add_forces_tool) if not method.startswith('_')]
                print(f"🔍 Available methods: {available_methods}")
                
                # Try different invocation methods
                try:
                    print("🧪 Attempting ainvoke...")
                    result = await add_forces_tool.ainvoke({
                        "forces_data": '[{"magnitude": 10, "angle": 30}, {"magnitude": 15, "angle": 120}]'
                    })
                    print("📊 TOOL RESULT (ainvoke):")
                    print(result)
                    print("\n✅ Direct tool call with ainvoke successful!")
                    
                except Exception as e1:
                    print(f"❌ ainvoke failed: {e1}")
                    
                    try:
                        print("🧪 Attempting arun...")
                        result = await add_forces_tool.arun(
                            forces_data='[{"magnitude": 10, "angle": 30}, {"magnitude": 15, "angle": 120}]'
                        )
                        print("📊 TOOL RESULT (arun):")
                        print(result)
                        print("\n✅ Direct tool call with arun successful!")
                        
                    except Exception as e2:
                        print(f"❌ arun failed: {e2}")
                        
                        try:
                            print("🧪 Attempting acall...")
                            result = await add_forces_tool.acall({
                                "forces_data": '[{"magnitude": 10, "angle": 30}, {"magnitude": 15, "angle": 120}]'
                            })
                            print("📊 TOOL RESULT (acall):")
                            print(result)
                            print("\n✅ Direct tool call with acall successful!")
                            
                        except Exception as e3:
                            print(f"❌ All async methods failed:")
                            print(f"   ainvoke: {e1}")
                            print(f"   arun: {e2}")
                            print(f"   acall: {e3}")
            else:
                print("❌ add_forces_2d tool not found")
        
    except Exception as e:
        print(f"❌ Agent MCP connection failed: {e}")
        import traceback
        traceback.print_exc()

async def test_simple_tool_creation():
    """Test creating a simple tool to understand the issue"""
    print("\n🔍 TESTING SIMPLE TOOL CREATION")
    print("="*40)
    
    try:
        from langchain_core.tools import tool
        
        @tool
        async def simple_test_tool(input_text: str) -> str:
            """A simple test tool."""
            return f"Test tool received: {input_text}"
        
        print("✅ Simple tool created")
        print(f"🔍 Tool type: {type(simple_test_tool)}")
        print(f"🔍 Tool class: {simple_test_tool.__class__.__name__}")
        
        # Test invocation
        try:
            result = await simple_test_tool.ainvoke({"input_text": "hello"})
            print(f"✅ Simple tool ainvoke works: {result}")
        except Exception as e:
            print(f"❌ Simple tool ainvoke failed: {e}")
            
        try:
            result = await simple_test_tool.arun("hello")
            print(f"✅ Simple tool arun works: {result}")
        except Exception as e:
            print(f"❌ Simple tool arun failed: {e}")
            
    except Exception as e:
        print(f"❌ Simple tool creation failed: {e}")

async def check_file_structure():
    """Check the file structure to ensure everything is in place"""
    print("\n🔍 CHECKING FILE STRUCTURE")
    print("="*30)
    
    files_to_check = [
        "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/forces_mcp/main.py",
        "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/forces_mcp/pyproject.toml",
        "/Users/asli.tandogan_kunkel/Projects/jakub_summer_project/forces_agent/forces_agent.py"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} NOT FOUND")

async def run_full_diagnostic():
    """Run complete diagnostic"""
    print("🔍 COMPREHENSIVE MCP DIAGNOSTIC - ENHANCED")
    print("="*60)
    
    await check_file_structure()
    await check_langchain_versions()
    await test_mcp_server_imports() 
    await test_mcp_server_direct()
    await test_simple_tool_creation()
    await test_agent_mcp_connection()
    
    print("\n🎯 ENHANCED DIAGNOSTIC SUMMARY")
    print("="*40)
    print("This enhanced diagnostic tests multiple tool invocation methods.")
    print("Look for which method (ainvoke, arun, acall) works successfully.")
    print("If all methods fail, there's a deeper compatibility issue.")
    print("If any method works, use that method in your agent.")

if __name__ == "__main__":
    asyncio.run(run_full_diagnostic())
