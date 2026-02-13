from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


### Answer grader


def create_answer_grader(llm):
    """Check the answer after generation and hallucination check"""

    class GradeAnswer(BaseModel):
        """Evaluate whether the generated answer actually resolves"""

        addresses_answer: Literal["yes", "no"] = Field(
            ...,
            description="Does the answer meaningfully resolve or respond to the question? yes / no"
        )

        reasoning: str = Field(
            ...,
            description="1–3 sentences explaining which parts of the question are / are not addressed and why"
        )


    # Initialize LLM with function calling
    structured_llm_grader = llm.with_structured_output(GradeAnswer)

    # Prompt
    system = """You are an simple evaluator checking whether an LLM answer properly resolves a user question.

            Rules:
            - 'yes' - if the answer directly and completely addresses the core intent of the question
            - 'no' - if the answer misses important parts, dodges the question, or only partially responds

            Now evaluate this answer against the question:"""

    # Prompt template
    answer_prompt = ChatPromptTemplate(
        [
            ("system", system),
            ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
        ]
    )
    # Answer grader
    answer_grader = answer_prompt | structured_llm_grader

    return answer_grader