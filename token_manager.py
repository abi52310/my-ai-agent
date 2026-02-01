import tiktoken
from debug_logger import debug_log

class TokenManager:

    def __init__(self, max_tokens=6000):
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.max_tokens = max_tokens

    def count_tokens(self, text):
        return len(self.encoding.encode(text))

    def total_tokens(self, messages):
        total = 0
        for msg in messages:
            total += self.count_tokens(msg["content"])
        return total

    def trim_memory(self, conversation_history):
        debug_log("TOKEN", "Checking token limits")
        while self.total_tokens(conversation_history) > self.max_tokens:
            # keep system message, remove oldest conversation
            debug_log("TOKEN", "Trimming old memory")
            if len(conversation_history) > 2:
                conversation_history.pop(1)
            else:
                break
