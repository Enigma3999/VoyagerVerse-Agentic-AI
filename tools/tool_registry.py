import logging
import importlib
from typing import Dict, List, Any, Optional, Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tool_registry")

class ToolRegistry:
    """Registry for all external API tools that the agentic AI can use.
    
    This class manages the registration, discovery, and execution of tools
    that connect to external APIs for weather, mapping, bookings, etc.
    """
    
    def __init__(self):
        self.tools = {}
        self.tool_metadata = {}
        self.tool_categories = {
            "weather": [],
            "mapping": [],
            "accommodation": [],
            "transportation": [],
            "attractions": [],
            "dining": [],
            "events": [],
            "local_info": []
        }
    
    def register_tool(self, tool_name: str, tool_function: Callable, 
                     category: str, description: str, 
                     required_params: List[str], optional_params: List[str] = None):
        """Register a new tool with the registry."""
        if tool_name in self.tools:
            logger.warning(f"Tool {tool_name} already registered. Overwriting.")
        
        self.tools[tool_name] = tool_function
        
        self.tool_metadata[tool_name] = {
            "name": tool_name,
            "category": category,
            "description": description,
            "required_params": required_params,
            "optional_params": optional_params or [],
            "usage_count": 0,
            "success_rate": 1.0,  # Start optimistic
            "average_latency": 0.0
        }
        
        if category in self.tool_categories:
            self.tool_categories[category].append(tool_name)
        else:
            logger.warning(f"Unknown category {category}. Tool registered but not categorized.")
        
        logger.info(f"Registered tool: {tool_name} in category {category}")
    
    def get_tool(self, tool_name: str) -> Optional[Callable]:
        """Get a tool by name."""
        return self.tools.get(tool_name)
    
    def get_tool_metadata(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific tool."""
        return self.tool_metadata.get(tool_name)
    
    def get_tools_by_category(self, category: str) -> List[str]:
        """Get all tools in a specific category."""
        return self.tool_categories.get(category, [])
    
    def get_all_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered tools and their metadata."""
        return self.tool_metadata
    
    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with the given parameters."""
        import time
        
        tool = self.get_tool(tool_name)
        if not tool:
            return {"status": "error", "message": f"Tool {tool_name} not found"}
        
        # Check required parameters
        metadata = self.get_tool_metadata(tool_name)
        missing_params = []
        for param in metadata["required_params"]:
            if param not in params:
                missing_params.append(param)
        
        if missing_params:
            return {
                "status": "error", 
                "message": f"Missing required parameters: {', '.join(missing_params)}"
            }
        
        # Execute the tool and measure performance
        start_time = time.time()
        try:
            result = tool(**params)
            success = True
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            result = {"status": "error", "message": str(e)}
            success = False
        
        end_time = time.time()
        latency = end_time - start_time
        
        # Update tool metadata
        self.tool_metadata[tool_name]["usage_count"] += 1
        
        # Update success rate as a moving average
        current_success_rate = self.tool_metadata[tool_name]["success_rate"]
        usage_count = self.tool_metadata[tool_name]["usage_count"]
        new_success_rate = ((current_success_rate * (usage_count - 1)) + (1.0 if success else 0.0)) / usage_count
        self.tool_metadata[tool_name]["success_rate"] = new_success_rate
        
        # Update average latency as a moving average
        current_latency = self.tool_metadata[tool_name]["average_latency"]
        new_latency = ((current_latency * (usage_count - 1)) + latency) / usage_count
        self.tool_metadata[tool_name]["average_latency"] = new_latency
        
        logger.info(f"Executed tool {tool_name} in {latency:.2f}s with status: {'success' if success else 'error'}")
        
        return result
    
    def get_best_tool_for_task(self, category: str, context: Dict[str, Any]) -> Optional[str]:
        """Intelligently select the best tool for a given task based on context."""
        tools_in_category = self.get_tools_by_category(category)
        if not tools_in_category:
            return None
        
        # Simple selection strategy: pick the tool with highest success rate
        best_tool = None
        best_score = -1
        
        for tool_name in tools_in_category:
            metadata = self.get_tool_metadata(tool_name)
            # Calculate a score based on success rate and latency
            success_weight = 0.8
            latency_weight = 0.2
            
            # Normalize latency: lower is better, cap at 5 seconds
            latency_score = max(0, 1 - (metadata["average_latency"] / 5.0))
            
            score = (metadata["success_rate"] * success_weight) + (latency_score * latency_weight)
            
            if score > best_score:
                best_score = score
                best_tool = tool_name
        
        return best_tool

# Create a global instance of the tool registry
tool_registry = ToolRegistry()

def load_all_tools():
    """Load and register all available tools."""
    # Import all tool modules
    from tools import weather_tools
    from tools import mapping_tools
    from tools import booking_tools
    from tools import attraction_tools
    from tools import dining_tools
    from tools import transportation_tools
    from tools import event_tools
    
    # Each module should register its tools with the registry
    logger.info(f"Loaded {len(tool_registry.tools)} tools across {len(tool_registry.tool_categories)} categories")
