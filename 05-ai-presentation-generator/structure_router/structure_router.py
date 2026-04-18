from typing import List, Dict, Any, Literal

from core.state import PresentationState


def structure_router(state: PresentationState) -> Literal["node_6_1_image_generation", "node_6_2_ppt_generation"]:
    """
    Router -  whether to generate images or skip 
    """
    if state.get("use_images", False):
        return "node_6_1_image_generation"
    return "node_6_2_ppt_generation"