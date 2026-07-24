from langgraph.graph import StateGraph, START, END
from foreman.state import State
from foreman.nodes import llm_node

# Define the graph at top level for LangGraph dashboard
graph = StateGraph(State)
graph.add_node("llm", llm_node)
graph.add_edge(START, "llm")
graph.add_edge("llm", END)

app = graph.compile()
