from executor import Executor
from tool_registry import ToolRegistry
from tool_router import ToolRouter


def test(plan_text):

    print("\n==============================")
    print("PLAN INPUT:\n", plan_text)

    tool_registry = ToolRegistry()
    tool_router = ToolRouter(tool_registry)

    executor = Executor(tool_router)

    results, final_result = executor.execute_plan(plan_text)

    print("\nSTEP RESULTS:")
    for step_no, r in enumerate(results, start=1):
        print(f"Step {step_no} → {r}")

    print("\nFINAL RESULT:", final_result)
    print("==============================")


if __name__ == "__main__":

    print("🚀 EXECUTOR TEST STARTED")

    # =====================================
    # TEST CASE 1 — Bracket then Multiply
    # Expected → 50
    # =====================================
    test("""
PLAN:
1. calculate_sum(2,3)
2. multiply(result,10)
""")

    # =====================================
    # TEST CASE 2 — Multiply then Add
    # Expected → 11
    # =====================================
    test("""
PLAN:
1. multiply(2,3)
2. calculate_sum(result,5)
""")

    # =====================================
    # TEST CASE 3 — Single Step
    # Expected → 112
    # =====================================
    test("""
PLAN:
1. calculate_sum(45,67)
""")
