


from config.logging_config import logger
from config.settings import get_llm

from core.state import PresentationState




import streamlit as st
import asyncio
import nest_asyncio
from workflow.workflow import create_presentation_graph

import os
import base64

# Apply nest_asyncio
nest_asyncio.apply()

# Page config
st.set_page_config(
    page_title="AI Presentation Generator",
    page_icon="🎨",
    layout="centered"
)

# Title
st.title("🎨 AI Presentation Generator")
st.markdown("*Turn any text into a professional presentation*")

# Sidebar - Image mode switcher
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    use_images = st.toggle(
        "🎨 Generate Images (GPU required)", 
        value=False,
        help="Enable AI-generated backgrounds. Requires GPU (T4 in Colab). Disable for CPU mode."
    )
    
    if use_images:
        st.info("🖼️ Image generation enabled (GPU mode)")
    else:
        st.info("💻 Image generation disabled (CPU mode - faster)")

# Example text
example_text = """Artificial Intelligence in Healthcare: Transforming Patient Care

Artificial Intelligence is revolutionizing healthcare by improving diagnosis accuracy, personalizing treatment plans, and streamlining administrative tasks. Machine learning algorithms can now detect diseases like cancer from medical images with higher accuracy than human radiologists.

Key Benefits:
- Early disease detection through pattern recognition
- Personalized treatment recommendations based on patient data
- Reduced administrative burden through automated documentation
- 24/7 patient support via AI-powered chatbots

Implementation Challenges:
- Data privacy and security concerns
- Integration with existing healthcare systems
- Need for regulatory compliance
- Training healthcare professionals to use AI tools

Future Outlook:
- AI-powered robotic surgery
- Predictive analytics for disease outbreaks
- Virtual health assistants for remote monitoring
- Drug discovery acceleration through AI modeling"""

# Main text input
st.markdown("### 📝 Enter your content")
text_input = st.text_area(
    "Paste your text here:",
    height=300,
    value=st.session_state.get("text_input", ""),
    placeholder="Paste your article, notes, or any text content here...\n\nThe AI will automatically extract key points and create a professional presentation.",
    help="Supports up to 50,000 characters"
)

# Store in session state
st.session_state.text_input = text_input

# Load example button - FIXED
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("📋 Load Example", type="secondary"):
        st.session_state.text_input = example_text
        st.rerun()

# Generate button
if st.button("🚀 Generate Presentation", type="primary", use_container_width=True):
    if not st.session_state.text_input.strip():
        st.error("❌ Please enter some text first!")
    else:
        with st.spinner("🎨 Generating your presentation... This may take a minute."):
            try:
                # Async runner

                async def run_agent():
                    graph = create_presentation_graph()
                    
                    initial_state: PresentationState = {
                        # Input
                        "raw_text": st.session_state.text_input,
                        
                        # Processing stages
                        "cleaned_text": "",
                        "text_chunks": [],
                        "structured_sections": [],
                        "refined_key_points": [],
                        
                        # Content generation
                        "executive_summary": "",
                        "presentation_theme": "",
                        "audience_type": "",
                        "total_insights": 0,
                        "slide_plan": [],
                        "formatted_slides": [],
                        
                        # Visual elements
                        "visual_suggestions": [],
                        "image_bytes": {},
                        "images_generated": False,
                        "image_gen_time": 0.0,
                        "slide_dimensions": {},
                        
                        # Output settings
                        "use_images": use_images,
                        "output_format": "ppt",
                        "ppt_file_path": "",
                        "pdf_file_path": "",
                        
                        # Feedback
                        "user_feedback": ""
                    }
                    
                    result = await graph.ainvoke(
                        initial_state,
                        config={"configurable": {"thread_id": "streamlit_app"}}
                    )
                    return result
                
                def run_sync():
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        return asyncio.run(run_agent())
                    else:
                        return loop.run_until_complete(run_agent())
                
                result = run_sync()
                
                # Check if PPT was generated
                ppt_path = result.get("ppt_file_path")
                
                if ppt_path and os.path.exists(ppt_path):
                    st.success("✅ Presentation generated successfully!")
                    
                    # Read file for download
                    with open(ppt_path, "rb") as f:
                        ppt_bytes = f.read()
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Presentation (PPTX)",
                        data=ppt_bytes,
                        file_name="presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )
                    


                    if result.get("images_generated", False):
                        st.balloons()
                        st.success("🎨 AI-generated images included!")
                        
                else:
                    st.error("❌ Failed to generate presentation. Please check your API keys.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by Groq LLM | LangGraph | Streamlit</p>",
    "<p style='text-align: center; color: gray;'>https://github.com/fcyber-labs/ai-engineering-hub</p>",
    unsafe_allow_html=True
)