from langchain_core.messages import HumanMessage
from foreman.graph import app


def main():
    result = app.invoke({"messages": [HumanMessage(content="Hello! What is the capital of France?")]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
