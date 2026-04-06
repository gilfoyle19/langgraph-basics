from typing import TypedDict, Annotated
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from chains import generate_chain, reflect_chain

class MessageGraph(TypedDict):
    """State for handling messages in the reflection agent."""
    messages: Annotated[list[BaseMessage], add_messages]

REFLECT = "reflect"
GENERATE = "generate"

def generation_node(state: MessageGraph):
    return {"messages": [generate_chain.invoke({"messages": state["messages"]})]} # Generate a new essay based on the current messages

def reflection_node(state: MessageGraph):
    result = reflect_chain.invoke({"messages": state["messages"]}) # Generate critique and recommendations based on the current messages
    return {"messages": [HumanMessage(content=result.content)]}

builder = StateGraph(state_schema=MessageGraph)
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)

def should_continue(state: MessageGraph):
    if len(state["messages"]) > 6:
        return END
    return REFLECT

builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()


if __name__ == "__main__":
    print("Hello LangGraph")
    inputs = {
        "messages": [
            HumanMessage(
                content="""Write a short essay on Ayn Rand's philosophy of Objectivism and its impact on modern literature."""
            )
        ]
    }
    response = graph.invoke(inputs)
    print(response)
