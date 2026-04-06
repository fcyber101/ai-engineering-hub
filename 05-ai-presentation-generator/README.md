### 👨‍🎨 [5.  AI Presentation Generator](./05-ai-presentation-generator)
[![Demo Video](https://img.shields.io/badge/📺-Watch%20Demo-red)](assets/project5-demo.gif) [![Live App](https://img.shields.io/badge/🤗-Try%20Now-yellow)](https://huggingface.co/spaces/fcyber/YouTubeScriptMaster)


#### AI Presentation Generator is an AI-powered presentation engine that transforms raw text into polished, executive-ready PowerPoint decks using a structured LangGraph pipeline. It extracts key insights, organizes content into compelling narratives, generates concise summaries, and enhances each slide with AI-generated visuals and modern glassmorphism design. The result is a high-impact, visually consistent .pptx presentation that rivals professional-grade work—delivering one clear, memorable takeaway per slide.




<div align="center">

![Status](https://img.shields.io/badge/Status-Active-success)
![LangGraph](https://img.shields.io/badge/LangGraph-🦜-blue)
![Groq](https://img.shields.io/badge/Groq-⚡-purple)
![Playground](https://img.shields.io/badge/Playground-v2.5-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Loguru](https://img.shields.io/badge/Loguru-📋-teal)
![Level](https://img.shields.io/badge/Level-Advanced-purple)
![AI Image Generation](https://img.shields.io/badge/AI_Image_Generation-🖼️-purple)


</div>
---


| Feature | Description |
| :--- | :--- |
| 📝 **Flexible Input Handling** | Accepts raw text, `.txt`, `.md`, or copied content |
| 🧠 **Insight Extraction** | Identifies key ideas and important information automatically |
| 📐 **Smart Structuring** | Organizes content into logical sections (problem, solution, insights) |
| ✍️ **Executive Summaries** | Generates short, clear summaries for each section |
| 🎯 **Slide Planning** | Determines optimal number of slides and layout |
| 📊 **Content Formatting** | Creates clean bullet points and structured slides |
| 🖼️ **AI Image Generation** | Generates backgrounds for title, slides, and closing page |
| 🎨 **Modern Design** | Clean, professional styling with consistent visuals |
| 📌 **Key Message Focus** | Each slide delivers one clear takeaway |
| 📄 **Export Options** | Generates PowerPoint (`.pptx`) with optional PDF |

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
   git clone [https://github.com/fcyber/ai-engineering-hub.git](https://github.com/fcyber/ai-engineering-hub.git)
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
git clone https://github.com/fcyber/ai-engineering-hub.git
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
