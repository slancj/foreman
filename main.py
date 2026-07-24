from langchain_core.messages import HumanMessage
from foreman.graph import app


def main():
    print("--- Starting Foreman Demo ---")
    
    # Message 1: Ask the agent to start Minesweeper
    print("\n[User]: Start a game of minesweeper and play it.")
    result = app.invoke(
        {"messages": [HumanMessage(content="Start a game of minesweeper and play it.")]},
        config={"recursion_limit": 7},
    )
    
    # Print agent conversation responses
    for msg in result["messages"]:
        if msg.type == "ai" and msg.content:
            print(f"\n[Foreman]: {msg.content}")


if __name__ == "__main__":
    main()
