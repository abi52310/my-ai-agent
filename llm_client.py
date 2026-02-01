import os
from groq import Groq
from dotenv import load_dotenv
from debug_logger import debug_log

load_dotenv()


class LLMClient:

    def __init__(self):
        self.provider = "groq"
        self.model = "llama-3.1-8b-instant"

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(self, messages, tools=None):
        debug_log("LLM", "Sending request to LLM")

        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            tools=tools,
            tool_choice="auto"
        )

        return response.choices[0].message
