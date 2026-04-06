from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

reflection_prompt = ChatPromptTemplate.from_messages(
[
    (
      "system",
      "You have a doctorate in English literature. Generate critique and recommendations for the user's short essay."
      "Always provide detailed feedback and suggestions for improvement. Be constructive and specific in your critique."  
    ),
    MessagesPlaceholder(variable_name="messages")
]
)

generation_prompt = ChatPromptTemplate.from_messages(
[
    (
      "system",
      "You have a doctorate in English literature. Generate a short essay based on the given topic"
      "Always provide detailed and well-structured content. Be creative and insightful in your writing."
      "The essay should no longer than 500 words."  
    ),
    MessagesPlaceholder(variable_name="messages")
]
)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

#chains
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm