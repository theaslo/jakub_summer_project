#!/usr/bin/env python3
"""
Simple test script for the Math MCP Server
Run this to verify the server functions are working correctly.
"""

import asyncio
import sys
import os

# Add the current directory to the path so we can import the server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from math_mcp_server import (
        solve_quadratic_equation,
        solve_linear_equation, 
        trigonometry_calculator,
        triangle_solver,
        unit_circle_reference,
        logarithm_calculator,
        statistics_calculator
    )
    print("✓ Successfully imported all functions from math_mcp_server")
except ImportError as e:
    print(f"✗ Failed to import functions: {e}")
    sys.exit(1)

async def test_functions():
    """Test each function with simple examples."""
    
    print("\n" + "="*50)
    print("TESTING MATH MCP SERVER FUNCTIONS")
    print("="*50)
    
    # Test 1: Quadratic Equation
    print("\n1. Testing Quadratic Equation Solver:")
    print("-" * 40)
    try:
        result = await solve_quadratic_equation("x² + 5x + 6 = 0")
        print("✓ Quadratic solver working")
        print("Sample output:", result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"✗ Quadratic solver failed: {e}")
    
    # Test 2: Linear Equation
    print("\n2. Testing Linear Equation Solver:")
    print("-" * 40)
    try:
        result = await solve_linear_equation("3x + 5 = 14")
        print("✓ Linear solver working")
        print("Sample output:", result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"✗ Linear solver failed: {e}")
    
    # Test 3: Trigonometry
    print("\n3. Testing Trigonometry Calculator:")
    print("-" * 40)
    try:
        result = await trigonometry_calculator("sin", 30, "degrees")
        print("✓ Trigonometry calculator working")
        print("Sample output:", result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"✗ Trigonometry calculator failed: {e}")
    
    # Test 4: Triangle Solver
    print("\n4. Testing Triangle Solver:")
    print("-" * 40)
    try:
        result = await triangle_solver('{"sides": {"a": 3, "b": 4, "c": 5}}')
        print("✓ Triangle solver working")
        print("Sample output:", result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"✗ Triangle solver failed: {e}")
    
    # Test 5: Unit Circle
    print("\n5. Testing Unit Circle Reference:")
    print("-" * 40)
    try:
        result = await unit_circle_reference(45, "degrees")
        print("✓ Unit circle reference working")
        print("Sample output:", result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"✗ Unit circle reference failed: {e}")
    
    # Test 6: Logarithms
    print("\n6. Testing Logarithm Calculator:")
    print("-" * 40)
    try:
        result = await logarithm_calculator("log", 10, 100)
        print("✓ Logarithm calculator working")
        print("Sample output:", result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"✗ Logarithm calculator failed: {e}")
    
    # Test 7: Statistics
    print("\n7. Testing Statistics Calculator:")
    print("-" * 40)
    try:
        result = await statistics_calculator("descriptive", "1.2, 1.5, 1.3, 1.4, 1.6")
        print("✓ Statistics calculator working")
        print("Sample output:", result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"✗ Statistics calculator failed: {e}")
    
    print("\n" + "="*50)
    print("TESTING COMPLETE")
    print("="*50)
    print("\nIf all tests show ✓, your Math MCP Server is ready to use!")
    print("To run the server: python math_mcp_server.py")

if __name__ == "__main__":
    # Run the async test function
    asyncio.run(test_functions())
