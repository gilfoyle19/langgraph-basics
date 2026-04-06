# Reflexion Agent

A sophisticated LangGraph-based research agent that drafts answers, searches for information, and revises based on research findings. Implements the Reflexion pattern from the paper ["Reflexion: Language Agents with Verbal Reinforcement Learning"](https://arxiv.org/abs/2303.11366).

## Overview

The Reflexion Agent demonstrates a research-driven improvement loop:
1. **Draft**: Agent produces an initial 250-word answer to a question
2. **Reflect**: Agent critiques its own answer and identifies information gaps
3. **Search**: Runs web searches based on identified gaps
4. **Revise**: Updates the answer using research findings
5. **Iterate**: Repeats until reaching maximum iterations or satisfactory quality

This pattern is ideal for research tasks, fact-checking, and knowledge-intensive questions requiring citations.

## Project Structure

```
reflexion-agent/
├── main.py              # Graph orchestration and workflow
├── chains.py            # LLM chains for drafting and revising
├── schemas.py           # Pydantic models for structured outputs
└── tool_executor.py     # Tool execution (web search)
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
  - Uses `PydanticToolsParser` for reliable output parsing

- **`tool_executor.py`**: Tool integration
  - `tavily_tool`: Web search via Tavily API
  - `run_queries()`: Executes search queries
  - `execute_tools`: LangGraph tool node for search execution

- **`main.py`**: Graph construction and execution
  - `draft_node()`: Initial answer generation
  - `revise_node()`: Answer refinement
  - `event_loop()`: Iteration control (max 2 iterations)
  - Complete workflow execution and output handling

## Requirements

- Python >= 3.11
- Google API key (for Gemini)
- Tavily API key (for web search)

## Installation

1. From the project root, install dependencies:
```bash
pip install -e .
```

2. Set up your `.env` file in the project root with:
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

The agent will research a query by:
1. Drafting an initial answer
2. Searching for relevant information
3. Revising the answer with citations
4. Outputting the final researched response

### Custom Query

To use a different query, modify `main.py`:

```python
res = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Your custom research question here.",
            }
        ]
    }
)
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

### Example Workflow Output

```
Question: "Write about AI-Powered SOC / autonomous SOC problem domain, 
           list startups that do that and raised capital."

1. DRAFT
   ├─ Generates 250-word initial answer
   ├─ Identifies missing information (specific companies, funding amounts)
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

### Key Features

- **Structured Outputs**: Uses Pydantic models for reliable extraction
- **Self-Reflection**: Agent critiques its own answers
- **Research Integration**: Searches for missing information
- **Citation Support**: Includes citable references in final answer
- **Iteration Control**: Configurable maximum iterations (current: 2)
- **Tool Use**: Integrates Tavily Search API for real information

## Configuration

### Adjust Iteration Limit

In `main.py`, modify `MAX_ITERATIONS`:

```python
MAX_ITERATIONS = 3  # Change this value to allow more revisions
```

### Modify System Prompts

In `chains.py`, edit the actor prompt template:

```python
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert researcher specializing in [YOUR_DOMAIN].
Current time: {time}

1. {first_instruction}
2. [Your custom instructions here]
3. Recommend search queries to research information and improve your answer.""",
        ),
        ...
    ]
)
```

### Change LLM Model

In `chains.py`:

```python
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
```

### Adjust Search Results

In `tool_executor.py`, modify max_results:

```python
tavily_tool = TavilySearch(max_results=10)  # Get more results
```

## Use Cases

- **Research Papers**: Building well-sourced documents iteratively
- **Fact Checking**: Verifying claims with web searches
- **News Writing**: Generating articles with citations
- **Legal Analysis**: Finding relevant case law and statutes
- **Product Research**: Analyzing competitors and market data
- **Academic Writing**: Creating properly cited content
- **Knowledge Base**: Building comprehensive reference documents

## Comparison with Other Agents

| Feature | ReAct | Reflection | Reflexion |
|---------|-------|-----------|-----------|
| **Primary Use** | Tool-driven tasks | Content refinement | Research & facts |
| **Stopping Criteria** | Tool availability | Message count | Iteration limit |
| **Self-Awareness** | No | Yes | Yes |
| **Output Structure** | Unstructured | Unstructured | Structured w/ citations |
| **External API** | Any tools | None | Web search |
| **Best For** | Planning, execution | Writing, creation | Research, citing |

## Output Format

The agent produces structured output with:

```python
{
    "answer": "250-word researched answer...",
    "reflection": {
        "missing": "Information gaps that were addressed",
        "superfluous": "Details that were removed"
    },
    "search_queries": ["search 1", "search 2"],
    "references": ["[1] https://source1.com", "[2] https://source2.com"]
}
```

## Common Issues

### No Search Results
- Verify Tavily API key is valid and has quota
- Check internet connection
- Try broader search queries

### Poor Quality Revisions
- Increase `MAX_ITERATIONS` for more refinement cycles
- Improve search query generation in first_responder
- Adjust LLM temperature for more variation

### Missing Citations
- Verify search results contain URL information
- Check Pydantic schema requires references field
- Ensure `ReviseAnswer` model is being used in revision

### Token Limit Exceeded
- Reduce `max_results` in TavilySearch
- Shorten initial prompt templates
- Limit message history

## Extensions

### Adding Multiple Search Strategies

Implement different search approaches:

```python
def intelligent_search_queries(reflection) -> List[str]:
    # Generate more sophisticated queries based on reflection
    # Could combine multiple query types:
    # - Exact phrase searches
    # - Domain-specific searches
    # - Temporal searches (recent articles)
    ...
```

### Integration with Document Storage

Save researched answers to a knowledge base:

```python
def save_to_knowledge_base(answer, references):
    # Store in vector DB for future reference
    # Create embeddings for semantic search
    # Organize by topic/category
    ...
```

### Interactive Refinement

Allow user feedback during iteration:

```python
while True:
    result = graph.invoke({"messages": messages})
    print(f"Answer: {result['messages'][-1].content}")
    feedback = input("Continue refining? (y/n): ")
    if feedback.lower() != 'y':
        break
    messages.extend(result["messages"])
```

## References

- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Tavily Search API](https://tavily.com/)

## Technology Stack

- **LangGraph**: Workflow orchestration and state machines
- **LangChain**: Chain and prompt management, tool abstractions
- **Google Gemini 2.5 Flash**: Language model for reasoning
- **Tavily Search**: Web search API
- **Pydantic**: Data validation and structured outputs
- **Python 3.11+**: Programming language

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
