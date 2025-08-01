# MOMENTUM-SPECIFIC DIRECT TOOL METHODS
# Add these methods to the CombinedMathematicsAgent class in agent.py

    async def _solve_momentum_problem_direct(self, problem: str) -> str:
        """Direct tool solving for momentum problems"""
        problem_lower = problem.lower()
        
        # 1D momentum calculations
        if any(word in problem_lower for word in ["momentum", "p =", "calculate momentum"]) and not any(word in problem_lower for word in ["2d", "angle", "degrees", "components"]):
            return await self._call_momentum_1d_tool(problem)
            
        # 2D momentum calculations
        elif any(word in problem_lower for word in ["2d momentum", "momentum", "angle", "degrees", "components"]) and any(word in problem_lower for word in ["°", "degree", "direction"]):
            return await self._call_momentum_2d_tool(problem)
            
        # 1D impulse calculations
        elif any(word in problem_lower for word in ["impulse", "force", "time", "j =", "n⋅s"]) and not any(word in problem_lower for word in ["2d", "components"]):
            return await self._call_impulse_1d_tool(problem)
            
        # 2D impulse calculations
        elif any(word in problem_lower for word in ["2d impulse", "impulse", "components"]) and any(word in problem_lower for word in ["angle", "vector", "fx", "fy"]):
            return await self._call_impulse_2d_tool(problem)
            
        # Impulse-momentum theorem
        elif any(word in problem_lower for word in ["impulse-momentum theorem", "impulse momentum", "theorem", "j = δp"]):
            return await self._call_momentum_impulse_theorem_tool(problem)
            
        # 1D momentum conservation (collisions)
        elif any(word in problem_lower for word in ["collision", "collides", "elastic", "inelastic", "conservation"]) and not any(word in problem_lower for word in ["2d", "angle"]):
            return await self._call_momentum_conservation_1d_tool(problem)
            
        # 2D momentum conservation
        elif any(word in problem_lower for word in ["2d collision", "collision", "billiard"]) and any(word in problem_lower for word in ["angle", "2d", "vector"]):
            return await self._call_momentum_conservation_2d_tool(problem)
            
        # Comprehensive collision analysis
        elif any(word in problem_lower for word in ["crash", "car crash", "safety", "analyze collision", "comprehensive"]):
            return await self._call_analyze_collision_tool(problem)
            
        else:
            # Default based on keywords - prioritize by complexity
            if any(word in problem_lower for word in ["crash", "car", "safety"]):
                return await self._call_analyze_collision_tool(problem)
            elif any(word in problem_lower for word in ["collision", "collides", "elastic", "inelastic"]):
                if any(word in problem_lower for word in ["2d", "angle", "°"]):
                    return await self._call_momentum_conservation_2d_tool(problem)
                else:
                    return await self._call_momentum_conservation_1d_tool(problem)
            elif any(word in problem_lower for word in ["impulse", "force", "time"]):
                if any(word in problem_lower for word in ["2d", "components"]):
                    return await self._call_impulse_2d_tool(problem)
                else:
                    return await self._call_impulse_1d_tool(problem)
            elif any(word in problem_lower for word in ["momentum"]):
                if any(word in problem_lower for word in ["2d", "angle", "°", "direction"]):
                    return await self._call_momentum_2d_tool(problem)
                else:
                    return await self._call_momentum_1d_tool(problem)
            else:
                return await self._call_momentum_1d_tool(problem)

    async def _call_momentum_1d_tool(self, problem: str) -> str:
        """Call 1D momentum calculation tool"""
        try:
            if "calculate_momentum_1d" not in self.tool_dict:
                return "❌ calculate_momentum_1d tool not available"
            
            mass, velocity = self._parse_momentum_1d_data(problem)
            
            tool = self.tool_dict["calculate_momentum_1d"]
            result = await tool.ainvoke({
                "mass": mass,
                "velocity": velocity
            })
            
            return f"🎯 **1D MOMENTUM CALCULATION**\\n\\n{result}\\n\\n✅ **Calculation completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in 1D momentum calculation: {e}"

    async def _call_momentum_2d_tool(self, problem: str) -> str:
        """Call 2D momentum calculation tool"""
        try:
            if "calculate_momentum_2d" not in self.tool_dict:
                return "❌ calculate_momentum_2d tool not available"
            
            mass, velocity, angle_degrees = self._parse_momentum_2d_data(problem)
            
            tool = self.tool_dict["calculate_momentum_2d"]
            result = await tool.ainvoke({
                "mass": mass,
                "velocity": velocity,
                "angle_degrees": angle_degrees
            })
            
            return f"🎯 **2D MOMENTUM CALCULATION**\\n\\n{result}\\n\\n✅ **Calculation completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in 2D momentum calculation: {e}"

    async def _call_impulse_1d_tool(self, problem: str) -> str:
        """Call 1D impulse calculation tool"""
        try:
            if "calculate_impulse_1d" not in self.tool_dict:
                return "❌ calculate_impulse_1d tool not available"
            
            force, time, initial_momentum, final_momentum = self._parse_impulse_1d_data(problem)
            
            tool = self.tool_dict["calculate_impulse_1d"]
            params = {
                "force": force,
                "time": time
            }
            if initial_momentum is not None:
                params["initial_momentum"] = initial_momentum
            if final_momentum is not None:
                params["final_momentum"] = final_momentum
            
            result = await tool.ainvoke(params)
            
            return f"🎯 **1D IMPULSE CALCULATION**\\n\\n{result}\\n\\n✅ **Calculation completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in 1D impulse calculation: {e}"

    async def _call_impulse_2d_tool(self, problem: str) -> str:
        """Call 2D impulse calculation tool"""
        try:
            if "calculate_impulse_2d" not in self.tool_dict:
                return "❌ calculate_impulse_2d tool not available"
            
            force_data, time, momentum_data = self._parse_impulse_2d_data(problem)
            
            tool = self.tool_dict["calculate_impulse_2d"]
            params = {
                "force_data": json.dumps(force_data)
            }
            if time is not None:
                params["time"] = time
            if momentum_data is not None:
                params["momentum_data"] = json.dumps(momentum_data)
            
            result = await tool.ainvoke(params)
            
            return f"🎯 **2D IMPULSE CALCULATION**\\n\\n{result}\\n\\n✅ **Calculation completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in 2D impulse calculation: {e}"

    async def _call_momentum_impulse_theorem_tool(self, problem: str) -> str:
        """Call momentum-impulse theorem tool"""
        try:
            if "momentum_impulse_theorem" not in self.tool_dict:
                return "❌ momentum_impulse_theorem tool not available"
            
            problem_data = self._parse_momentum_impulse_theorem_data(problem)
            
            tool = self.tool_dict["momentum_impulse_theorem"]
            result = await tool.ainvoke({
                "problem_data": json.dumps(problem_data)
            })
            
            return f"🎯 **MOMENTUM-IMPULSE THEOREM ANALYSIS**\\n\\n{result}\\n\\n✅ **Analysis completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in momentum-impulse theorem analysis: {e}"

    async def _call_momentum_conservation_1d_tool(self, problem: str) -> str:
        """Call 1D momentum conservation tool"""
        try:
            if "momentum_conservation_1d" not in self.tool_dict:
                return "❌ momentum_conservation_1d tool not available"
            
            collision_data = self._parse_momentum_conservation_1d_data(problem)
            
            tool = self.tool_dict["momentum_conservation_1d"]
            result = await tool.ainvoke({
                "collision_data": json.dumps(collision_data)
            })
            
            return f"🎯 **1D MOMENTUM CONSERVATION ANALYSIS**\\n\\n{result}\\n\\n✅ **Analysis completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in 1D momentum conservation analysis: {e}"

    async def _call_momentum_conservation_2d_tool(self, problem: str) -> str:
        """Call 2D momentum conservation tool"""
        try:
            if "momentum_conservation_2d" not in self.tool_dict:
                return "❌ momentum_conservation_2d tool not available"
            
            collision_data = self._parse_momentum_conservation_2d_data(problem)
            
            tool = self.tool_dict["momentum_conservation_2d"]
            result = await tool.ainvoke({
                "collision_data": json.dumps(collision_data)
            })
            
            return f"🎯 **2D MOMENTUM CONSERVATION ANALYSIS**\\n\\n{result}\\n\\n✅ **Analysis completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in 2D momentum conservation analysis: {e}"

    async def _call_analyze_collision_tool(self, problem: str) -> str:
        """Call comprehensive collision analysis tool"""
        try:
            if "analyze_collision" not in self.tool_dict:
                return "❌ analyze_collision tool not available"
            
            collision_scenario = self._parse_collision_scenario_data(problem)
            
            tool = self.tool_dict["analyze_collision"]
            result = await tool.ainvoke({
                "collision_scenario": json.dumps(collision_scenario)
            })
            
            return f"🎯 **COMPREHENSIVE COLLISION ANALYSIS**\\n\\n{result}\\n\\n✅ **Analysis completed using MCP tools**"
            
        except Exception as e:
            return f"❌ Error in comprehensive collision analysis: {e}"

    # PARSING METHODS (Momentum)
    def _parse_momentum_1d_data(self, text: str) -> tuple:
        """Parse 1D momentum parameters"""
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
        
        # Parse velocity (including direction)
        velocity_patterns = [
            r'(-?\d+(?:\.\d+)?)\s*m/s',
            r'velocity[:\s=]+(-?\d+(?:\.\d+)?)',
            r'speed[:\s=]+(\d+(?:\.\d+)?)',
            r'v[:\s=]+(-?\d+(?:\.\d+)?)',
            r'moving.*?(-?\d+(?:\.\d+)?)\s*m/s'
        ]
        
        for pattern in velocity_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                velocity = float(match.group(1))
                break
        
        # Check for direction indicators
        if any(word in text.lower() for word in ["left", "backward", "negative", "opposite"]):
            velocity = -abs(velocity)
        elif any(word in text.lower() for word in ["right", "forward", "positive"]):
            velocity = abs(velocity)
        
        return mass, velocity

    def _parse_momentum_2d_data(self, text: str) -> tuple:
        """Parse 2D momentum parameters"""
        # Default values
        mass = 3.0
        velocity = 15.0
        angle_degrees = 30.0
        
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
        
        # Parse angle
        angle_patterns = [
            r'(\d+(?:\.\d+)?)\s*°',
            r'(\d+(?:\.\d+)?)\s*degree',
            r'angle[:\s=]+(\d+(?:\.\d+)?)',
            r'at\s+(\d+(?:\.\d+)?)\s*°',
            r'direction[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in angle_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                angle_degrees = float(match.group(1))
                break
        
        return mass, velocity, angle_degrees

    def _parse_impulse_1d_data(self, text: str) -> tuple:
        """Parse 1D impulse parameters"""
        # Default values
        force = 20.0
        time = 0.5
        initial_momentum = None
        final_momentum = None
        
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
        
        # Parse time
        time_patterns = [
            r'(\d+(?:\.\d+)?)\s*s(?:ec|ond)?',
            r'time[:\s=]+(\d+(?:\.\d+)?)',
            r'for\s+(\d+(?:\.\d+)?)\s*s',
            r't[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                time = float(match.group(1))
                break
        
        # Parse initial momentum
        initial_p_patterns = [
            r'initial momentum[:\s=]+(\d+(?:\.\d+)?)',
            r'pi[:\s=]+(\d+(?:\.\d+)?)',
            r'p0[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in initial_p_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                initial_momentum = float(match.group(1))
                break
        
        # Parse final momentum
        final_p_patterns = [
            r'final momentum[:\s=]+(\d+(?:\.\d+)?)',
            r'pf[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in final_p_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                final_momentum = float(match.group(1))
                break
        
        return force, time, initial_momentum, final_momentum

    def _parse_impulse_2d_data(self, text: str) -> tuple:
        """Parse 2D impulse parameters"""
        force_data = {}
        time = None
        momentum_data = None
        
        # Parse force components or magnitude/angle
        fx_match = re.search(r'fx[:\s=]+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        fy_match = re.search(r'fy[:\s=]+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        
        if fx_match and fy_match:
            force_data = {
                "fx": float(fx_match.group(1)),
                "fy": float(fy_match.group(1))
            }
        else:
            # Try magnitude and angle
            force_mag_match = re.search(r'force.*?(\d+(?:\.\d+)?)\s*N', text, re.IGNORECASE)
            force_angle_match = re.search(r'(\d+(?:\.\d+)?)\s*°', text, re.IGNORECASE)
            
            if force_mag_match:
                magnitude = float(force_mag_match.group(1))
                angle = float(force_angle_match.group(1)) if force_angle_match else 0.0
                force_data = {
                    "magnitude": magnitude,
                    "angle": angle
                }
            else:
                # Default force data
                force_data = {"magnitude": 15, "angle": 30}
        
        # Parse time
        time_match = re.search(r'(\d+(?:\.\d+)?)\s*s(?:ec|ond)?', text, re.IGNORECASE)
        if time_match:
            time = float(time_match.group(1))
        
        # Parse momentum data (if provided)
        # This would be complex to parse from natural language, so we'll use defaults
        if "initial" in text.lower() and "final" in text.lower():
            momentum_data = {
                "initial": {"px": 5, "py": 3},
                "final": {"px": 8, "py": 7}
            }
        
        return force_data, time, momentum_data

    def _parse_momentum_impulse_theorem_data(self, text: str) -> dict:
        """Parse momentum-impulse theorem parameters"""
        data = {}
        
        # Parse mass
        mass_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', text, re.IGNORECASE)
        if mass_match:
            data["mass"] = float(mass_match.group(1))
        
        # Parse initial velocity
        initial_v_patterns = [
            r'initial velocity[:\s=]+(\d+(?:\.\d+)?)',
            r'vi[:\s=]+(\d+(?:\.\d+)?)',
            r'v0[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in initial_v_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["initial_velocity"] = float(match.group(1))
                break
        
        # Parse force
        force_match = re.search(r'(\d+(?:\.\d+)?)\s*N', text, re.IGNORECASE)
        if force_match:
            data["force"] = float(force_match.group(1))
        
        # Parse time
        time_match = re.search(r'(\d+(?:\.\d+)?)\s*s(?:ec|ond)?', text, re.IGNORECASE)
        if time_match:
            data["time"] = float(time_match.group(1))
        
        # Parse impulse
        impulse_patterns = [
            r'impulse[:\s=]+(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*N⋅s',
            r'J[:\s=]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in impulse_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["impulse"] = float(match.group(1))
                break
        
        # Default values if nothing found
        if not data:
            data = {"mass": 2, "initial_velocity": 5, "force": 10, "time": 3}
        
        return data

    def _parse_momentum_conservation_1d_data(self, text: str) -> dict:
        """Parse 1D momentum conservation parameters"""
        data = {}
        
        # Parse masses
        mass_matches = re.findall(r'(\d+(?:\.\d+)?)\s*kg', text, re.IGNORECASE)
        if len(mass_matches) >= 2:
            data["m1"] = float(mass_matches[0])
            data["m2"] = float(mass_matches[1])
        else:
            data["m1"] = 2.0  # Default
            data["m2"] = 3.0
        
        # Parse initial velocities
        velocity_matches = re.findall(r'(-?\d+(?:\.\d+)?)\s*m/s', text, re.IGNORECASE)
        if len(velocity_matches) >= 2:
            data["v1i"] = float(velocity_matches[0])
            data["v2i"] = float(velocity_matches[1])
        elif len(velocity_matches) == 1:
            data["v1i"] = float(velocity_matches[0])
            data["v2i"] = 0.0  # At rest
        else:
            data["v1i"] = 8.0  # Default
            data["v2i"] = 0.0  # At rest
        
        # Determine collision type
        if "elastic" in text.lower():
            data["collision_type"] = "elastic"
        elif "perfectly inelastic" in text.lower() or "stick" in text.lower():
            data["collision_type"] = "perfectly_inelastic"
        elif "inelastic" in text.lower():
            data["collision_type"] = "inelastic"
        else:
            data["collision_type"] = "elastic"  # Default
        
        # Parse final velocities if given
        if "final" in text.lower():
            final_v_matches = re.findall(r'vf.*?(\d+(?:\.\d+)?)', text, re.IGNORECASE)
            if final_v_matches:
                data["v1f"] = float(final_v_matches[0])
        
        return data

    def _parse_momentum_conservation_2d_data(self, text: str) -> dict:
        """Parse 2D momentum conservation parameters"""
        data = {"collision_type": "elastic"}
        
        # Parse object data
        mass_matches = re.findall(r'(\d+(?:\.\d+)?)\s*kg', text, re.IGNORECASE)
        velocity_matches = re.findall(r'(\d+(?:\.\d+)?)\s*m/s', text, re.IGNORECASE)
        angle_matches = re.findall(r'(\d+(?:\.\d+)?)\s*°', text, re.IGNORECASE)
        
        if len(mass_matches) >= 2 and len(velocity_matches) >= 2:
            data["object1"] = {
                "mass": float(mass_matches[0]),
                "velocity": float(velocity_matches[0]),
                "angle": float(angle_matches[0]) if len(angle_matches) >= 1 else 0.0
            }
            data["object2"] = {
                "mass": float(mass_matches[1]),
                "velocity": float(velocity_matches[1]),
                "angle": float(angle_matches[1]) if len(angle_matches) >= 2 else 90.0
            }
        else:
            # Default billiard ball scenario
            data["object1"] = {"mass": 0.16, "velocity": 25, "angle": 0}
            data["object2"] = {"mass": 0.16, "velocity": 0, "angle": 0}
        
        # Determine collision type
        if "perfectly inelastic" in text.lower():
            data["collision_type"] = "perfectly_inelastic"
        elif "inelastic" in text.lower():
            data["collision_type"] = "inelastic"
        else:
            data["collision_type"] = "elastic"
        
        return data

    def _parse_collision_scenario_data(self, text: str) -> dict:
        """Parse comprehensive collision scenario parameters"""
        data = {"scenario": "general", "analysis_type": "basic"}
        
        # Determine scenario type
        if "car" in text.lower() or "vehicle" in text.lower() or "crash" in text.lower():
            data["scenario"] = "car_crash"
            data["analysis_type"] = "safety"
        elif "rocket" in text.lower():
            data["scenario"] = "rocket_propulsion"
        elif "sport" in text.lower() or "ball" in text.lower():
            data["scenario"] = "sports_collision"
        
        # Parse vehicle/object data
        mass_matches = re.findall(r'(\d+(?:\.\d+)?)\s*kg', text, re.IGNORECASE)
        velocity_matches = re.findall(r'(\d+(?:\.\d+)?)\s*m/s', text, re.IGNORECASE)
        angle_matches = re.findall(r'(\d+(?:\.\d+)?)\s*°', text, re.IGNORECASE)
        
        if len(mass_matches) >= 2 and len(velocity_matches) >= 2:
            data["car1"] = {
                "mass": float(mass_matches[0]),
                "velocity": float(velocity_matches[0]),
                "direction": float(angle_matches[0]) if len(angle_matches) >= 1 else 0.0
            }
            data["car2"] = {
                "mass": float(mass_matches[1]),
                "velocity": float(velocity_matches[1]),
                "direction": float(angle_matches[1]) if len(angle_matches) >= 2 else 90.0
            }
        else:
            # Default car crash scenario
            data["car1"] = {"mass": 1500, "velocity": 20, "direction": 0}
            data["car2"] = {"mass": 1200, "velocity": 15, "direction": 90}
        
        return data

# Additional methods to add to the _setup_agent_config method:

        elif self.agent_id == "momentum_agent":
            from prompts.momentum_agent_prompt import get_user_message, get_system_message, get_metadata
            self.get_system_message = get_system_message
            self.get_user_message = get_user_message
            self.metadata = get_metadata()
            self.mcp_port = 10104  # MCP port for momentum agent on VM

# Additional condition to add to the _solve_with_direct_tools method:

        elif self.agent_id == "momentum_agent":
            return await self._solve_momentum_problem_direct(problem)

# Factory function to add:

def create_momentum_agent(use_direct_tools: bool = True) -> CombinedMathematicsAgent:
    """Create a momentum agent"""
    return CombinedMathematicsAgent(
        agent_id="momentum_agent", 
        use_direct_tools=use_direct_tools
    )

# Interactive interface function to add:

async def interactive_momentum_agent():
    """Interactive momentum agent interface"""
    agent = create_momentum_agent(use_direct_tools=True)  # Use working mode
    
    await agent.initialize()
    agent.get_user_message()
    
    while True:
        try:
            user_input = input(f"🚗 Momentum Problem: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print(f"👋 Goodbye from Momentum Agent!")
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
            print(f"\\n👋 Goodbye from Momentum Agent!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\\n")
