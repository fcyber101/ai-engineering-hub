from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from pathlib import Path
from dotenv import load_dotenv

from workflow.workflow import create_presentation_graph
from core.state import PresentationState

app = FastAPI()

# Load environment variables
load_dotenv()

# Store API key (in memory - for demo purposes)
# In production, use a secure key management system
api_key_store = {"groq_api_key": os.getenv("GROQ_API_KEY", "")}

# Request model
class GenerateRequest(BaseModel):
    text: str
    use_images: bool = False
    groq_api_key: str = None

@app.get("/", response_class=HTMLResponse)
async def home():
    html_path = Path(__file__).parent / "templates" / "index.html"
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    else:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head><title>AI Presentation Generator</title></head>
        <body>
            <h1>🎨 AI Presentation Generator</h1>
            <p>Template file not found. Please check installation.</p>
        </body>
        </html>
        """)

@app.post("/validate_key")
async def validate_key(request: Request):
    """Validate Groq API key"""
    data = await request.json()
    api_key = data.get("groq_api_key", "")
    
    # Check if key starts with 'gsk_' (Groq key format)
    is_valid = api_key.startswith("gsk_") if api_key else False
    
    if is_valid:
        api_key_store["groq_api_key"] = api_key
        # Here you could also test the key with a real API call
    
    return {"valid": is_valid}

@app.post("/generate")
async def generate(request: GenerateRequest):
    text = request.text
    use_images = request.use_images
    api_key = request.groq_api_key or api_key_store.get("groq_api_key", "")
    
    if not text.strip():
        return {"success": False, "error": "No text provided"}
    
    if not api_key or not api_key.startswith("gsk_"):
        return {"success": False, "error": "Valid Groq API key is required. Get one at console.groq.com"}
    
    try:
        # Set API key for the session (you may need to pass this to your workflow)
        os.environ["GROQ_API_KEY"] = api_key
        
        # Run the agent
        graph = create_presentation_graph()
        
        initial_state: PresentationState = {
            "raw_text": text,
            "cleaned_text": "",
            "text_chunks": [],
            "structured_sections": [],
            "refined_key_points": [],
            "executive_summary": "",
            "presentation_theme": "",
            "audience_type": "",
            "total_insights": 0,
            "slide_plan": [],
            "formatted_slides": [],
            "visual_suggestions": [],
            "image_bytes": {},
            "images_generated": False,
            "image_gen_time": 0.0,
            "slide_dimensions": {},
            "use_images": use_images,
            "output_format": "ppt",
            "ppt_file_path": "",
            "pdf_file_path": "",
            "user_feedback": ""
        }
        
        result = await graph.ainvoke(
            initial_state,
            config={"configurable": {"thread_id": "fastapi_app"}}
        )
        ppt_path = result.get("ppt_file_path")
        
        if ppt_path and os.path.exists(ppt_path):
            return {
                "success": True,
                "download_url": f"/download/{os.path.basename(ppt_path)}",
                "images_generated": result.get("images_generated", False)
            }
        else:
            return {"success": False, "error": "Generation failed"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/download/{filename}")
async def download(filename: str):
    file_path = Path("outputs") / filename
    if file_path.exists():
        return FileResponse(file_path, filename="presentation.pptx")
    return {"error": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)