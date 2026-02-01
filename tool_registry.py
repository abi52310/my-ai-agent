from tools import calculate_sum, multiply


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "calculate_sum": {
                "function": calculate_sum,
                "description": "Add two numbers"
            },
            "multiply": {
                "function": multiply,
                "description": "Multiply two numbers"
            }
        }

    def get_tool(self, tool_name):
        return self.tools.get(tool_name)

    def list_tool_schemas(self):

        return [
            {
                "type": "function",
                "function": {
                    "name": "calculate_sum",
                    "description": "Add two numbers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"}
                        },
                        "required": ["a", "b"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "multiply",
                    "description": "Multiply two numbers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"}
                        },
                        "required": ["a", "b"]
                    }
                }
            }
        ]
