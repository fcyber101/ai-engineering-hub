

# State


from typing import TypedDict, Annotated, Sequence, List, Optional, Literal
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

# Possible route types
RouteType = Literal[
    "retrieve", "grade_retrieval", "generate_answer", 
    "hallucination_check", "grade_answer", "final_respond",
    "rewrite_query", "clarify", "off_topic", "end", "good"
]

# State definition
class GraphState(TypedDict):
    question: str
    original_question: str
    documents: List[Document]
    generation: str
    messages: Annotated[Sequence[BaseMessage], "add"]
    route: RouteType                      
    retrieval_grade: str
    hallucination_grade: str
    answer_grade: str
    rewrite_count: int
    max_rewrites: int = 3
    attempts: int
    grade_feedback: Optional[str]