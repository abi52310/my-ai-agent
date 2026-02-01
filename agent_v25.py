from planner import Planner
from executor import Executor
from responder import Responder
from reflection import Reflection

from tool_registry import ToolRegistry
from tool_router import ToolRouter
from llm_client import LLMClient


MAX_REFLECTION_RETRIES = 2


class AgentV25:

    def __init__(self):

        llm_client = LLMClient()

        self.planner = Planner(llm_client)

        tool_registry = ToolRegistry()
        tool_router = ToolRouter(tool_registry)

        self.executor = Executor(tool_router)

        self.responder = Responder()
        self.reflection = Reflection()

    def run(self, user_query):

        retry_count = 0

        while retry_count <= MAX_REFLECTION_RETRIES:

            print("\n[AGENT] Planning...")
            plan = self.planner.create_plan(user_query)

            print("\n[PLAN]")
            print(plan)

            print("\n[AGENT] Executing Plan...")
            results, final_result = self.executor.execute_plan(plan)

            print("\n[EXECUTION RESULTS]")
            for r in results:
                print(r)

            print("\n[AGENT] Reflecting...")
            decision = self.reflection.evaluate(
                user_query,
                plan,
                final_result
            )

            print("[REFLECTION RESULT]", decision)

            if "PASS" in decision.upper():
                print("\n[AGENT] Generating Response...")
                return self.responder.generate_response(user_query, final_result)

            print("\n[AGENT] Reflection failed. Replanning...")
            retry_count += 1

        return "I could not confidently compute the result. Please rephrase."


if __name__ == "__main__":

    agent = AgentV25()

    print("🤖 Agent V2.5 Ready (Reflection Enabled)\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        reply = agent.run(user_input)

        print("\nAgent:", reply, "\n")
