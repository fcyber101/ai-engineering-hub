### 📺 [4.  YouTubeScriptMaster](./04-YouTubeScriptMaster)
[![Demo Video](https://img.shields.io/badge/📺-Watch%20Demo-red)](assets/project4-demo.gif) [![Live App](https://img.shields.io/badge/🤗-Try%20Now-yellow)](https://huggingface.co/spaces/fcyber/YouTubeScriptMaster)


#### Automatically generate structured scripts from any YouTube link with YouTube Summary Master. The system intelligently chunks long videos, extracts metadata, and creates rich summaries including executive overviews, TL;DR, semantic sections, key insights, and named entities – all in a beautifully formatted markdown document. Choose between lightning-fast Groq API or privacy-focused local BART processing, then download both summary and raw transcript with one click.




<div align="center">

![Status](https://img.shields.io/badge/Status-Active-success) 
![LangGraph](https://img.shields.io/badge/LangGraph-🦜-blue) 
![Groq](https://img.shields.io/badge/Groq-⚡-purple) 
![BART](https://img.shields.io/badge/BART-🤗-blue) 
![yt-dlp](https://img.shields.io/badge/yt--dlp-🎥-darkgreen) 
![Loguru](https://img.shields.io/badge/Loguru-📋-teal) 
![Level](https://img.shields.io/badge/Level-Advanced-purple) 


</div>
---


| Feature | Description |
| :--- | :--- |
| **📹 Multi-Source Transcript Extraction** | Automatically fetches transcripts from YouTube subtitles (manual & auto-generated), video descriptions, and external sources with intelligent fallback strategies. |
| **🧠 Smart Metadata Extraction** | Extracts video title, channel, upload date, duration, caption type, and language with confidence scoring. |
| **🔀 Dual-Mode AI Processing** | Switch between **Groq API** for lightning-fast, high-quality structuring or **Local BART** (sshleifer/distilbart-cnn-12-6) for free, private processing. |
| **📊 Rich Content Structuring** | Generates executive summary, TL;DR, semantic sections, key insights, key quotes, named entities, and main topics from any video transcript. |
| **🎨 Beautiful Markdown Output** | Creates professionally formatted markdown with table of contents, numbered sections, quote blocks, entity lists, and proper spacing. |
| **📥 Export & Download** | One-click download of both markdown summary and raw transcript for offline use and archiving. |
| **⏱️ Real-time Streaming** | Watch the markdown generate character-by-character in the Streamlit UI with live progress indicators. |
| **🔄 LangGraph Workflow** | Orchestrates the entire 5-node pipeline (metadata → extraction → cleaning → structuring → presentation) with conditional routing for API/local modes. |
| **🧩 Intelligent Chunking** | Handles 2+ hour videos with smart text splitting, overlapping chunks, and consolidation for complete transcript processing. |
| **⚡ Groq Acceleration** | Ultra-fast LLM inference powered by Groq's LPU technology for real-time structuring of long-form content. |
| **🤗 Local BART Model** | Facebook's DistilBART (sshleifer/distilbart-cnn-12-6) provides free, private summarization with high-quality results for offline use. |
| **📝 Structured Logging** | **loguru**-based logging with rotation, compression, JSON output for cloud, colorized terminal output for development, and persistent log files for production. |

---

<div align="center">

![Agentischer RAG-Workflow](assets/workflow.gif)

</div>

---


## 🚀 Getting Started
### 🎯 Quick Start Comparison

| Method | Command | Time | Requires |
|--------|---------|------|----------|
| **Python** | `pip install -r requirements.txt && streamlit run streamlit_app.py` | 2-5 min | Python 3.9+ |
| **Docker** | `docker-compose up -d` | 30 sec | Docker + Compose |
| **Hugging Face** | [![Hugging Face](https://img.shields.io/badge/🤗%20Live%20Demo-FFD21E?style=flat-square)](https://huggingface.co/spaces/fcyber/YouTubeScriptMaster) | 1 sec | Web browser |


### 📦 Option 1: Python (Local Setup)

1. **Clone the repository**
   ```bash
   git clone https://github.com/fcyber-labs/ai-engineering-hub.git
   ```

2. **Navigate to the desired project directory**
   ```bash
   cd ai-engineering-hub/04-YouTubeScriptMaster
   ```

3. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run streamlit apps**
   ```bash
   streamlit run streamlit_app.py
   ```

#### Follow the project-specific instructions in each project's `README.md` file to set up and run the app.
• • •

### 🐳 Option 2: Docker Compose (Recommended)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/fcyber/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)

1. **Clone the repository**
```bash
git clone https://github.com/fcyber-labs/ai-engineering-hub.git
```

2. **Navigate to the desired project directory**
```bash
cd ai-engineering-hub/04-YouTubeScriptMaster
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your GROQ_API_KEY keys
```

4. **Run with Docker Compose**
```bash
docker-compose up -d
```

5. **View logs (optional)**
```bash
docker-compose logs -f
```

6. **Open in browser**
```bash
http://localhost:8501
```


7. **Stop the container**
```bash
docker-compose down
```

**That's it!** The project includes a pre-configured `Dockerfile` and `docker-compose.yml` — no additional setup needed.

• • •

### 🤗 Option 3: Hugging Face Spaces

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Live%20Demo-Hugging%20Face-FFD21E?style=for-the-badge)](https://huggingface.co/spaces/fcyber/YouTubeScriptMaster)

```bash
# No installation needed! Click the badge above to try the live demo.
# Or clone and run locally:
pip install huggingface-hub
huggingface-cli download fcyber/YouTubeScriptMaster
python streamlit run streamlit_app.py  # Gradio apps run with python
```
---
### 🖥  Watch demo 
[![Demo Video](https://img.shields.io/badge/📺-Watch%20Demo-red)](assets/project4-demo.gif)

<div align="center">

![Agentischer RAG-Workflow](assets/project4-demo.gif)

</div>

---