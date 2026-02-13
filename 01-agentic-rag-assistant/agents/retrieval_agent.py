

### Retriever Grader

from typing import Literal

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate




def create_retriever_grader(llm):
    """Define data model for document evaluation"""
    class GradeDocuments(BaseModel):
        """Grade whether a retrieved document is relevant to the user question."""

        relevant: Literal["yes", "no"] = Field(...,
            description="Is the document relevant to the question?"
        )
        reasoning: str = Field(  
            ...,
            description="Short explanation (1–2 sentences) why you chose this route"
        )

    structured_llm_grader = llm.with_structured_output(GradeDocuments)

    # Create prompt template containing system message and user question
    system = """You are an expert relevance grader for a company RAG system.

            Your job is to decide if a retrieved document chunk contains information useful 
            to answer the user question. Be lenient: if the document has **any** keywords, 
            semantic overlap or related concepts → grade 'yes'.

            Rules:
            - Grade 'yes' if the document mentions entities, topics, processes, numbers 
            or context that could help answer the question (even partially).
            - Grade 'no' only if the document is clearly unrelated (wrong topic, random text, 
            boilerplate, footer, navigation links...).
            - Do NOT be overly strict — better to keep some marginal docs than filter out good ones.
            
            Now evaluate this document against the question:"""

    grade_prompt = ChatPromptTemplate(
        [
            ("system", system),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}")
        ]
    )

    # Create document retrieval grader
    retrieval_grader = grade_prompt | structured_llm_grader
    return retrieval_grader


