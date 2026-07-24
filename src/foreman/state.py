from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class State(TypedDict):
    # add_messages handles message deduplication and updates automatically
    messages: Annotated[list[BaseMessage], add_messages]
