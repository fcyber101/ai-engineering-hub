from langgraph.graph import StateGraph, END


from core.state import AgenticState
from nodes.node1 import node_1_video_metadata_and_source_detection
from nodes.node2 import node_2_transcript_extraction
from nodes.node3 import node_3_transcript_cleaning_and_normalization
from nodes.node4 import node_4_intelligent_structuring_api
from nodes.node5 import node_5_beautiful_presentation
from nodes.node5_api import node_5_beautiful_presentation_api

from routers.present_router import present_router


workflow = StateGraph(AgenticState)

workflow.add_node("node_1_metadata", node_1_video_metadata_and_source_detection)
workflow.add_node("node_2_extract", node_2_transcript_extraction)
workflow.add_node("node_3_clean", node_3_transcript_cleaning_and_normalization)


workflow.add_node("node_4_structure_api", node_4_intelligent_structuring_api)

workflow.add_node("node_5_present", node_5_beautiful_presentation)
workflow.add_node("node_5_present_api", node_5_beautiful_presentation_api)





workflow.set_entry_point("node_1_metadata")
workflow.add_edge("node_1_metadata", "node_2_extract")
workflow.add_edge("node_2_extract", "node_3_clean")


workflow.add_edge("node_3_clean", "node_4_structure_api")

workflow.add_conditional_edges(
    "node_4_structure_api",
    present_router,
    {
        "local": "node_5_present",
        "api": "node_5_present_api"
    }
)

workflow.add_edge("node_5_present", END)
workflow.add_edge("node_5_present_api", END)

graph_app = workflow.compile(debug=True)
graph_app