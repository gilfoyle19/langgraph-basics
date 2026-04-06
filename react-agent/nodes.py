from dotenv import load_dotenv
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from react import llm, tools

load_dotenv()

#Define a system prompt
SYSTEM_PROMPT = """You are a helpful assistant that can use tools to answer questions."""

#create the reasoning node
def run_agent_reasoning(state: MessagesState) -> MessagesState:
    response = llm.invoke([{"role": "system", "content": SYSTEM_PROMPT}] + state["messages"]) 
    return {"messages": [response]}

tn= ToolNode(tools)