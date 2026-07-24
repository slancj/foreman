from langchain_core.messages import HumanMessage
from foreman.graph import app


def main():
    print("--- Starting Foreman Wordle Demo ---")
    
    # Message 1: Ask the agent to start a game and guess 'CRANE'
    print("\n[User]: Start a Wordle game and make your first guess 'CRANE'.")
    result = app.invoke(
        {"messages": [HumanMessage(content="Start a Wordle game and make your first guess 'CRANE'.")]}
    )
    
    # Print agent conversation responses
    for msg in result["messages"]:
        if msg.type == "ai" and msg.content:
            print(f"\n[Foreman]: {msg.content}")


if __name__ == "__main__":
    main()
