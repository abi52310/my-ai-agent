class PlannerV3:

    def __init__(self, llm_client):
        self.llm = llm_client

    def create_multiple_plans(self, user_input, num_plans=2):
        planning_prompt = f"""
        You are an AI planning engine.

        Create {num_plans} DIFFERENT execution plans.

        EXECUTION DSL CONTRACT:

        Allowed function names:
        - calculate_sum
        - multiply

        Allowed arguments:
        - numbers
        - result keyword only

        STRICTLY FORBIDDEN:
        - word "tool"
        - placeholders like a,b,x,y
        - variables like previous_result
        - function names not listed

        Available tools:
        - calculate_sum(a,b)
        - multiply(a,b)

        User request:
        {user_input}

        STRICT OUTPUT RULES:
        - NEVER use word "tool"
        - ONLY use calculate_sum or multiply
        - ALWAYS use real numbers
        - Multi step math → break into steps

        Output format EXACTLY:

        PLAN OPTION 1:
        PLAN:
        1. calculate_sum(number,number) OR multiply(number,number)
        2. calculate_sum(result,number) OR multiply(result,number)

        PLAN OPTION 2:
        PLAN:
        1. calculate_sum(number,number) OR multiply(number,number)
        2. calculate_sum(result,number) OR multiply(result,number)
        """

        messages = [
            {"role": "system", "content": "You are planning engine. Output only plans."},
            {"role": "user", "content": planning_prompt}
        ]

        message = self.llm.generate(messages, tools=None)

        return message.content
