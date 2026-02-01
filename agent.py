from token_manager import TokenManager
from memory_manager import MemoryManager
from llm_client import LLMClient
from tool_router import ToolRouter
from tool_registry import ToolRegistry

token_manager = TokenManager(max_tokens=6000)
memory_manager = MemoryManager()
llm_client = LLMClient()

tool_registry = ToolRegistry()
tool_router = ToolRouter(tool_registry)


def ask_agent(user_input):

    memory_manager.add_user_message(user_input)

    history = memory_manager.get_history()

    token_manager.trim_memory(history)

    message = llm_client.generate(
        history,
        tools=tool_registry.list_tool_schemas()
    )

    # Tool execution
    if message.tool_calls:

        tool_result = tool_router.execute_tool(message.tool_calls[0])

        if tool_result["success"]:
            reply = f"{tool_result['tool_name']} result = {tool_result['result']}"
        else:
            reply = f"Tool error: {tool_result['error']}"

        memory_manager.add_assistant_message(reply)
        return reply

    reply = message.content

    memory_manager.add_assistant_message(reply)

    token_manager.trim_memory(history)

    return reply


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
