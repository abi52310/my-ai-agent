from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


class Responder:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def generate_response(self, user_query, final_result):

        prompt = f"""
            You are a response formatter for an AI system.

            You will receive:
            1. User question
            2. Final computed result

            Your job:
            Return ONLY a short final answer sentence.

            STRICT RULES:
            - Maximum 1 sentence
            - Do NOT explain steps
            - Do NOT explain math
            - Do NOT mention tools
            - Do NOT add extra commentary
            - Must include the final result

            User Question:
            {user_query}

            Final Result:
            {final_result}

            Return final answer now:
            """

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content



    