from foreman.state import State
from foreman.llm import llm


def llm_node(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
