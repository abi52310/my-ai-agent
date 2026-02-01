from planner import Planner
from executor import Executor
from responder import Responder

from tool_registry import ToolRegistry
from tool_router import ToolRouter
from llm_client import LLMClient


class AgentV2:

    def __init__(self):

        # ⭐ Create shared LLM client
        llm_client = LLMClient()

        # ⭐ Inject into planner
        self.planner = Planner(llm_client)

        tool_registry = ToolRegistry()
        tool_router = ToolRouter(tool_registry)

        self.executor = Executor(tool_router)

        self.responder = Responder()

    def run(self, user_query):

        print("\n[AGENT] Planning...")
        plan = self.planner.create_plan(user_query)

        print("\n[PLAN]")
        print(plan)

        print("\n[AGENT] Executing Plan...")
        results, final_result = self.executor.execute_plan(plan)

        print("\n[EXECUTION RESULTS]")
        for r in results:
            print(r)

        print("\n[AGENT] Generating Response...")
        final_answer = self.responder.generate_response(user_query, final_result)

        return final_answer


if __name__ == "__main__":

    agent = AgentV2()

    print("🤖 Agent V2 Ready (type 'exit' to quit)\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        reply = agent.run(user_input)

        print("\nAgent:", reply, "\n")
