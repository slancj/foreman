from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from foreman.state import State
from foreman.nodes import llm_node
from foreman.plugins import all_plugin_tools

# Define the graph at top level for LangGraph dashboard
graph = StateGraph(State)

# Add nodes
graph.add_node("llm", llm_node)
graph.add_node("tools", ToolNode(all_plugin_tools))

# Add edges
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", tools_condition)
graph.add_edge("tools", "llm")

app = graph.compile()
