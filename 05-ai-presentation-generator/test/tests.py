import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


import pytest
import asyncio

from core.state import PresentationState
from nodes.node_1_input_processing import node_1_input_processing
from nodes.node_2_semantic_structuring import node_2_semantic_structuring
from nodes.node_4_slide_planning import node_4_slide_planning
from nodes.node_5_content_formatting import node_5_content_formatting
from nodes.node_6_2_ppt_generation import node_6_2_ppt_generation


from structure_router.structure_router import structure_router

def test_node_1_input_processing():
    state: PresentationState = {"raw_text": "Hello World! This is a test text."}
    result = node_1_input_processing(state)
    assert "cleaned_text" in result
    assert "text_chunks" in result
    assert len(result["cleaned_text"]) > 0

@pytest.mark.asyncio
async def test_node_2_semantic_structuring():
    state: PresentationState = {
        "cleaned_text": "AI is transforming presentations.",
        "text_chunks": ["AI is transforming presentations."]
    }
    result = await node_2_semantic_structuring(state)
    assert "structured_sections" in result
    assert "refined_key_points" in result

@pytest.mark.asyncio
async def test_node_4_slide_planning():
    state: PresentationState = {
        "refined_key_points": [{"point": "Test point", "importance": 5}],
        "structured_sections": []
    }
    result = await node_4_slide_planning(state)
    assert "slide_plan" in result

@pytest.mark.asyncio
async def test_node_5_content_formatting():
    state: PresentationState = {
        "slide_plan": [{"title": "Test", "bullets": ["Long bullet that should be shortened"]}]
    }
    result = await node_5_content_formatting(state)
    assert "formatted_slides" in result

def test_node_6_2_ppt_generation():
    state: PresentationState = {
        "formatted_slides": [{"title": "Test Slide", "bullets": ["Bullet 1", "Bullet 2"]}],
        "structured_sections": [],
        "output_format": "ppt",
        "image_bytes": {}
    }
    result = node_6_2_ppt_generation(state)
    assert result["ppt_file_path"].endswith(".pptx")





def test_router_returns_image_generation_when_use_images_is_true():
    state = {"use_images": True}
    result = structure_router(state)
    assert result == "node_6_1_image_generation"

def test_router_returns_ppt_generation_when_use_images_is_false():
    state = {"use_images": False}
    result = structure_router(state)
    assert result == "node_6_2_ppt_generation"

def test_router_returns_ppt_generation_when_use_images_missing():
    state = {}
    result = structure_router(state)
    assert result == "node_6_2_ppt_generation"