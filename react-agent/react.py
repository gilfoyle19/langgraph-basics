from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

load_dotenv()

@tool
def triple(num:float) -> float:
    """Returns the triple of a number."""
    return float(num) * 3

# Define the tools to be used by the agent
tools = [triple, TavilySearch(max_results=1)]

#Initialize the llm
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0).bind_tools(tools)
