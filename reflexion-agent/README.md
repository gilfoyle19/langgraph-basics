# Reflexion Agent

A sophisticated LangGraph-based research agent that drafts answers, searches for information, and revises based on research findings. Implements the Reflexion pattern from the paper ["Reflexion: Language Agents with Verbal Reinforcement Learning"](https://arxiv.org/abs/2303.11366).

## Overview

The Reflexion Agent demonstrates a research-driven improvement loop:
1. **Draft**: Agent produces an initial 250-word answer to a question
2. **Reflect**: Agent critiques its own answer and identifies what information is missing
3. **Search**: Runs web searches based on identified gaps
4. **Revise**: Updates the answer using new information from search results
5. **Iterate**: Repeats until reaching maximum iterations or satisfactory quality

## Project Structure

```
reflexion-agent/
├── main.py              # Graph orchestration and workflow
├── chains.py            # LLM chains for drafting and revising
├── schemas.py           # Pydantic models for structured outputs
├── tool_executor.py     # Tool execution (web search)
```

### Files

- **`schemas.py`**: Pydantic models defining structured outputs
  - `Reflection`: Captures what's missing and what's superfluous
  - `AnswerQuestion`: Initial answer with reflection and search queries
  - `ReviseAnswer`: Refined answer with citations and references

- **`chains.py`**: LLM chains and prompts
  - `first_responder`: Generates initial answer with reflection
  - `revisor`: Refines answer based on search results
  - Templates with system prompts for structured outputs

- **`tool_executor.py`**: Tool integration
  - `tavily_tool`: Web search via Tavily API
  - `run_queries()`: Executes search queries
  - `execute_tools`: LangGraph tool node for search execution

- **`main.py`**: Graph construction and execution
  - `draft_node()`: Initial answer generation
  - `revise_node()`: Answer refinement
  - `event_loop()`: Iteration control (max 2 iterations)
  - Complete workflow execution

## Requirements

- Python >= 3.11
- Google API key (for Gemini)
- Tavily API key (for web search)

## Installation

1. From the project root, install dependencies:
```bash
pip install -e .
```

2. Set up your `.env` file with:
```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get API keys from:
- [Google AI Studio](https://ai.google.dev/)
- [Tavily Search](https://tavily.com/)

## Usage

Run the reflexion agent:

```bash
cd reflexion-agent
python main.py
```

The agent will research "AI-Powered SOC/Autonomous SOC startups and their funding" by:
1. Drafting an initial answer
2. Searching for relevant information
3. Revising the answer with citations

### Example Workflow

```
Question: "Write about AI-Powered SOC / autonomous soc problem domain, 
            list startups that do that and raised capital."

1. DRAFT
   ├─ Generates 250-word initial answer
   ├─ Identifies missing information (e.g., specific companies, funding amounts)
   └─ Creates search queries

2. EXECUTE_TOOLS
   ├─ Search: "AI-powered SOC startups funding"
   ├─ Search: "Autonomous security operations center companies"
   └─ Collects results from Tavily

3. REVISE
   ├─ Incorporates search findings
   ├─ Adds numerical citations [1], [2], etc.
   ├─ Includes References section
   └─ Keeps answer within 250 words

4. OUTPUT
   - Final researched answer with citations
   - References to sources
```

## How It Works

### Workflow Diagram

```
           ┌────────────┐
           │   DRAFT    │
           └──────┬─────┘
                  │
          ┌───────▼──────────┐
          │  EXECUTE_TOOLS   │
          │  (Web Search)    │
          └───────┬──────────┘
                  │
          ┌───────▼──────────┐
          │     REVISE       │
          └───────┬──────────┘
                  │
          ┌───────▼──────────────┐
          │  Iteration Limit     │
          │  Reached? (MAX=2)    │
          └───┬────────────┬─────┘
            YES│           │ NO
               │           └──────┐
               │                  │
            ┌──▼─────────────────┐│
            │   END / OUTPUT     ││
            └────────────────────┘└─ Loop back to REVISE (max 1 more time)
```

### Key Features

- **Structured Outputs**: Uses Pydantic models for reliable extraction
- **Self-Reflection**: Agent critiques its own answers
- **Research Integration**: Searches for missing information
- **Citation Support**: Includes citable references in final answer
- **Iteration Control**: Configurable maximum iterations (current: 2)
- **Tool Use**: Integrates Tavily Search API

### Reflection Structure

Each step includes:
- **Answer**: The actual response (≤250 words)
- **Missing**: What information gaps need addressing
- **Superfluous**: What information could be removed
- **Search Queries**: Specific queries to research gaps
- **References**: Sources cited in revised answer

## Configuration

### Adjust Iteration Limit

In `main.py`, modify `MAX_ITERATIONS`:
```python
MAX_ITERATIONS = 2  # Change this value
```

### Modify System Prompts

In `chains.py`, edit the actor prompt template to:
- Change the expertise level
- Add specific instructions
- Adjust output format

### Change LLM Model

In `chains.py`:
```python
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")  # Change model here
```

## Use Cases

- **Research Papers**: Iteratively building well-sourced documents
- **Fact Checking**: Verifying claims with web searches
- **News Writing**: Generating articles with citations
- **Legal Analysis**: Finding relevant case law and statutes
- **Product Research**: Analyzing competitors and market data
- **Academic Writing**: Creating properly cited content

## How It Differs from ReAct Agent

| Feature | ReAct | Reflexion |
|---------|-------|-----------|
| **Focus** | Tool selection based on reasoning | Research-driven iteration |
| **Loop** | Reason → Act → Loop | Draft → Search → Revise → Loop |
| **Self-Awareness** | No | Yes (self-critique) |
| **Output Format** | Any (tools determine) | Structured with citations |
| **Refinement** | Tool results | Research findings + reflection |

## Technology Stack

- **LangGraph**: Workflow orchestration
- **LangChain**: Chain and prompt management
- **Google Gemini 2.5 Flash**: Language model
- **Tavily Search**: Web search API
- **Pydantic**: Data validation and serialization
- **Python 3.11+**: Programming language

## References

- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
