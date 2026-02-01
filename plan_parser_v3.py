import re


class PlanParserV3:

    def extract_plans(self, multi_plan_text):

        plans = re.findall(
            r"PLAN OPTION \d+:\s*(PLAN:\s*.*?)(?=PLAN OPTION|\Z)",
            multi_plan_text,
            re.DOTALL
        )

        return [p.strip() for p in plans]
