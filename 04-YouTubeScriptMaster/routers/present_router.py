from core.state import AgenticState

from loguru import logger
from typing import List, Dict, Any, Literal


@logger.catch
def present_router(state: AgenticState) -> Literal["api", "local"]:
    """
    Router - directs to BART or API summarizer
    """
    if state.use_api_for_presentation:
        logger.info("Router: API")
        return "api"
        
    logger.info("✅ Router: local model")
    return "local"


