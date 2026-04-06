from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, END
from nodes import run_agent_reasoning, tn

load_dotenv()

AGENT_REASON = "agent_reason"
ACT = "act"
LAST = -1

def should_continue(state: MessagesState) -> str:
    """
    Determines whether the agent should continue reasoning or act based on the tool calls in the last message."""
    if not state["messages"][LAST].tool_calls:
        return END
    return ACT

flow = StateGraph(MessagesState)

flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, tn)

flow.add_conditional_edges(AGENT_REASON, should_continue, {ACT:ACT, END:END})
flow.add_edge(ACT, AGENT_REASON)

app = flow.compile()
app.get_graph().draw_mermaid_png(output_file_path="agent_flow.png")

if __name__ == "__main__":
    print("Hello, React Agent!")
    result = app.invoke({"messages": [HumanMessage(content="What is temperature in Germany? List it and triple it")]})
    print(result["messages"][LAST].content)
