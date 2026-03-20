import streamlit as st
import asyncio
import time
import os
from dotenv import load_dotenv
from loguru import logger

# ENV_TYPE=prod streamlit run streamlit_app.py

# Initialize API key
if "groq_api_key" not in st.session_state or not st.session_state.groq_api_key:
    if os.path.exists(".env"):
        load_dotenv()
        logger.info("✅ Loaded .env file")
    else:
        logger.info("No .env file found, using environment variables or manual input")

    # Try to get from environment
    env_key = os.getenv("GROQ_API_KEY", "")
    st.session_state.groq_api_key = env_key
    if env_key:
        logger.info("✅ Loaded GROQ_API_KEY from environment")


# Logging Setup
if "logging_setup_done" not in st.session_state:
    from app.logging_config import setup_logging
    setup_logging()
    st.session_state.logging_setup_done = True
    logger.info("Loguru configured successfully")



# Streamlit Workflow            
        

from workflow import graph_app
from api.api_client import init_clients
from core.state import AgenticState

#  Page config
st.set_page_config(
    page_title="YouTube Summary",
    page_icon="🎬",
    layout="wide"
)

#  Custom css
st.markdown("""
<style>
    .main-title {
        font-size: 3.5rem; font-weight: 800;
        background: linear-gradient(135deg, #ff4b4b, #ff8c4b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 1.2rem; color: #666; margin-top: -5px; margin-bottom: 30px; }
    .error-box {
        background: #ffe8e8; padding: 1rem; border-radius: 10px;
        border-left: 4px solid #ff0000; color: #d32f2f;
    }
</style>
""", unsafe_allow_html=True)

#  Session state
if 'state_dict' not in st.session_state:
    st.session_state.state_dict = {}
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'use_api_present' not in st.session_state:
    st.session_state.use_api_present = True

#  HEADER 
st.markdown('<p class="main-title">🎬 YouTube Summary</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Full transcript + AI summary⚡</p>', unsafe_allow_html=True)

#  Sidebar 
with st.sidebar:
    groq_api_key = st.text_input("GROQ API Key 🔑 ", type="password", value=st.session_state.groq_api_key)
    
    if groq_api_key:
        st.session_state.groq_api_key = groq_api_key
        st.session_state.api_key_valid = groq_api_key.startswith("gsk_")
        if st.session_state.api_key_valid:
            st.success("✅ API key ready", icon="🔑")
        else:
            st.warning("⚠️ API key should start with 'gsk_'")
    else:
        st.info("👆 Enter your Groq API key")

    st.markdown("## ⚙️ Configuration")
    use_api_present = st.toggle(
        "Use API for summary (recommended)",
        value=st.session_state.use_api_present,
        help="Groq = fast & high quality | Local BART = free but slower"
    )
    st.session_state.use_api_present = use_api_present

    st.markdown("#### ⚠️ YouTube may block IP → use VPN")
    st.divider()


    # Features Showcase
    st.subheader("✨ Key Features")
    features = [
        ("📥 Download", "Export summary (markdown) and raw transcript (txt) with one click"),
        ("🔀 Dual-Mode AI", "Switch between Groq API or local BART model"),
        ("⏱️ Real-time Streaming", "Watch markdown generate character-by-character"),
        ("🎥 2+ Hour Videos", "Handles long-form content with intelligent chunking"),
        ("📊 Rich Structuring", "Semantic sections, key quotes, entities, topics")
    ]
    

    for icon, desc in features:
        st.markdown(f"{icon} **{desc.split(' ', 1)[0]}** — {desc.split(' ', 1)[1]}")


    # Info 
    with st.expander("About & Tech Stack", expanded=False):
        st.markdown("""
        Built with:
        - **Streamlit** – Clean, responsive UI
        - **LangGraph** – Modular 5-node workflow
        - **Groq** – Fast LLM inference
        - **Hugging Face** – Local BART models
        - **yt-dlp** – Transcript extraction

        Created for turning long YouTube videos into beautifully structured summaries.
        """)


    # Footer note
    st.markdown(
        "<small style='color: gray;'>https://github.com/fcyber-labs/</small>", 
        unsafe_allow_html=True
    )



#  Input 
col1, col2 = st.columns([5, 1])
with col1:
    default_url = st.session_state.get('example_url', '')
    youtube_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        value=default_url,
        key="url_input",
        label_visibility="collapsed"
    )
with col2:
    process_btn = st.button(
        "🚀 Process",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.processing
    )




#  Processing 
if process_btn and youtube_url and not st.session_state.processing:
    if not st.session_state.get('api_key_valid'):
        st.error("👈 Please enter a valid GROQ API key | .env not found")
        st.stop()

    st.session_state.processing = True
    st.session_state.state_dict = None   

    progress_bar = st.progress(0, text="🚀 Starting pipeline...")
    status_text = st.empty()

    try:
        status_text.text("📥 Initializing AgenticState...")
        progress_bar.progress(0.2)

        if st.session_state.api_key_valid and st.session_state.groq_api_key:
            llm = init_clients(st.session_state.groq_api_key)
            st.session_state.llm = llm

            # DEBUG: Print what's going into initial_state
            logger.info("🚀 Creating initial_state with URL: {url}", url=youtube_url)

            initial_state = AgenticState(
                youtube_url=youtube_url,
                llm=llm,
                use_api_for_presentation=st.session_state.use_api_present
            )
            

            logger.info("✅ initial_state created with URL: {url}", url=initial_state.youtube_url)
        else:
            st.error("👈 Please enter a valid GROQ API key | .env not found")
            st.stop()

        status_text.text("🤖 Running full pipeline...")
        progress_bar.progress(0.5)

        final_state = asyncio.run(graph_app.ainvoke(initial_state))

        # Normalize state
        if hasattr(final_state, "model_dump"):
            raw_dict = final_state.model_dump()
        elif isinstance(final_state, dict):
            raw_dict = final_state
        else:
            raw_dict = vars(final_state)

        # Support both API mode and Local mode
        state_dict = raw_dict.copy()
        if 'node_5_present_api' in raw_dict:
            node5 = raw_dict['node_5_present_api']
            state_dict['final_formatted_markdown'] = node5.get('final_formatted_markdown')
            state_dict['presentation_complete'] = node5.get('presentation_complete')
            state_dict['video_id'] = node5.get('video_id', raw_dict.get('video_id'))

        st.session_state.state_dict = state_dict
        st.success("✅ Processing complete!")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.exception(e)
        logger.opt(exception=e, diagnose=False).error("Exception in Initializing AgenticState")
    finally:
        progress_bar.empty()
        status_text.empty()
        st.session_state.processing = False
        st.rerun()

#  Display 
state_dict = st.session_state.get('state_dict') or {}

if state_dict:  
# Only show tabs if data loaded
    tab1, tab2 = st.tabs(["📄 Summary", "📜 Raw Transcript"])

    with tab1:
        st.markdown("### ✨ Final Formatted Markdown")
        markdown = state_dict.get('final_formatted_markdown', '')

        if markdown and isinstance(markdown, str) and markdown.strip():
            st.markdown("=" * 80)
            st.markdown("**FINAL FORMATTED MARKDOWN OUTPUT**")
            st.markdown("=" * 80)

            output_container = st.empty()
            displayed = ""
            for line in markdown.split('\n'):
                displayed += line + "\n"
                if len(displayed) % 500 == 0:
                    output_container.markdown(f"```\n{displayed}▌\n```")
                    time.sleep(0.01)
            output_container.markdown(markdown)
            st.markdown("=" * 80)

            video_id = state_dict.get('video_id', 'video')
            st.download_button(
                label="📥 Download Markdown",
                data=markdown,
                file_name=f"{video_id}_summary.md",
                mime="text/markdown"
            )
        else:
            if st.session_state.processing:
                st.info("⏳ Processing... the markdown will appear here")
            else:
                st.info("⚠️ Run a video first to see the beautiful summary")

    with tab2:
        st.markdown("### 📜 Raw Transcript")
        transcript = state_dict.get('raw_transcript_text', '')

        if transcript:
            st.text_area("Raw Transcript", transcript, height=400)
            video_id = state_dict.get('video_id', 'video')
            st.download_button(
                label="📥 Download Transcript",
                data=transcript,
                file_name=f"{video_id}_transcript.txt",
                mime="text/plain"
            )
        else:
            st.info("⚠️ No transcript yet")

    # Errors
    errors = state_dict.get('errors', [])
    if errors:
        with st.expander("⚠️ Errors Encountered"):
            for err in errors:
                msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
                st.markdown(f'<div class="error-box">❌ {msg}</div>', unsafe_allow_html=True)
                logger.error("Errors Encountered: {msg}", msg=err.get("message", str(err)))

    # Debug
    with st.expander("🔧 Debug: Full AgenticState", expanded=False):
        st.json({
            "youtube_url": state_dict.get('youtube_url'),
            "video_id": state_dict.get('video_id'),
            "presentation_complete": state_dict.get('presentation_complete'),
            "final_markdown_length": len(state_dict.get('final_formatted_markdown', '')),
            "structured_sections": len(state_dict.get('structured_script', {}).get('sections', [])),
            "errors": state_dict.get('errors', []),
            "title": state_dict.get('title'),
            "channel": state_dict.get('channel'),
            "upload_date": state_dict.get('upload_date'),
            "duration_seconds": state_dict.get('duration_seconds'),
            "duration_human": state_dict.get('duration_human'),
            "has_manual_captions": state_dict.get('has_manual_captions'),
            "language": state_dict.get('language'),
            "is_live": state_dict.get('is_live')
        })


# Footer
st.markdown("---")
st.markdown(
    f"⚡ **YouTube Transcript Master** • "
    f"Summary: {'🚀 API' if st.session_state.use_api_present else '💻 Local Model'}"
)
