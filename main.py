import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add]

def llm_node(state: State):
    llm = ChatOpenAI(
        model="gemini/gemini-3.5-flash-lite",
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("UPSTREAM_API_URL"),
    )
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Define the graph at top level for LangGraph dashboard
graph = StateGraph(State)
graph.add_node("llm", llm_node)
graph.add_edge(START, "llm")
graph.add_edge("llm", END)

app = graph.compile()


def main():
    result = app.invoke({"messages": ["Hello! What is the capital of Paris"]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
