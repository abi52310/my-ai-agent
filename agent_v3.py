from planner_v3 import PlannerV3
from plan_parser_v3 import PlanParserV3
from executor import Executor
from responder import Responder
from reflection import Reflection

from tool_registry import ToolRegistry
from tool_router import ToolRouter
from llm_client import LLMClient


class AgentV3:

    def __init__(self):

        llm_client = LLMClient()

        self.planner = PlannerV3(llm_client)
        self.parser = PlanParserV3()

        tool_registry = ToolRegistry()
        tool_router = ToolRouter(tool_registry)

        self.executor = Executor(tool_router)
        self.reflection = Reflection()
        self.responder = Responder()

    def run(self, user_query):

        print("\n[AGENT V3] Generating Multiple Plans...")

        multi_plan_text = self.planner.create_multiple_plans(user_query)

        print("\n[MULTI PLAN RAW]")
        print(multi_plan_text)

        plans = self.parser.extract_plans(multi_plan_text)

        best_result = None

        for i, plan in enumerate(plans):

            print(f"\n[EXECUTING PLAN {i+1}]")

            results, final_result = self.executor.execute_plan(plan)

            decision = self.reflection.evaluate(
                user_query,
                plan,
                final_result
            )

            print(f"[REFLECTION PLAN {i+1}] → {decision}")

            if "PASS" in decision.upper():
                best_result = final_result
                break

        if best_result is None:
            return "No reliable plan found."

        return self.responder.generate_response(user_query, best_result)


if __name__ == "__main__":

    agent = AgentV3()

    print("🤖 Agent V3 Ready (Multi Plan Mode)\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        reply = agent.run(user_input)

        print("\nAgent:", reply, "\n")
