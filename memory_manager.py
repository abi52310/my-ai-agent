from debug_logger import debug_log
class MemoryManager:

    def __init__(self):
        self.conversation_history = [
            {
                "role": "system",
                "content": """
                You are a helpful AI assistant with access to external tools.

                GENERAL RULES:
                - Use tools when needed.
                - Do not guess tool results.
                - Tool results are always correct.

                CRITICAL TOOL EXECUTION RULES:

                You MUST follow these rules strictly.

                1. NEVER output text like:
                <function=tool_name>{}</function>

                2. NEVER simulate tool calls in text.

                3. ONLY use structured tool calling via tool_calls.

                4. If you output text tool syntax, it is a system error.

                5. When tools are available:
                - Decide tool
                - Call tool using tool_calls
                - Wait for tool result
                - Then produce final answer

                6. If tool result exists:
                STOP calling tools
                Produce final answer only

                MATH TOOL RULES:

                1. Follow order of operations (BODMAS).
                2. Use multiply tool for multiplication.
                3. Use calculate_sum tool for addition.
                4. Use previous tool result as input to next step.

                FINAL RESPONSE RULE:
                After tools finish, respond ONLY with final answer.
                Do not explain tool usage steps unless user asks.
                """
            }
        ]

    def add_user_message(self, message):
        
        self.conversation_history.append(
            {"role": "user", "content": message}
        )

    def add_assistant_message(self, message):
        self.conversation_history.append(
            {"role": "assistant", "content": message}
        )

    def get_history(self):
        return self.conversation_history