
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from core.state import PresentationState
from nodes.node_1_input_processing import node_1_input_processing
from nodes.node_2_semantic_structuring import node_2_semantic_structuring
from nodes.node_4_slide_planning import node_4_slide_planning
from nodes.node_5_content_formatting import node_5_content_formatting
from nodes.node_6_1_image_generation import node_6_1_image_generation
from nodes.node_6_2_ppt_generation import node_6_2_ppt_generation

from structure_router.structure_router import structure_router

def create_presentation_graph():
    """Creates the full Presentation Agent LangGraph with conditional image generation"""

    workflow = StateGraph(PresentationState)


    workflow.add_node("node_1_input_processing", node_1_input_processing)
    workflow.add_node("node_2_semantic_structuring", node_2_semantic_structuring)
    workflow.add_node("node_4_slide_planning", node_4_slide_planning)
    workflow.add_node("node_5_content_formatting", node_5_content_formatting)
    workflow.add_node("node_6_1_image_generation", node_6_1_image_generation)
    workflow.add_node("node_6_2_ppt_generation", node_6_2_ppt_generation)


    workflow.add_edge(START, "node_1_input_processing")
    workflow.add_edge("node_1_input_processing", "node_2_semantic_structuring")
    workflow.add_edge("node_2_semantic_structuring", "node_4_slide_planning")
    workflow.add_edge("node_4_slide_planning", "node_5_content_formatting")

    # Conditional edge 
    workflow.add_conditional_edges(
        "node_5_content_formatting",
        structure_router,  
        {
            "node_6_1_image_generation": "node_6_1_image_generation",
            "node_6_2_ppt_generation": "node_6_2_ppt_generation"
        }
    )

    workflow.add_edge("node_6_1_image_generation", "node_6_2_ppt_generation")
    workflow.add_edge("node_6_2_ppt_generation", END)

    memory = MemorySaver()
    graph = workflow.compile(checkpointer=memory)
    return graph