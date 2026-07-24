from foreman.state import State
from foreman.llm import llm
from foreman.plugins import all_plugin_tools

# Bind plugin tools to the LLM
llm_with_tools = llm.bind_tools(all_plugin_tools)


def llm_node(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}
