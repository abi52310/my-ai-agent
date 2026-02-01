from debug_logger import debug_log
class MemoryManager:

    def __init__(self):
        self.conversation_history = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant with memory. "
                    "You must use conversation history."
                )
            }
        ]

    def add_user_message(self, message):
        debug_log("MEMORY", f"Adding user message: {message}")
        self.conversation_history.append(
            {"role": "user", "content": message}
        )

    def add_assistant_message(self, message):
        self.conversation_history.append(
            {"role": "assistant", "content": message}
        )

    def get_history(self):
        return self.conversation_history