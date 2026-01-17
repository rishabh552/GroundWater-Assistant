"""
Jal-Rakshak Agent Controller
Manages the Thinking -> Action -> Observation Loop
"""
import re
import json
import ast
import os
from backend.tools import AVAILABLE_TOOLS
from backend.llm import generate_response
from backend.prompts import AGENT_SYSTEM_PROMPT

# Get the project root directory for data files
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Agency:
    def __init__(self, llm_tuple, retriever):
        self.llm = llm_tuple
        self.retriever = retriever
        self.max_steps = 3  # Reduced for faster responses (most queries need 1-2 calls)
        self._load_district_risks()
    
    def _load_district_risks(self):
        """Load known district risk data from generated_map_data.json."""
        try:
            map_data_path = os.path.join(PROJECT_ROOT, "generated_map_data.json")
            with open(map_data_path, "r") as f:
                self.district_risks = json.load(f)
        except Exception:
            self.district_risks = {}
    
    def _get_district_risk(self, query):
        """Check if query mentions a known district and return its risk level."""
        query_lower = query.lower()
        for district, data in self.district_risks.items():
            if district.lower() in query_lower:
                risk = data.get("risk", "Unknown")
                if risk == "Over-Exploited":
                    return f"⚠️ **WARNING: {district} is classified as OVER-EXPLOITED** (extraction > 100%). Groundwater is being used faster than it can recharge. Drilling borewells here is NOT recommended without special permits."
                elif risk == "Critical":
                    return f"🟠 **CAUTION: {district} is classified as CRITICAL** (extraction 90-100%). Water availability is severely stressed. Consider water conservation measures."
                elif risk == "Semi-Critical":
                    return f"🟡 **MODERATE RISK: {district} is classified as SEMI-CRITICAL** (extraction 70-90%). Monitor usage carefully and implement rainwater harvesting."
                elif risk == "Safe":
                    return f"🟢 **{district} is classified as SAFE** (extraction < 70%). Groundwater levels are sustainable for now."
                else:
                    return f"ℹ️ {district} risk level: {risk}"
        return None
        
    def _parse_action(self, llm_output):
        """
        Parse the LLM response to find specific Tool Actions.
        Looking for: Action: tool_name(arg1, arg2)
        """
        # Regex to capture "Action: tool_name(args)"
        action_pattern = r"Action:\s*(\w+)\((.*)\)"
        match = re.search(action_pattern, llm_output)
        
        if match:
            tool_name = match.group(1)
            tool_args = match.group(2)
            return tool_name, tool_args
        return None, None

    def _execute_tool(self, tool_name, tool_args_str):
        """Execute the python function for the tool."""
        if tool_name == "search_knowledge_base":
            # Special case for RAG which needs the retriever
            # Remove quotes if present
            query = tool_args_str.strip('"\'')
            
            # First, check if we have known district risk data
            district_risk_info = self._get_district_risk(query)
            
            results = self.retriever.search(query)
            
            if not results:
                if district_risk_info:
                    return district_risk_info
                return f"NO DATA FOUND: '{query}' is not in our documents. Try a nearby district name instead."
            
            # Check result quality - FAISS L2 distance: lower is better
            # If best match has score > 0.8, the query term likely doesn't exist
            best_score = results[0][1] if results else 1.0
            if best_score > 0.8:
                if district_risk_info:
                    return district_risk_info
                return f"NO DIRECT DATA for '{query}'. The closest match has low relevance. Suggest checking the district name (e.g., Pudukkottai, Chennai, Salem) or use the nearest major city."
            
            # Prepend known district risk to RAG results
            context = self.retriever.format_context(results)
            if district_risk_info:
                context = f"**KNOWN DISTRICT RISK**: {district_risk_info}\n\n**ADDITIONAL CONTEXT FROM DOCUMENTS**:\n{context}"
            
            return context
            
        elif tool_name in AVAILABLE_TOOLS:
            try:
                # Use safe literal_eval instead of eval for security
                func = AVAILABLE_TOOLS[tool_name]
                # Parse arguments to python types (int, float, str)
                # This handles "500" -> 500, "'paddy'" -> 'paddy'
                args = ast.literal_eval(f"({tool_args_str})")
                
                # Handle single argument vs tuple
                if not isinstance(args, tuple):
                    args = (args,)
                    
                return func(*args)
            except Exception as e:
                return f"Error executing tool: {str(e)}"
        
        return f"Unknown tool: {tool_name}"

    def run(self, user_query):
        """
        Run the ReAct loop.
        """
        # Initial Context
        history = f"User: {user_query}\n"
        
        # Track executed actions to detect loops
        executed_actions = []
        
        # Yield status updates for the UI
        yield {"status": "thinking", "content": "Analyzing request..."}
        
        for i in range(self.max_steps):
            # 1. Think
            prompt = history + "Thought:"
            response = generate_response(self.llm, prompt, system_prompt=AGENT_SYSTEM_PROMPT)
            
            # Clean up response to avoid repetition
            if "Observation:" in response:
                response = response.split("Observation:")[0]
            
            thought = response.strip()
            history += f"Thought: {thought}\n"
            
            # Yield thought for UI
            yield {"status": "thought", "content": thought}
            
            # 2. Check for Action
            tool_name, tool_args = self._parse_action(thought)
            
            if tool_name:
                # LOOP DETECTION: Check if we are repeating the exact same action
                # Normalize args for comparison (handle quote variations)
                args_normalized = tool_args.strip().replace("'", '"').lower()
                current_action = (tool_name.lower(), args_normalized)
                
                # Check if this exact action was already executed
                is_loop = current_action in executed_actions

                if is_loop:
                    observation = "SYSTEM: You just ran this action. STOP. Do NOT try to 'recall' or use new tools. You generally already have the information. write 'Final Answer: [Your Answer]' now."
                    yield {"status": "observation", "content": "Loop Detected - Forcing Final Answer"}
                else:
                    # Record this action to prevent loops
                    executed_actions.append(current_action)
                    
                    # Yield action for UI
                    yield {"status": "action", "content": f"Running {tool_name}({tool_args})..."}
                    
                    # 3. Act
                    observation = self._execute_tool(tool_name, tool_args)
                
                # 4. Observe
                # Include full observation in history so LLM can see all RAG context
                history += f"Observation: {observation}\n"
                # Show truncated version to user for UI
                observation_preview = str(observation)[:500] + ("..." if len(str(observation)) > 500 else "")
                yield {"status": "observation", "content": observation_preview}
                
            else:
                # No action means we have the final answer or asking for clarification
                if "Final Answer:" in thought:
                    final_ans = thought.split("Final Answer:")[1].strip()
                    yield {"status": "final", "content": final_ans}
                    return
                else:
                    # Model just talked without calling tool (or failed pattern)
                    # Treat entire thing as response
                    yield {"status": "final", "content": thought}
                    return
                    
        yield {"status": "final", "content": "Detailed analysis timed out. based on what I found: " + history[-500:]}
