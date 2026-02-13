


# Router

from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field



# Data model
def create_question_checker(llm):
    """Route the query"""
    class QueryRoute(BaseModel):
        """Decide whether a user question should be answered from the company knowledge base."""

        route: Literal["vectorstore", "general_chat", "needs_clarification"] = Field(
            ...,
            description="One of: 'vectorstore', 'general_chat', 'needs_clarification'"
        )


    structured_llm_router = llm.with_structured_output(QueryRoute)

    # Prompt
    system_prompt = """You are a routing expert for a company internal AI assistant.

The vector store ONLY contains documents about:
• Company history, mission, values
• Products, services, features, pricing
• Internal policies, HR, benefits
• Organizational structure, teams, key people
• Processes, guidelines, SOPs
• Financial reports, OKRs (internal only), Financial analysis

Rules – output EXACTLY one of these three values for 'route':
vectorstore       - if the question is clearly about the company, products, policies, people, processes, internal rules or documents
general_chat      - if the question is clearly unrelated to the company (weather, math, recipes, jokes, sports, politics, general knowledge, personal advice, LLM, LangGraph, Programming)
needs_clarification - if the question is too vague, ambiguous, incomplete, or could reasonably go to more than one category

Examples:
Question: What is our sick leave policy?     → route: "vectorstore"
Question: What's the weather in Berlin?      → route: "general_chat"
Question: Tell me about something...         → route: "needs_clarification"

Now classify this question.'.
"""

    route_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}")
        ]
    )

    router_chain = route_prompt | structured_llm_router
    return router_chain

