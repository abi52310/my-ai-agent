from token_manager import TokenManager
from memory_manager import MemoryManager
from llm_client import LLMClient
from tool_router import ToolRouter
from tool_registry import ToolRegistry
MAX_TOOL_ITERATIONS = 5

token_manager = TokenManager(max_tokens=6000)
memory_manager = MemoryManager()
llm_client = LLMClient()

tool_registry = ToolRegistry()
tool_router = ToolRouter(tool_registry)


# ============================================================
# 📌 ask_agent() RUNTIME FLOW — STEP BY STEP EXAMPLE
#
# Example User Input:
#   "Add 45 and 67"
#
# ------------------------------------------------------------
# STEP 0 — Initial Memory State
#
# history = [
#   { role: "system", content: "You are helpful AI assistant..." }
# ]
#
# ------------------------------------------------------------
# STEP 1 — User Message Added
#
# memory_manager.add_user_message("Add 45 and 67")
#
# history becomes:
# [
#   system: You are helpful AI assistant...
#   user: Add 45 and 67
# ]
#
# ------------------------------------------------------------
# STEP 2 — First LLM Call
#
# message = llm_client.generate(history, tools=tool_schemas)
#
# LLM internally decides:
#   "Math problem → Use calculate_sum tool"
#
# LLM RETURNS (NOT TEXT):
#
# message.tool_calls = [
#   {
#     function.name = "calculate_sum"
#     function.arguments = {"a": 45, "b": 67}
#   }
# ]
#
# message.content = None
#
# IMPORTANT:
# LLM is NOT answering user yet.
# LLM is asking system to execute tool first.
#
# ------------------------------------------------------------
# STEP 3 — Tool Execution (Outside LLM)
#
# tool_router.execute_tool()
#
# Python runs:
#   calculate_sum(45, 67)
#
# Tool Result:
#   112
# Example tool_router return format:
#
# SUCCESS CASE:
# {
#   "success": True,
#   "tool_name": "calculate_sum",
#   "result": 112
# }
#
# ERROR CASE:
# {
#   "success": False,
#   "tool_name": "calculate_sum",
#   "error": "Invalid arguments"
# }
#
# ------------------------------------------------------------
# STEP 4 — Tool Result Added Back To Conversation (CRITICAL)
#
# We MUST add tool result as role="tool", NOT assistant.
#
# history.append({
#   role: "tool",
#   name: "calculate_sum",
#   content: "112"
# })
#
# history becomes:
# [
#   system: ...
#   user: Add 45 and 67
#   assistant: (tool call request)
#   tool: 112
# ]
#
# ------------------------------------------------------------
# STEP 5 — Second LLM Call
#
# Now LLM sees:
#   User question
#   Tool was called
#   Tool returned result = 112
#
# LLM now generates FINAL answer:
#
# message.content =
#   "The sum of 45 and 67 is 112."
#
# message.tool_calls = None
#
# ------------------------------------------------------------
# STEP 6 — Final Answer Returned To User
#
# memory_manager.add_assistant_message(final_answer)
#
# Final history:
# [
#   system
#   user: Add 45 and 67
#   assistant: tool call calculate_sum
#   tool: 112
#   assistant: Final answer text
# ]
#
# ------------------------------------------------------------
# 🚨 IMPORTANT RULES
#
# ❌ NEVER add tool result as assistant message
# ✔ ALWAYS add tool result as role="tool"
#
# If wrong → LLM may:
#   - Call tool repeatedly
#   - Generate invalid tool syntax
#   - Cause API errors (tool_use_failed)
#
# ------------------------------------------------------------
# 🧠 MENTAL MODEL
#
# LLM = Planner / Thinker
# Tool = External Execution Engine
#
# Flow:
# User → LLM → Tool → LLM → Final Answer → User
#
# ============================================================


def ask_agent(user_input):

    memory_manager.add_user_message(user_input)

    iteration = 0
    last_tool_result = None

    while iteration < MAX_TOOL_ITERATIONS:

        history = memory_manager.get_history()
        token_manager.trim_memory(history)

        print("[DEBUG][LLM] Sending request to LLM")

        message = llm_client.generate(
            history,
            tools=tool_registry.list_tool_schemas()
        )

        # 🚨 Guard: If model tries text tool syntax, ignore and retry
        if message.content and any(x in message.content for x in [
            "<function=",
            "<multiply",
            "<calculate_sum",
            "</multiply>",
            "</calculate_sum>"
        ]):
            print("[DEBUG] Model attempted text tool call. Retrying...")
            iteration += 1
            continue

        # =================================================
        # TOOL CALL CASE
        # =================================================
        if message.tool_calls:

            tool_call = message.tool_calls[0]

            print(f"[DEBUG][TOOL] Executing tool: {tool_call.function.name}")

            tool_result = tool_router.execute_tool(tool_call)
            last_tool_result = tool_result

            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(
                    tool_result["result"]
                    if tool_result["success"]
                    else tool_result["error"]
                )
            })

            iteration += 1
            continue

        # =================================================
        # FINAL ANSWER CASE
        # =================================================
        reply = message.content

        if reply:
            memory_manager.add_assistant_message(reply)
            return reply

        iteration += 1

    # =====================================================
    # LOOP SAFETY FALLBACK (ONLY ONE BLOCK NEEDED)
    # =====================================================
    if last_tool_result:
        if last_tool_result["success"]:
            return f"The result is {last_tool_result['result']}"
        else:
            return f"Tool failed: {last_tool_result['error']}"

    return "I reached tool execution limit. Please refine your request."




def main():
    print("🤖 Real Tool Layer Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        reply = ask_agent(user_input)
        print("\nAgent:", reply, "\n")


if __name__ == "__main__":
    main()
