from pydantic import BaseModel, Field
from typing import TypedDict, List, Dict, Optional

class PresentationState(TypedDict):
    raw_text: str
    cleaned_text: str
    text_chunks: List[str] 
    structured_sections: List[Dict]
    refined_key_points: List[Dict]
    executive_summary: str
    use_images: bool
    presentation_theme: str
    audience_type: str
    total_insights: int
    slide_plan: List[Dict]
    formatted_slides: List[Dict]
    image_bytes: Dict[str, bytes]
    images_generated: bool
    image_gen_time: float
    slide_dimensions: Dict[str, int]
    visual_suggestions: List[Dict]
    ppt_file_path: str
    pdf_file_path: str
    output_format: str
    user_feedback: str