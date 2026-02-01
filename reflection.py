from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


class Reflection:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def evaluate(self, user_query, plan, execution_result):

        prompt = f"""
You are an AI quality checker.

User Question:
{user_query}

Plan Used:
{plan}

Execution Result:
{execution_result}

Task:
Check if the result logically answers the user question.

Return ONLY one word:
PASS  → if result is correct
FAIL  → if result is wrong
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()
