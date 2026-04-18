from loguru import logger
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from typing import List


from core.state import PresentationState
from config.settings import get_llm


class Slide(BaseModel):
    slide_number: int
    title: str
    bullets: List[str] = Field(default_factory=list)

class SlidePlan(BaseModel):
    slides: List[Slide]

async def node_4_slide_planning(state: PresentationState) -> PresentationState:
    """Starting slide planning"""
    
    logger.info("Node 4: Starting slide planning")
    llm = get_llm()
    parser = PydanticOutputParser(pydantic_object=SlidePlan)

    prompt = (
    "Create a professional and logical slide plan from the key points below.\n\n"
    "You MUST generate a valid JSON object. Every slide object MUST contain a 'bullets' field, "
    "even if it is an empty list ([]). Do not omit the 'bullets' key.\n\n"
    'Example format: {"slides": [{"slide_number": 1, "title": "...", "bullets": ["point 1", "point 2"]}]}\n\n'
    f"Key points:\n{state.get('refined_key_points', [])}\n\n"
    f"Return ONLY valid JSON in this exact format:\n{parser.get_format_instructions()}"
)

    response = await llm.ainvoke(prompt)
    plan = parser.parse(response.content)

    result = [s.model_dump() for s in plan.slides]

    logger.success(f"Node 4 completed | Planned {len(result)} slides")
    return {**state, "slide_plan": result}