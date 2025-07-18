# Forces MCP Server

A comprehensive Model Context Protocol (MCP) server for algebra-based force calculations and analysis. This server provides tools for all fundamental force operations including 1D and 2D force addition, component resolution, equilibrium analysis, free body diagrams, and specialized force calculations.

## Features

### Core Force Operations
- **1D Force Addition**: Add forces along a single axis
- **2D Force Addition**: Add multiple forces with magnitude and angle
- **Force Component Resolution**: Break forces into x and y components
- **Resultant Force Calculation**: Find magnitude and direction from components
- **Vector Operations**: Addition, subtraction, dot product, cross product

### Force Analysis Tools
- **Free Body Diagrams**: Generate text-based force diagrams
- **Equilibrium Analysis**: Check balance and suggest balancing forces
- **Inclined Plane Analysis**: Complete force analysis for objects on inclines

### Specialized Force Calculations
- **Spring Forces**: Hooke's Law calculations (F = -kx)
- **Friction Forces**: Static and kinetic friction (f = μN)
- **Weight/Gravitational Forces**: Weight calculations (W = mg)
- **Tension Forces**: Rope and pulley system analysis

## Available Tools

### `add_forces_1d(forces: str) -> str`
Add forces in one dimension along a line.

**Parameters:**
- `forces`: Comma-separated list of forces in Newtons (positive/negative for direction)

**Example:**
```json
{
  "forces": "10, -5, 15, -3"
}
```

### `add_forces_2d(forces_data: str) -> str`
Add multiple 2D forces to find the resultant.

**Parameters:**
- `forces_data`: JSON string with list of forces containing magnitude and angle

**Example:**
```json
{
  "forces_data": "[{\"magnitude\": 10, \"angle\": 30}, {\"magnitude\": 15, \"angle\": 120}]"
}
```

### `resolve_force_components(magnitude: float, angle_degrees: float) -> str`
Break down a force into its x and y components.

**Parameters:**
- `magnitude`: Force magnitude in Newtons
- `angle_degrees`: Angle in degrees (counterclockwise from positive x-axis)

**Example:**
```json
{
  "magnitude": 20,
  "angle_degrees": 30
}
```

### `find_resultant_force(force_components: str) -> str`
Find the resultant force from x and y components.

**Parameters:**
- `force_components`: JSON string with x and y components

**Example:**
```json
{
  "force_components": "{\"fx\": 8.66, \"fy\": 5.0}"
}
```

### `create_free_body_diagram(object_name: str, forces_data: str) -> str`
Generate a text-based free body diagram description.

**Parameters:**
- `object_name`: Name of the object (e.g., "box", "ball", "car")
- `forces_data`: JSON string with list of forces acting on the object

**Example:**
```json
{
  "object_name": "box",
  "forces_data": "[{\"name\": \"Weight\", \"magnitude\": 50, \"angle\": 270}, {\"name\": \"Normal\", \"magnitude\": 50, \"angle\": 90}, {\"name\": \"Applied\", \"magnitude\": 20, \"angle\": 0}]"
}
```

### `check_equilibrium(forces_data: str) -> str`
Check if forces are in equilibrium and suggest balancing force if needed.

**Parameters:**
- `forces_data`: JSON string with list of forces

**Example:**
```json
{
  "forces_data": "[{\"magnitude\": 10, \"angle\": 0}, {\"magnitude\": 15, \"angle\": 120}]"
}
```

### `calculate_spring_force_tool(spring_constant: float, displacement: float) -> str`
Calculate spring force using Hooke's Law.

**Parameters:**
- `spring_constant`: Spring constant k in N/m
- `displacement`: Displacement from equilibrium in meters (positive = stretched, negative = compressed)

**Example:**
```json
{
  "spring_constant": 100,
  "displacement": 0.05
}
```

### `calculate_friction_force_tool(coefficient: float, normal_force: float, force_type: str = "kinetic") -> str`
Calculate friction force.

**Parameters:**
- `coefficient`: Coefficient of friction (μ)
- `normal_force`: Normal force in Newtons
- `force_type`: Type of friction - "kinetic" or "static"

**Example:**
```json
{
  "coefficient": 0.3,
  "normal_force": 100,
  "force_type": "kinetic"
}
```

### `calculate_weight_force(mass: float, gravity: float = 9.81) -> str`
Calculate gravitational/weight force.

**Parameters:**
- `mass`: Mass of the object in kilograms
- `gravity`: Acceleration due to gravity in m/s² (default: 9.81 for Earth)

**Example:**
```json
{
  "mass": 10,
  "gravity": 9.81
}
```

### `analyze_forces_on_incline(mass: float, angle_degrees: float, coefficient_friction: float = 0.0, gravity: float = 9.81) -> str`
Analyze forces acting on an object on an inclined plane.

**Parameters:**
- `mass`: Mass of the object in kg
- `angle_degrees`: Angle of the incline in degrees (from horizontal)
- `coefficient_friction`: Coefficient of kinetic friction (default: 0.0 for frictionless)
- `gravity`: Acceleration due to gravity in m/s² (default: 9.81)

**Example:**
```json
{
  "mass": 5,
  "angle_degrees": 30,
  "coefficient_friction": 0.2,
  "gravity": 9.81
}
```

### `force_vector_operations(operation: str, vector_data: str) -> str`
Perform vector operations on forces.

**Parameters:**
- `operation`: Type of operation - "add", "subtract", "dot_product", "cross_product"
- `vector_data`: JSON string with vector information

**Examples:**
```json
// Addition/Subtraction
{
  "operation": "add",
  "vector_data": "{\"vectors\": [{\"fx\": 10, \"fy\": 5}, {\"fx\": -3, \"fy\": 8}]}"
}

// Dot Product
{
  "operation": "dot_product", 
  "vector_data": "{\"vector1\": {\"fx\": 4, \"fy\": 3}, \"vector2\": {\"fx\": 2, \"fy\": 1}}"
}
```

### `analyze_tension_forces(masses: str, angles: str = "0", gravity: float = 9.81) -> str`
Analyze tension forces in rope/string systems.

**Parameters:**
- `masses`: Comma-separated list of masses in kg
- `angles`: Comma-separated list of angles in degrees for each mass (default: "0")
- `gravity`: Acceleration due to gravity in m/s² (default: 9.81)

**Example:**
```json
{
  "masses": "5, 10",
  "angles": "0, 0",
  "gravity": 9.81
}
```

## Running the Server

### Standalone Testing
To run the forces server independently for testing:

```bash
cd forces_mcp
uv run main.py
```

### Using MCP Inspector
To test the server with the MCP Inspector:

```bash
cd forces_mcp
npx @modelcontextprotocol/inspector@latest uv run main.py
```

The inspector will open a web interface where you can:
- View all available tools and their schemas
- Test tool execution with different parameters
- Debug server responses and errors
- Verify server initialization

## Usage Examples

### Example 1: 2D Force Addition
```json
{
  "tool": "add_forces_2d",
  "parameters": {
    "forces_data": "[{\"magnitude\": 10, \"angle\": 0}, {\"magnitude\": 15, \"angle\": 90}, {\"magnitude\": 8, \"angle\": 180}]"
  }
}
```

This will calculate the resultant of three forces: 10N rightward, 15N upward, and 8N leftward.

### Example 2: Free Body Diagram
```json
{
  "tool": "create_free_body_diagram",
  "parameters": {
    "object_name": "block",
    "forces_data": "[{\"name\": \"Weight\", \"magnitude\": 98, \"angle\": 270}, {\"name\": \"Normal\", \"magnitude\": 98, \"angle\": 90}, {\"name\": \"Applied\", \"magnitude\": 50, \"angle\": 0}, {\"name\": \"Friction\", \"magnitude\": 20, \"angle\": 180}]"
  }
}
```

This creates a free body diagram for a block with weight, normal force, applied force, and friction.

### Example 3: Inclined Plane Analysis
```json
{
  "tool": "analyze_forces_on_incline",
  "parameters": {
    "mass": 10,
    "angle_degrees": 30,
    "coefficient_friction": 0.25,
    "gravity": 9.81
  }
}
```

This analyzes all forces on a 10kg object on a 30° incline with friction.

## Important Notes

### Angle Convention
- All angles are measured in **degrees** (not radians)
- Angles are measured **counterclockwise** from the positive x-axis
- 0° = rightward (→)
- 90° = upward (↑)
- 180° = leftward (←)
- 270° = downward (↓)

### Force Direction Conventions
- **1D Forces**: Positive values = positive direction, Negative values = negative direction
- **2D Forces**: Specified by magnitude (always positive) and angle
- **Components**: Fx (horizontal), Fy (vertical)

### JSON Format Requirements
When using JSON strings as parameters, ensure proper formatting:
- Use double quotes for keys and string values
- Escape quotes in JSON strings: `"{\"key\": \"value\"}"`
- Arrays: `"[{\"item1\": value}, {\"item2\": value}]"`

## Integration with Other Systems

This MCP server is designed to work with:
- **LangChain MCP Adapters**: For integration with LangChain applications
- **Agent Orchestration Systems**: As a tool provider for multi-agent systems
- **Educational Platforms**: For physics problem solving and tutoring
- **Engineering Applications**: For basic force analysis and design

## Development and Customization

### Adding New Force Types
To add new specialized force calculations, follow this pattern:

```python
@mcp.tool()
async def calculate_new_force(param1: float, param2: str) -> str:
    """Description of the new force calculation.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        str: Calculation results and explanation
    """
    try:
        # Implementation here
        result = f"""
New Force Calculation:
====================
[Detailed calculation steps and results]
"""
        return result
    except Exception as e:
        return f"Error in calculation: {str(e)}"
```

### Error Handling
The server includes comprehensive error handling for:
- Invalid JSON formats
- Missing required parameters
- Mathematical errors (division by zero, etc.)
- Type conversion errors

All errors return descriptive messages to help users correct their input.

## Dependencies

- `mcp`: Model Context Protocol framework
- `math`: Standard mathematical functions
- `json`: JSON parsing and formatting
- `typing`: Type hints support

## License

This forces MCP server is part of the jakub_summer_project and follows the same licensing terms.
