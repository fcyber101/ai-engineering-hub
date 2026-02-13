### Adding Hallucination Checker for Responses

# define data model for hallucination check

from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field



def create_hallucination_grader(llm):
    """define data model for hallucination check"""
    class GradeHallucinations(BaseModel):
        """Evaluate hallucinations."""

        grounded: Literal["yes", "no"] = Field(
            description="Is answer grounded?"
        )

        reasoning: str = Field(
            description="Brief reasoning"
        )

        
    # Initialize LLM with function calling
    structured_llm_grader = llm.with_structured_output(GradeHallucinations)

    # Very simple prompt
    system_prompt = """Check if answer is based on documents. Say 'yes' unless clearly made up."""
    
    hallucination_prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", "Docs: {documents} \n Answer: {generation}")
        ]
    )

    hallucination_grader = hallucination_prompt | structured_llm_grader
    return hallucination_grader