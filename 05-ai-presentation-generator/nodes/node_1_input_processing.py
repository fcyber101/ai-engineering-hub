import re
from loguru import logger

from core.state import PresentationState


def node_1_input_processing(state: PresentationState) -> PresentationState:
    """Split text into safe chunks for LLM"""
    raw_text = state.get("raw_text", "").strip()

    if not raw_text:
        logger.warning("Node 1: Empty raw_text")
        return {**state, "cleaned_text": "", "text_chunks": []}

    # Clean text
    text = re.sub(r'\n\s*\n+', '\n\n', raw_text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove noise
    noise_patterns = [
        r'(?i)disclaimer:.*?(?=\n\n|\Z)',
        r'(?i)copyright \d{4}.*?(?=\n\n|\Z)',
        r'\[.*?\]',
        r'http\S+',
    ]
    for pattern in noise_patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL)

    text = re.sub(r'\n{3,}', '\n\n', text)

    # Chunk by size 
    MAX_CHUNK_SIZE = 4000
    chunks = []

    # Split by paragraphs first
    paragraphs = text.split('\n\n')

    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 > MAX_CHUNK_SIZE:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    logger.info(f"Node 1: Created {len(chunks)} chunks")
    for i, c in enumerate(chunks):
        logger.debug(f"  Chunk {i+1}: {len(c)} chars, ~{len(c)//4} tokens")

    logger.success(f"Node 1 | {len(chunks)} chunks | {len(raw_text)} chars")

    return {
        **state,
        "cleaned_text": chunks[0] if chunks else "",
        "text_chunks": chunks
    }