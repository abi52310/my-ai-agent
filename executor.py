import re


class Executor:

    def __init__(self, tool_router):
        self.tool_router = tool_router

    def execute_plan(self, plan_text):

        steps = re.findall(r"\d+\.\s*(\w+)\((.*?)\)", plan_text)

        results = []
        last_result = None

        if not steps:
            raise ValueError("No executable steps found in plan")

        for step_num, (tool_name, args_str) in enumerate(steps, start=1):

            args = []

            for arg in args_str.split(","):

                arg = arg.strip()

                if arg.lower() == "result":

                    if last_result is None:
                        raise ValueError(
                            f"Step {step_num} uses result before any tool executed"
                        )

                    args.append(last_result)

                else:
                    args.append(float(arg))

            tool_result = self.tool_router.execute_tool_direct(tool_name, args)

            if not tool_result.get("success", True):
                raise RuntimeError(
                    f"Tool {tool_name} failed: {tool_result.get('error')}"
                )

            last_result = tool_result["result"]
            results.append(tool_result)

        return results, last_result
