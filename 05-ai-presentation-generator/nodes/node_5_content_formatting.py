from loguru import logger
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from typing import List

from core.state import PresentationState
from config.settings import get_llm



class FormattedSlide(BaseModel):
    title: str
    bullets: List[str]

class FormattedSlides(BaseModel):
    slides: List[FormattedSlide]

async def node_5_content_formatting(state: PresentationState) -> PresentationState:
    """Starting content formatting"""

    logger.info("Node 5: Starting content formatting")
    llm = get_llm()
    parser = PydanticOutputParser(pydantic_object=FormattedSlides)

    prompt = f"""Convert the slide plan into beautiful, concise, presentation-ready content.

Rules:
- Keep every bullet very short (maximum 8-10 words)
- Make language professional and impactful

Current plan:
{state.get('slide_plan', [])}

Return ONLY valid JSON in this exact format:
{parser.get_format_instructions()}

Do not add any extra text or markdown."""

    response = await llm.ainvoke(prompt)

    try:
        formatted_output = parser.parse(response.content)
        result = [slide.model_dump() for slide in formatted_output.slides]
    except Exception as e:
        logger.error(f"Parsing failed in Node 5: {e}")
        result = []

    logger.success(f"Node 5 completed | Formatted {len(result)} slides")
    return {**state, "formatted_slides": result}