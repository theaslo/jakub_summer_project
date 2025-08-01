# ENERGY-SPECIFIC DIRECT TOOL METHODS
# Add these methods to the CombinedMathematicsAgent class in agent.py

    async def _solve_energy_problem_direct(self, problem: str) -> str:
        """Direct tool solving for energy problems"""
        problem_lower = problem.lower()
        
        # Kinetic energy calculations
        if any(word in problem_lower for word in ["kinetic energy", "ke", "kinetic", "moving", "velocity"]) and any(word in problem_lower for word in ["mass", "kg", "m/s"]):
            return await self._call_kinetic_energy_tool(problem)
            
        # Gravitational potential energy
        elif any(word in problem_lower for word in ["potential energy", "pe", "gravitational", "height", "mgh"]):
            return await self._call_gravitational_potential_energy_tool(problem)
            
        # Elastic potential energy (springs)
        elif any(word in problem_lower for word in ["spring", "elastic", "compressed", "stretched", "spring constant", "k="]):
            return await self._call_elastic_potential_energy_tool(problem)
            
        # Work calculations
        elif any(word in problem_lower for word in ["work", "force", "displacement", "distance"]) and any(word in problem_lower for word in ["angle", "cos", "n", "meter", "m"]):
            return await self._call_work_tool(problem)
            
        # Work-energy theorem
        elif any(word in problem_lower for word in ["work-energy theorem", "work energy", "net work", "change in kinetic"]):
            return await self._call_work_energy_theorem_tool(problem)
            
        # Energy conservation
        elif any(word in problem_lower for word in ["conservation", "conserved", "energy transformation", "dropped", "falls", "pendulum"]):
            return await self._call_energy_conservation_tool(problem)
            
        # Energy with friction
        elif any(word in problem_lower for word in ["friction", "braking", "sliding", "efficiency", "heat", "dissipation"]):
            return await self._call_energy_with_friction_tool(problem)
            
        # Complex energy systems
        elif any(word in problem_lower for word in ["roller coaster", "system", "multi", "complex", "track", "trajectory"]):
            return await self._call_analyze_energy_system_tool(problem)
            
        else:
            # Default based on keywords
            if any(word in problem_lower for word in ["kinetic", "velocity", "speed"]):
                return await self._call_kinetic_energy_tool(problem)
            elif any(word in problem_lower for word in ["height", "gravitational", "dropped", "fall"]):
                return await self._call_gravitational_potential_energy_tool(problem)
            elif any(word in problem_lower for word in ["spring", "elastic", "compressed"]):
                return await self._call_elastic_potential_energy_tool(problem)
            elif any(word in problem_lower for word in ["work", "force"]):
                return await self._call_work_tool(problem)
            else:
                return await self._call_energy_conservation_tool(problem)

    async def _call_kinetic_energy_tool(self, problem: str) -> str:
        """Call kinetic energy calculation tool"""
        try:
            if "calculate_kinetic_energy_tool" not in self.tool_dict:
                return "❌ calculate_kinetic_energy_tool not available"
            
            mass, velocity = self._parse_kinetic_energy_data(problem)
            
            tool = self.tool_dict["calculate_kinetic_energy_tool"]
            result = await tool.ainvoke({
                "mass": mass,
                "velocity": velocity
            })
            
            return f"🎯 **KINETIC ENERGY CALCULATION**\\n\\n{result}\\n\\n✅ **Calculation completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in kinetic energy calculation: {e}"

    async def _call_gravitational_potential_energy_tool(self, problem: str) -> str:
        """Call gravitational potential energy calculation tool"""
        try:
            if "calculate_gravitational_potential_energy_tool" not in self.tool_dict:
                return "❌ calculate_gravitational_potential_energy_tool not available"
            
            mass, height, gravity, reference_level = self._parse_gravitational_pe_data(problem)
            
            tool = self.tool_dict["calculate_gravitational_potential_energy_tool"]
            params = {
                "mass": mass,
                "height": height
            }
            if gravity != 9.81:
                params["gravity"] = gravity
            if reference_level != "ground":
                params["reference_level"] = reference_level
            
            result = await tool.ainvoke(params)
            
            return f"🎯 **GRAVITATIONAL POTENTIAL ENERGY CALCULATION**\\n\\n{result}\\n\\n✅ **Calculation completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in gravitational potential energy calculation: {e}"

    async def _call_elastic_potential_energy_tool(self, problem: str) -> str:
        """Call elastic potential energy calculation tool"""
        try:
            if "calculate_elastic_potential_energy_tool" not in self.tool_dict:
                return "❌ calculate_elastic_potential_energy_tool not available"
            
            spring_constant, displacement, equilibrium_position = self._parse_elastic_pe_data(problem)
            
            tool = self.tool_dict["calculate_elastic_potential_energy_tool"]
            params = {
                "spring_constant": spring_constant,
                "displacement": displacement
            }
            if equilibrium_position != "natural length":
                params["equilibrium_position"] = equilibrium_position
            
            result = await tool.ainvoke(params)
            
            return f"🎯 **ELASTIC POTENTIAL ENERGY CALCULATION**\\n\\n{result}\\n\\n✅ **Calculation completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in elastic potential energy calculation: {e}"

    async def _call_work_tool(self, problem: str) -> str:
        """Call work calculation tool"""
        try:
            if "calculate_work_tool" not in self.tool_dict:
                return "❌ calculate_work_tool not available"
            
            force, displacement, angle_degrees, force_type = self._parse_work_data(problem)
            
            tool = self.tool_dict["calculate_work_tool"]
            params = {
                "force": force,
                "displacement": displacement,
                "angle_degrees": angle_degrees
            }
            if force_type != "constant":
                params["force_type"] = force_type
            
            result = await tool.ainvoke(params)
            
            return f"🎯 **WORK CALCULATION**\\n\\n{result}\\n\\n✅ **Calculation completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in work calculation: {e}"

    async def _call_work_energy_theorem_tool(self, problem: str) -> str:
        """Call work-energy theorem tool"""
        try:
            if "work_energy_theorem" not in self.tool_dict:
                return "❌ work_energy_theorem tool not available"
            
            problem_data = self._parse_work_energy_theorem_data(problem)
            
            tool = self.tool_dict["work_energy_theorem"]
            result = await tool.ainvoke({
                "problem_data": json.dumps(problem_data)
            })
            
            return f"🎯 **WORK-ENERGY THEOREM ANALYSIS**\\n\\n{result}\\n\\n✅ **Analysis completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in work-energy theorem analysis: {e}"

    async def _call_energy_conservation_tool(self, problem: str) -> str:
        """Call energy conservation analysis tool"""
        try:
            if "energy_conservation" not in self.tool_dict:
                return "❌ energy_conservation tool not available"
            
            system_data = self._parse_energy_conservation_data(problem)
            
            tool = self.tool_dict["energy_conservation"]
            result = await tool.ainvoke({
                "system_data": json.dumps(system_data)
            })
            
            return f"🎯 **ENERGY CONSERVATION ANALYSIS**\\n\\n{result}\\n\\n✅ **Analysis completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in energy conservation analysis: {e}"

    async def _call_energy_with_friction_tool(self, problem: str) -> str:
        """Call energy with friction analysis tool"""
        try:
            if "energy_with_friction" not in self.tool_dict:
                return "❌ energy_with_friction tool not available"
            
            friction_data = self._parse_energy_with_friction_data(problem)
            
            tool = self.tool_dict["energy_with_friction"]
            result = await tool.ainvoke({
                "friction_data": json.dumps(friction_data)
            })
            
            return f"🎯 **ENERGY WITH FRICTION ANALYSIS**\\n\\n{result}\\n\\n✅ **Analysis completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in energy with friction analysis: {e}"

    async def _call_analyze_energy_system_tool(self, problem: str) -> str:
        """Call comprehensive energy system analysis tool"""
        try:
            if "analyze_energy_system" not in self.tool_dict:
                return "❌ analyze_energy_system tool not available"
            
            system_data = self._parse_energy_system_data(problem)
            
            tool = self.tool_dict["analyze_energy_system"]
            result = await tool.ainvoke({
                "system_data": json.dumps(system_data)
            })
            
            return f"🎯 **COMPREHENSIVE ENERGY SYSTEM ANALYSIS**\\n\\n{result}\\n\\n✅ **Analysis completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in energy system analysis: {e}"

    # PARSING METHODS (Energy)
    def _parse_kinetic_energy_data(self, text: str) -> tuple:
        """Parse kinetic energy parameters"""
        # Default values
        mass = 5.0
        velocity = 10.0
        
        # Parse mass
        mass_patterns = [
            r'(\d+(?:\.\d+)?)\s*kg',
            r'mass[:\s=]+(\d+(?:\.\d+)?)',
            r'm[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in mass_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                mass = float(match.group(1))
                break
        
        # Parse velocity
        velocity_patterns = [
            r'(\d+(?:\.\d+)?)\s*m/s',
            r'velocity[:\s=]+(\d+(?:\.\d+)?)',
            r'speed[:\s=]+(\d+(?:\.\d+)?)',
            r'v[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in velocity_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                velocity = float(match.group(1))
                break
        
        return mass, velocity

    def _parse_gravitational_pe_data(self, text: str) -> tuple:
        """Parse gravitational potential energy parameters"""
        # Default values
        mass = 2.0
        height = 15.0
        gravity = 9.81
        reference_level = "ground"
        
        # Parse mass
        mass_patterns = [
            r'(\d+(?:\.\d+)?)\s*kg',
            r'mass[:\s=]+(\d+(?:\.\d+)?)',
            r'm[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in mass_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                mass = float(match.group(1))
                break
        
        # Parse height
        height_patterns = [
            r'(\d+(?:\.\d+)?)\s*m(?:\\s|$)',
            r'height[:\s=]+(\d+(?:\.\d+)?)',
            r'h[:\s=]+(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*meter'
        ]
        
        for pattern in height_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                height = float(match.group(1))
                break
        
        # Parse gravity (if specified)
        gravity_patterns = [
            r'g[:\s=]+(\d+(?:\.\d+)?)',
            r'gravity[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in gravity_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                gravity = float(match.group(1))
                break
        
        # Parse reference level
        if "table" in text.lower():
            reference_level = "table"
        elif "floor" in text.lower():
            reference_level = "floor"
        elif "sea level" in text.lower():
            reference_level = "sea level"
        
        return mass, height, gravity, reference_level

    def _parse_elastic_pe_data(self, text: str) -> tuple:
        """Parse elastic potential energy parameters"""
        # Default values
        spring_constant = 200.0
        displacement = 0.1
        equilibrium_position = "natural length"
        
        # Parse spring constant
        k_patterns = [
            r'k[:\s=]+(\d+(?:\.\d+)?)',
            r'spring constant[:\s=]+(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*N/m'
        ]
        
        for pattern in k_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                spring_constant = float(match.group(1))
                break
        
        # Parse displacement
        displacement_patterns = [
            r'compressed[:\s]+(\d+(?:\.\d+)?)',
            r'stretched[:\s]+(\d+(?:\.\d+)?)',
            r'displacement[:\s=]+(\d+(?:\.\d+)?)',
            r'x[:\s=]+(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*m(?:\\s|$)',
            r'(\d+(?:\.\d+)?)\s*cm'
        ]
        
        for pattern in displacement_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                displacement = float(match.group(1))
                # Convert cm to m if needed
                if "cm" in match.group(0):
                    displacement /= 100
                break
        
        # Determine sign (compression vs stretch)
        if "compressed" in text.lower():
            displacement = abs(displacement)  # Positive for compression
        elif "stretched" in text.lower():
            displacement = abs(displacement)  # Positive for stretch
        
        return spring_constant, displacement, equilibrium_position

    def _parse_work_data(self, text: str) -> tuple:
        """Parse work calculation parameters"""
        # Default values
        force = 20.0
        displacement = 5.0
        angle_degrees = 0.0
        force_type = "constant"
        
        # Parse force
        force_patterns = [
            r'(\d+(?:\.\d+)?)\s*N',
            r'force[:\s=]+(\d+(?:\.\d+)?)',
            r'F[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in force_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                force = float(match.group(1))
                break
        
        # Parse displacement
        displacement_patterns = [
            r'(\d+(?:\.\d+)?)\s*m(?:\\s|$|[^/])',
            r'distance[:\s=]+(\d+(?:\.\d+)?)',
            r'displacement[:\s=]+(\d+(?:\.\d+)?)',
            r'd[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in displacement_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                displacement = float(match.group(1))
                break
        
        # Parse angle
        angle_patterns = [
            r'(\d+(?:\.\d+)?)\s*°',
            r'(\d+(?:\.\d+)?)\s*degree',
            r'angle[:\s=]+(\d+(?:\.\d+)?)',
            r'θ[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in angle_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                angle_degrees = float(match.group(1))
                break
        
        # Determine force type
        if "friction" in text.lower():
            force_type = "friction"
        elif "variable" in text.lower():
            force_type = "variable"
        elif "applied" in text.lower():
            force_type = "applied"
        
        return force, displacement, angle_degrees, force_type

    def _parse_work_energy_theorem_data(self, text: str) -> dict:
        """Parse work-energy theorem parameters"""
        data = {}
        
        # Parse mass
        mass_patterns = [
            r'(\d+(?:\.\d+)?)\s*kg',
            r'mass[:\s=]+(\d+(?:\.\d+)?)',
            r'm[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in mass_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["mass"] = float(match.group(1))
                break
        
        # Parse initial velocity
        initial_v_patterns = [
            r'initial velocity[:\s=]+(\d+(?:\.\d+)?)',
            r'vi[:\s=]+(\d+(?:\.\d+)?)',
            r'v0[:\s=]+(\d+(?:\.\d+)?)',
            r'starts.*?(\d+(?:\.\d+)?)\s*m/s'
        ]
        
        for pattern in initial_v_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["initial_velocity"] = float(match.group(1))
                break
        
        # Parse final velocity
        final_v_patterns = [
            r'final velocity[:\s=]+(\d+(?:\.\d+)?)',
            r'vf[:\s=]+(\d+(?:\.\d+)?)',
            r'final.*?(\d+(?:\.\d+)?)\s*m/s'
        ]
        
        for pattern in final_v_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["final_velocity"] = float(match.group(1))
                break
        
        # Parse work done
        work_patterns = [
            r'(\d+(?:\.\d+)?)\s*J',
            r'work[:\s=]+(\d+(?:\.\d+)?)',
            r'W[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in work_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["work_done"] = float(match.group(1))
                break
        
        # Parse force and displacement if present
        force_match = re.search(r'(\d+(?:\.\d+)?)\s*N', text, re.IGNORECASE)
        displacement_match = re.search(r'(\d+(?:\.\d+)?)\s*m(?:\\s|$|[^/])', text, re.IGNORECASE)
        
        if force_match:
            data["force"] = float(force_match.group(1))
        if displacement_match:
            data["displacement"] = float(displacement_match.group(1))
        
        # Default values if nothing found
        if not data:
            data = {"mass": 3, "initial_velocity": 5, "work_done": 40}
        
        return data

    def _parse_energy_conservation_data(self, text: str) -> dict:
        """Parse energy conservation parameters"""
        data = {}
        
        # Parse mass
        mass_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', text, re.IGNORECASE)
        if mass_match:
            data["mass"] = float(mass_match.group(1))
        else:
            data["mass"] = 2.0  # Default
        
        # Parse initial height
        initial_height_patterns = [
            r'(?:from|at|initial height)[:\s]+(\d+(?:\.\d+)?)\s*m',
            r'(\d+(?:\.\d+)?)\s*m.*?height',
            r'height.*?(\d+(?:\.\d+)?)\s*m'
        ]
        
        for pattern in initial_height_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["initial_height"] = float(match.group(1))
                break
        
        # Parse final height (often 0 for ground level)
        if "ground" in text.lower() or "floor" in text.lower():
            data["final_height"] = 0.0
        
        # Parse initial velocity
        initial_v_match = re.search(r'initial.*?(\d+(?:\.\d+)?)\s*m/s', text, re.IGNORECASE)
        if initial_v_match:
            data["initial_velocity"] = float(initial_v_match.group(1))
        elif "rest" in text.lower() or "dropped" in text.lower():
            data["initial_velocity"] = 0.0
        
        # Parse spring constant and compression/stretch
        k_match = re.search(r'k[:\s=]+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        compression_match = re.search(r'compress.*?(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        
        if k_match:
            data["spring_constant"] = float(k_match.group(1))
        if compression_match:
            data["compression"] = float(compression_match.group(1))
        
        # Default conservation scenario if minimal data
        if len(data) <= 1:
            data = {"mass": 2, "initial_height": 10, "final_height": 0, "initial_velocity": 0}
        
        return data

    def _parse_energy_with_friction_data(self, text: str) -> dict:
        """Parse energy with friction parameters"""
        data = {}
        
        # Parse mass
        mass_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', text, re.IGNORECASE)
        if mass_match:
            data["mass"] = float(mass_match.group(1))
        else:
            data["mass"] = 1500.0  # Default car mass
        
        # Parse initial velocity
        velocity_patterns = [
            r'(\d+(?:\.\d+)?)\s*m/s',
            r'velocity[:\s=]+(\d+(?:\.\d+)?)',
            r'speed[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in velocity_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["initial_velocity"] = float(match.group(1))
                break
        
        # Parse friction coefficient
        friction_patterns = [
            r'coefficient[:\s=]+(\d+(?:\.\d+)?)',
            r'μ[:\s=]+(\d+(?:\.\d+)?)',
            r'friction.*?(\d+(?:\.\d+)?)'
        ]
        
        for pattern in friction_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["friction_coefficient"] = float(match.group(1))
                break
        
        # Parse distance
        distance_match = re.search(r'(\d+(?:\.\d+)?)\s*m(?:\\s|$|[^/])', text, re.IGNORECASE)
        if distance_match:
            data["distance"] = float(distance_match.group(1))
        
        # Parse heights for inclined scenarios
        height_matches = re.findall(r'(\d+(?:\.\d+)?)\s*m', text, re.IGNORECASE)
        if len(height_matches) >= 2:
            data["initial_height"] = float(height_matches[0])
            data["final_height"] = float(height_matches[1])
        
        # Default braking scenario if minimal data
        if not data:
            data = {"mass": 1500, "initial_velocity": 25, "friction_coefficient": 0.7}
        
        return data

    def _parse_energy_system_data(self, text: str) -> dict:
        """Parse complex energy system parameters"""
        data = {"scenario": "general_system"}
        
        # Determine scenario type
        if "roller coaster" in text.lower():
            data["scenario"] = "roller_coaster"
        elif "pendulum" in text.lower():
            data["scenario"] = "pendulum"
        elif "spring" in text.lower() and "mass" in text.lower():
            data["scenario"] = "spring_mass"
        
        # Parse mass
        mass_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', text, re.IGNORECASE)
        if mass_match:
            data["mass"] = float(mass_match.group(1))
        else:
            data["mass"] = 500.0  # Default
        
        # For roller coaster scenarios
        if data["scenario"] == "roller_coaster":
            # Parse track points
            height_matches = re.findall(r'(\d+(?:\.\d+)?)\s*m', text, re.IGNORECASE)
            if height_matches:
                track_points = []
                for i, height in enumerate(height_matches):
                    point = {"height": float(height)}
                    if i == 0:
                        point["velocity"] = 0  # Start from rest typically
                    else:
                        point["velocity"] = None  # To be calculated
                    track_points.append(point)
                data["track_points"] = track_points
            
            # Parse friction coefficient
            friction_match = re.search(r'friction.*?(\d+(?:\.\d+)?)', text, re.IGNORECASE)
            if friction_match:
                data["friction_coefficient"] = float(friction_match.group(1))
            else:
                data["friction_coefficient"] = 0.02  # Low friction
            
            # Parse track length
            length_match = re.search(r'(\d+(?:\.\d+)?)\s*m.*?(?:long|length|track)', text, re.IGNORECASE)
            if length_match:
                data["track_length"] = float(length_match.group(1))
            else:
                data["track_length"] = 1000  # Default
        
        # For pendulum scenarios
        elif data["scenario"] == "pendulum":
            length_match = re.search(r'(\d+(?:\.\d+)?)\s*m.*?length', text, re.IGNORECASE)
            if length_match:
                data["length"] = float(length_match.group(1))
            else:
                data["length"] = 1.5
            
            angle_match = re.search(r'(\d+(?:\.\d+)?)\s*°', text, re.IGNORECASE)
            if angle_match:
                data["initial_angle_degrees"] = float(angle_match.group(1))
            else:
                data["initial_angle_degrees"] = 30
        
        # For spring-mass scenarios
        elif data["scenario"] == "spring_mass":
            k_match = re.search(r'k[:\s=]+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
            if k_match:
                data["spring_constant"] = float(k_match.group(1))
            else:
                data["spring_constant"] = 100
            
            amplitude_match = re.search(r'amplitude.*?(\d+(?:\.\d+)?)', text, re.IGNORECASE)
            if amplitude_match:
                data["amplitude"] = float(amplitude_match.group(1))
            else:
                data["amplitude"] = 0.1
        
        return data

# Additional methods to add to the _setup_agent_config method:

        elif self.agent_id == "energy_agent":
            from prompts.energy_agent_prompt import get_user_message, get_system_message, get_metadata
            self.get_system_message = get_system_message
            self.get_user_message = get_user_message
            self.metadata = get_metadata()
            self.mcp_port = 10105  # MCP port for energy agent on VM

# Additional condition to add to the _solve_with_direct_tools method:

        elif self.agent_id == "energy_agent":
            return await self._solve_energy_problem_direct(problem)

# Factory function to add:

def create_energy_agent(use_direct_tools: bool = True) -> CombinedMathematicsAgent:
    """Create an energy agent"""
    return CombinedMathematicsAgent(
        agent_id="energy_agent", 
        use_direct_tools=use_direct_tools
    )

# Interactive interface function to add:

async def interactive_energy_agent():
    """Interactive energy agent interface"""
    agent = create_energy_agent(use_direct_tools=True)  # Use working mode
    
    await agent.initialize()
    agent.get_user_message()
    
    while True:
        try:
            user_input = input(f"⚡ Energy Problem: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print(f"👋 Goodbye from Energy Agent!")
                break
                
            if not user_input:
                continue
                
            print("\\n🤖 Analyzing and solving...")
            result = await agent.solve_problem(user_input)
            
            if result["success"]:
                print("📊 SOLUTION:")
                print(result["solution"])
            else:
                print(f"❌ ERROR: {result['error']}")
                
            print("\\n" + "-"*70 + "\\n")
            
        except KeyboardInterrupt:
            print(f"\\n👋 Goodbye from Energy Agent!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\\n")
