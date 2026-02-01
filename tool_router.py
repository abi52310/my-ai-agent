import json
from debug_logger import debug_log


class ToolRouter:
   

    def __init__(self, tool_registry):
        self.tool_registry = tool_registry

    def execute_tool_direct(self, tool_name, args):

        tool = self.tool_registry.get_tool(tool_name)

        if not tool:
            return {
                "success": False,
                "tool_name": tool_name,
                "error": f"Tool {tool_name} not found"
            }

        try:
            result = tool["function"](*args)

            return {
                "success": True,
                "tool_name": tool_name,
                "result": result
            }

        except Exception as e:
            return {
                "success": False,
                "tool_name": tool_name,
                "error": str(e)
            }


    def execute_tool(self, tool_call):

        try:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            debug_log("TOOL", f"Executing tool: {tool_name}")

            tool_entry = self.tool_registry.get_tool(tool_name)

            if not tool_entry:
                return {
                    "success": False,
                    "error": f"Tool {tool_name} not found"
                }

            tool_function = tool_entry["function"]

            result = tool_function(**arguments)

            return {
                "success": True,
                "tool_name": tool_name,
                "result": result
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
