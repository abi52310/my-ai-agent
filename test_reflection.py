from reflection import Reflection


if __name__ == "__main__":

    reflection = Reflection()

    user_query = "(2 + 3) * 10"
    plan = """
PLAN:
1. calculate_sum(2,3)
2. multiply(result,10)
"""
    result = 50

    decision = reflection.evaluate(user_query, plan, result)

    print("\nREFLECTION RESULT:", decision)
