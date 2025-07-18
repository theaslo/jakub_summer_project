from typing import List, Tuple, Any
import math
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("forces")

def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians for internal calculations."""
    return math.radians(degrees)

def format_force_result(force_x: float, force_y: float, magnitude: float, angle: float) -> str:
    """Format force calculation results into a readable string."""
    return f"""
Force Components:
- X-component: {force_x:.2f} N
- Y-component: {force_y:.2f} N
- Magnitude: {magnitude:.2f} N
- Direction: {angle:.1f}° (measured counterclockwise from positive x-axis)
"""

def calculate_force_components(magnitude: float, angle_degrees: float) -> Tuple[float, float]:
    """Calculate x and y components from magnitude and angle."""
    angle_rad = degrees_to_radians(angle_degrees)
    force_x = magnitude * math.cos(angle_rad)
    force_y = magnitude * math.sin(angle_rad)
    return force_x, force_y

def calculate_resultant_force(force_x_total: float, force_y_total: float) -> Tuple[float, float]:
    """Calculate magnitude and angle from x and y components."""
    magnitude = math.sqrt(force_x_total**2 + force_y_total**2)
    if force_x_total == 0:
        angle = 90.0 if force_y_total > 0 else 270.0
    else:
        angle = math.degrees(math.atan2(force_y_total, force_x_total))
        if angle < 0:
            angle += 360  # Convert to positive angle
    return magnitude, angle

@mcp.tool()
async def add_forces_1d(forces: str) -> str:
    """Add forces in one dimension (along a line).
    
    Args:
        forces: Comma-separated list of forces in Newtons. 
                Use positive values for forces in positive direction,
                negative values for forces in negative direction.
                Example: "10, -5, 15, -3"
    
    Returns:
        str: Net force calculation and explanation
    """
    try:
        force_list = [float(f.strip()) for f in forces.split(',')]
        net_force = sum(force_list)
        
        result = f"""
        1D Force Addition:
        Individual Forces: {', '.join([f'{f:.1f} N' for f in force_list])}
        Net Force: {net_force:.2f} N

        Explanation:
        - Positive forces act in the positive direction
        - Negative forces act in the negative direction
        - Net force = {' + '.join([f'({f:.1f})' for f in force_list])} = {net_force:.2f} N
        """
        
        if net_force > 0:
            result += "- The net force acts in the positive direction"
        elif net_force < 0:
            result += "- The net force acts in the negative direction"
        else:
            result += "- The forces are balanced (net force = 0)"
            
        return result
        
    except ValueError:
        return "Error: Please provide valid numbers separated by commas (e.g., '10, -5, 15')"

async def add_forces_2d(forces_data: str) -> str:
    """Add multiple 2D forces using '[{"magnitude": 10, "angle": 30}, ...]' format."""
    try:
        if isinstance(forces_data, str):
            if forces_data.startswith("[{") and '"' not in forces_data:
                forces_data = forces_data.replace("'", '"')  # Patch single quotes to double quotes
            forces = json.loads(forces_data)
        else:
            forces = forces_data

        total_fx, total_fy = 0, 0
        force_details = []

        for i, force in enumerate(forces, 1):
            magnitude = float(force['magnitude'])
            angle = float(force['angle'])
            fx, fy = calculate_force_components(magnitude, angle)
            total_fx += fx
            total_fy += fy
            force_details.append(f"Force {i}: {magnitude:.1f} N at {angle:.1f}° → Fx = {fx:.2f} N, Fy = {fy:.2f} N")

        net_magnitude, net_angle = calculate_resultant_force(total_fx, total_fy)

        result = f"""
2D Force Addition:

Individual Forces:
{chr(10).join(force_details)}

Net Force Components:
- Total Fx = {total_fx:.2f} N
- Total Fy = {total_fy:.2f} N

Resultant Force:
- Magnitude = √(Fx² + Fy²) = √({total_fx:.2f}² + {total_fy:.2f}²) = {net_magnitude:.2f} N
- Direction = {net_angle:.1f}° (counterclockwise from +x axis)
"""
        if abs(net_magnitude) < 0.01:
            result += "\nThe forces are balanced (net force ≈ 0)"

        return result.strip()
    except Exception as e:
        return f"Error: {str(e)}\nExpected format: '[{{\"magnitude\": 10, \"angle\": 30}}]'"
@mcp.tool()
async def resolve_force_components(magnitude: float, angle_degrees: float) -> str:
    """Break down a force into its x and y components.
    
    Args:
        magnitude: Force magnitude in Newtons
        angle_degrees: Angle in degrees (counterclockwise from positive x-axis)
    
    Returns:
        str: Force components calculation and explanation
    """
    try:
        force_x, force_y = calculate_force_components(magnitude, angle_degrees)
        
        result = f"""
Force Component Analysis:

Given Force:
- Magnitude: {magnitude:.2f} N
- Angle: {angle_degrees:.1f}°

Component Calculations:
- Fx = F × cos(θ) = {magnitude:.2f} × cos({angle_degrees:.1f}°) = {force_x:.2f} N
- Fy = F × sin(θ) = {magnitude:.2f} × sin({angle_degrees:.1f}°) = {force_y:.2f} N

Result:
- X-component: {force_x:.2f} N
- Y-component: {force_y:.2f} N

Verification: √(Fx² + Fy²) = √({force_x:.2f}² + {force_y:.2f}²) = {magnitude:.2f} N ✓
"""
        return result
        
    except Exception as e:
        return f"Error in calculation: {str(e)}"

@mcp.tool()
async def find_resultant_force(force_components: str) -> str:
    """Find the resultant force from x and y components.
    
    Args:
        force_components: JSON string with x and y components.
                         Example: '{"fx": 8.66, "fy": 5.0}'
    
    Returns:
        str: Resultant force magnitude and direction
    """
    try:
        components = json.loads(force_components)
        fx = components['fx']
        fy = components['fy']
        
        magnitude, angle = calculate_resultant_force(fx, fy)
        
        result = f"""
Resultant Force Calculation:

Given Components:
- Fx = {fx:.2f} N
- Fy = {fy:.2f} N

Magnitude Calculation:
- |F| = √(Fx² + Fy²) = √({fx:.2f}² + {fy:.2f}²) = {magnitude:.2f} N

Direction Calculation:
- θ = arctan(Fy/Fx) = arctan({fy:.2f}/{fx:.2f}) = {angle:.1f}°

Resultant Force:
- Magnitude: {magnitude:.2f} N
- Direction: {angle:.1f}° (counterclockwise from +x axis)
"""
        
        return result
        
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return 'Error: Please provide valid JSON format like {"fx": 8.66, "fy": 5.0}'

@mcp.tool()
async def create_free_body_diagram(object_name: str, forces_data: str) -> str:
    """Generate a text-based free body diagram description.
    
    Args:
        object_name: Name of the object (e.g., "box", "ball", "car")
        forces_data: JSON string with list of forces acting on the object.
                    Example: '[{"name": "Weight", "magnitude": 50, "angle": 270}, 
                             {"name": "Normal", "magnitude": 50, "angle": 90},
                             {"name": "Applied", "magnitude": 20, "angle": 0}]'
    
    Returns:
        str: Text description of the free body diagram with force analysis
    """
    try:
        forces = json.loads(forces_data)
        
        diagram_text = f"""
FREE BODY DIAGRAM: {object_name.upper()}

Object: {object_name} (represented as a dot or simple shape)

Forces Acting on {object_name}:
"""
        
        total_fx = 0
        total_fy = 0
        
        for force in forces:
            name = force['name']
            magnitude = force['magnitude']
            angle = force['angle']
            
            fx, fy = calculate_force_components(magnitude, angle)
            total_fx += fx
            total_fy += fy
            
            # Describe force direction
            if angle == 0:
                direction = "→ (right)"
            elif angle == 90:
                direction = "↑ (up)"
            elif angle == 180:
                direction = "← (left)"
            elif angle == 270:
                direction = "↓ (down)"
            else:
                direction = f"at {angle:.1f}° from +x axis"
            
            diagram_text += f"- {name}: {magnitude:.1f} N {direction}\n"
        
        net_magnitude, net_angle = calculate_resultant_force(total_fx, total_fy)
        
        diagram_text += f"""
Force Analysis:
- Total Fx = {total_fx:.2f} N
- Total Fy = {total_fy:.2f} N
- Net Force = {net_magnitude:.2f} N at {net_angle:.1f}°

Equilibrium Status:
"""
        
        if abs(net_magnitude) < 0.01:
            diagram_text += "✓ Object is in equilibrium (net force = 0)"
        else:
            diagram_text += f"✗ Object is NOT in equilibrium (net force = {net_magnitude:.2f} N)"
            
        return diagram_text
        
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return 'Error: Please provide valid JSON format like [{"name": "Weight", "magnitude": 50, "angle": 270}]'

@mcp.tool()
async def check_equilibrium(forces_data: str) -> str:
    """Check if forces are in equilibrium and suggest balancing force if needed.
    
    Args:
        forces_data: JSON string with list of forces.
                    Example: '[{"magnitude": 10, "angle": 0}, {"magnitude": 15, "angle": 120}]'
    
    Returns:
        str: Equilibrium analysis and balancing force if needed
    """
    try:
        forces = json.loads(forces_data)
        
        total_fx = 0
        total_fy = 0
        
        force_summary = "Forces Applied:\n"
        for i, force in enumerate(forces, 1):
            magnitude = force['magnitude']
            angle = force['angle']
            fx, fy = calculate_force_components(magnitude, angle)
            total_fx += fx
            total_fy += fy
            force_summary += f"- Force {i}: {magnitude:.1f} N at {angle:.1f}°\n"
        
        net_magnitude, net_angle = calculate_resultant_force(total_fx, total_fy)
        
        result = f"""
Equilibrium Analysis:

{force_summary}
Net Force Components:
- Fx = {total_fx:.2f} N
- Fy = {total_fy:.2f} N
- Net Force = {net_magnitude:.2f} N at {net_angle:.1f}°

"""
        
        if abs(net_magnitude) < 0.01:
            result += "✓ EQUILIBRIUM: The forces are balanced!"
        else:
            # Calculate balancing force
            balance_fx = -total_fx
            balance_fy = -total_fy
            balance_magnitude, balance_angle = calculate_resultant_force(balance_fx, balance_fy)
            
            result += f"""✗ NOT IN EQUILIBRIUM

To achieve equilibrium, add a balancing force:
- Magnitude: {balance_magnitude:.2f} N
- Direction: {balance_angle:.1f}° (counterclockwise from +x axis)
- Components: Fx = {balance_fx:.2f} N, Fy = {balance_fy:.2f} N

This balancing force will cancel out the net force and restore equilibrium.
"""
        
        return result
        
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return 'Error: Please provide valid JSON format like [{"magnitude": 10, "angle": 30}]'

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')