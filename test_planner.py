from planner import Planner
from llm_client import LLMClient


def test(input_text):

    print("\n==============================")
    print("INPUT:", input_text)

    llm = LLMClient()
    planner = Planner(llm)

    plan = planner.create_plan(input_text)

    print("\nPLAN OUTPUT:")
    print(plan)
    print("==============================")


if __name__ == "__main__":

    print("🚀 TEST PLANNER STARTED")

    test("(2 + 3) * 10")
