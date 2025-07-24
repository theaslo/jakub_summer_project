# Math MCP Server

A comprehensive Model Context Protocol (MCP) server for mathematical calculations needed in algebra-based physics courses. This server provides tools for algebra, trigonometry, equation solving, and statistical analysis.

## Features

### 🔢 Algebra Tools
- **Linear Equation Solver**: Solve equations like `3x + 5 = 14`
- **Quadratic Equation Solver**: Solve equations like `x² + 5x + 6 = 0` with detailed steps
- **Expression Simplification**: Basic algebraic simplification (like terms, factoring)

### 📐 Trigonometry Tools
- **Trigonometric Calculator**: Calculate sin, cos, tan and their inverses
- **Triangle Solver**: Solve triangles using Law of Sines and Law of Cosines
- **Unit Circle Reference**: Get unit circle values and quadrant analysis

### 📊 Advanced Math
- **Logarithm Calculator**: Natural and common logarithms with properties
- **Statistics Calculator**: Descriptive statistics and error analysis

## Installation

1. Clone or download the server files
2. Install dependencies:
```bash
pip install fastmcp mcp
```

Or install from requirements:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python math_mcp_server.py
```

## Development Installation

For development with additional tools:
```bash
pip install -e ".[dev]"
```

## Tool Reference

### `solve_quadratic_equation(equation: str)`
Solves quadratic equations with complete step-by-step solutions.

**Examples:**
```python
# Standard form
solve_quadratic_equation("x² + 5x + 6 = 0")

# Non-standard forms
solve_quadratic_equation("2x² - 8x + 6")
solve_quadratic_equation("x² = 4x - 3")
```

**Returns:** Complete solution with discriminant analysis, factored form, and verification.

### `solve_linear_equation(equation: str)`
Solves linear equations step by step.

**Examples:**
```python
solve_linear_equation("3x + 5 = 14")
solve_linear_equation("2x - 7 = x + 3")
```

### `trigonometry_calculator(function: str, value: float, unit: str = "degrees")`
Calculate trigonometric functions with detailed analysis.

**Parameters:**
- `function`: "sin", "cos", "tan", "arcsin", "arccos", "arctan"
- `value`: Input value (angle for trig functions, ratio for inverse functions)
- `unit`: "degrees" or "radians"

**Examples:**
```python
trigonometry_calculator("sin", 30, "degrees")
trigonometry_calculator("arctan", 0.5, "radians")
trigonometry_calculator("cos", 45, "degrees")
```

### `triangle_solver(triangle_data: str)`
Solve triangles using Law of Sines and Law of Cosines.

**Examples:**
```python
# SSS (three sides)
triangle_solver('{"sides": {"a": 3, "b": 4, "c": 5}}')

# SAS (two sides, included angle)
triangle_solver('{"sides": {"a": 5, "b": 7}, "angles": {"C": 60}}')

# AAS (two angles, one side)
triangle_solver('{"angles": {"A": 30, "B": 60}, "sides": {"c": 10}}')
```

### `unit_circle_reference(angle: float, unit: str = "degrees")`
Get complete unit circle information for any angle.

**Examples:**
```python
unit_circle_reference(45, "degrees")
unit_circle_reference(1.57, "radians")  # π/2
```

### `logarithm_calculator(operation: str, base: float = None, value: float = None, result: float = None)`
Calculate logarithms and exponentials.

**Examples:**
```python
# Natural logarithm
logarithm_calculator("log", None, 10)

# Common logarithm
logarithm_calculator("log", 10, 100)

# Antilog
logarithm_calculator("antilog", 10, 2)  # 10^2
```

### `algebra_simplify(expression: str)`
Simplify basic algebraic expressions.

**Examples:**
```python
algebra_simplify("2x + 3x")
algebra_simplify("x² - 4")
algebra_simplify("x² + 6x + 9")
```

### `statistics_calculator(data_type: str, values: str)`
Perform statistical calculations for data analysis.

**Examples:**
```python
# Descriptive statistics
statistics_calculator("descriptive", "1.2, 1.5, 1.3, 1.4, 1.6")

# Error analysis
statistics_calculator("error", "9.8, 9.9, 9.7, 9.8, 10.0")
```

## Physics Applications

This server is specifically designed for algebra-based physics courses and supports:

### Kinematics
- Quadratic equations for motion problems
- Trigonometry for vector components
- Statistical analysis of experimental data

### Forces and Vectors
- Triangle solving for force equilibrium
- Trigonometric decomposition of forces
- Error analysis for measurements

### Energy and Waves
- Logarithmic calculations for decibels and exponential decay
- Trigonometric functions for wave analysis
- Algebraic manipulation of energy equations

## Example Usage in Physics

### Finding Impact Time for Projectile Motion
```python
# Solve: h = h₀ + v₀t - ½gt²
# Rearrange to: ½gt² - v₀t + (h - h₀) = 0
solve_quadratic_equation("4.905t² - 20t + 15 = 0")
```

### Analyzing Force Components
```python
# Find components of 50N force at 30°
trigonometry_calculator("cos", 30, "degrees")  # x-component
trigonometry_calculator("sin", 30, "degrees")  # y-component
```

### Solving for Unknown Angle in Triangle
```python
# Given three sides of a triangle
triangle_solver('{"sides": {"a": 3, "b": 4, "c": 5}}')
```

## Error Handling

The server includes comprehensive error handling for:
- Invalid equation formats
- Out-of-domain values for trigonometric functions
- Insufficient data for triangle solving
- Division by zero in calculations

## Development Notes

This server follows the same patterns as your existing forces and kinematics MCP servers:
- Uses FastMCP for easy tool creation
- Provides detailed step-by-step solutions
- Includes verification of results
- Follows consistent formatting and error handling

## Contributing

To extend this server:
1. Add new tool functions using the `@mcp.tool()` decorator
2. Follow the existing pattern of detailed explanations
3. Include verification steps where possible
4. Handle edge cases and provide clear error messages

## License

This project is designed for educational use in physics courses.
