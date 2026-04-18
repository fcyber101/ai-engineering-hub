

from loguru import logger
#from diffusers import DiffusionPipeline
#import torch
import time
from typing import Dict, Any, Optional, Tuple
from PIL import Image
import io


from core.state import PresentationState


class PlaygroundManager:
    """Singleton manager for Playground v2.5 model - loaded once in memory"""

    _instance = None
    _pipe = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_pipeline(self):
        if self._pipe is None:
            self._load_model()
        return self._pipe

    def _load_model(self):
        logger.info("🔄 Loading Playground v2.5 model...")

        if not torch.cuda.is_available():
            logger.warning("CUDA not available, using CPU")
            device = "cpu"
            dtype = torch.float32
        else:
            device = "cuda"
            dtype = torch.float16
            logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")

        self._pipe = DiffusionPipeline.from_pretrained(
            "playgroundai/playground-v2.5-1024px-aesthetic",
            torch_dtype=dtype,
            variant="fp16" if device == "cuda" else None,
            use_safetensors=True
        )
        self._pipe.to(device)
        self._pipe.enable_attention_slicing()

        if device == "cuda" and torch.cuda.get_device_properties(0).total_memory < 16e9:
            self._pipe.enable_sequential_cpu_offload()

        logger.success("Playground v2.5 model ready")

playground_manager = PlaygroundManager()

async def generate_image_memory(prompt: str) -> Optional[Image.Image]:
    """Generate image and return as PIL Image object"""
    pipe = playground_manager.get_pipeline()

    try:
        image = pipe(
            prompt=prompt,
            num_inference_steps=20,
            guidance_scale=3.0,
            height=768,
            width=1344
        ).images[0]
        return image
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        return None

async def node_6_1_image_generation(state: PresentationState) -> PresentationState:
    """Generate images in-memory, store as bytes in state"""

    logger.info("Node 6.1: Generating images in-memory")

    theme = state.get("presentation_theme", "Professional Presentation")
    executive_summary = state.get("executive_summary", theme)

    # Store images as bytes in dictionary
    image_bytes = {}
    start_time = time.time()

    # 1. Title background
    logger.info("Generating TITLE SLIDE background...")
    title_prompt = f"""Professional background for a presentation about: {theme}. STYLE: {theme}.
    Not abstract. Visual representation of: {executive_summary}. Important no text needed! ABSOLUTELY NO TEXT, NO LETTERS, NO WORDS, NO TYPOGRAPHY.
    Clean corporate design, blue and white gradient, minimalist,
    professional, landscape 16:9, subtle relevant imagery, high quality, 4K"""

    title_img = await generate_image_memory(title_prompt)
    if title_img:
        # Convert PIL to bytes
        img_byte_arr = io.BytesIO()
        title_img.save(img_byte_arr, format='PNG')
        image_bytes["title_background"] = img_byte_arr.getvalue()
        logger.success("Title background ready (in-memory)")

    # 2. Content background
    logger.info("Generating CONTENT background...")
    content_prompt = f"NO TEXT. Content background for {theme}. Soft gradient, abstract shapes, landscape 16:9, clean"
    content_img = await generate_image_memory(content_prompt)
    if content_img:
        img_byte_arr = io.BytesIO()
        content_img.save(img_byte_arr, format='PNG')
        image_bytes["content_background"] = img_byte_arr.getvalue()
        logger.success("Content background ready (in-memory)")

    # 3. Thank you background
    logger.info("Generating THANK YOU SLIDE background...")
    thanks_prompt = f"""Professional  background for: {theme}. STYLE: {theme}. Important no text needed! ABSOLUTELY NO TEXT, NO LETTERS, NO WORDS, NO TYPOGRAPHY.
    Summary: {executive_summary}
    Not abstract. Visual metaphor for success and completion, warm elegant colors,
    subtle relevant imagery, no text, memorable, landscape 16:9,
    inspiring but not distracting, high quality"""
    thanks_img = await generate_image_memory(thanks_prompt)
    if thanks_img:
        img_byte_arr = io.BytesIO()
        thanks_img.save(img_byte_arr, format='PNG')
        image_bytes["thanks_background"] = img_byte_arr.getvalue()
        logger.success("Thank you background ready (in-memory)")

    elapsed = time.time() - start_time
    logger.success(f"Node 6.1 completed | {len(image_bytes)} images in memory | {elapsed:.1f}s")

    return {
        **state,
        "image_bytes": image_bytes,  
        "images_generated": len(image_bytes) > 0,
        "image_gen_time": elapsed
    }