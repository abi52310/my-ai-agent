class Planner:

    #This is just wrapper around LLM.

    #Planner does NOT talk to API directly.
    #It uses your shared LLM client.

    def __init__(self, llm_client):
        self.llm = llm_client

    def create_plan(self, user_input):

        #Control #1 — Role Isolation
        #You are an AI planning engine.
        #Prevents assistant style responses.

        #Control #2 — Tool Prohibition
        #Do NOT call tools
        #Do NOT simulate tool output
        #Prevents fake tool syntax.

        #Control #3 — Output Contract
        #Output format EXACTLY:


        planning_prompt = f"""
            You are an AI planning engine.

            Your job:
            Create a tool execution plan to solve the user request.

            Rules:
            - Do NOT call tools
            - Do NOT simulate tool output
            - Only output steps
            - Use tool names exactly
            - If multi-step math → break into steps

            Available tools:
            - multiply(a,b)
            - calculate_sum(a,b)

            User request:
            {user_input}

            Output format EXACTLY:

            PLAN:
            1. tool_name(arg1,arg2)
            2. tool_name(result,arg2)
            """

        messages = [
            {"role": "system", "content": "You are planning engine. No tools allowed."},
            {"role": "user", "content": planning_prompt}
        ]

        message = self.llm.generate(messages, tools=None)

        return message.content
