import warnings
from core.state import AgenticState
import json
from loguru import logger


# Configuration
MODEL_NAME = "sshleifer/distilbart-cnn-12-6" 

@logger.catch
def load_bart_summarizer():

    """Load BART model with proper configuration"""

    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    warnings.filterwarnings("ignore")

    device = 0 if torch.cuda.is_available() else -1

    logger.info(f"The model {MODEL_NAME} is loaded", MODEL_NAME=MODEL_NAME)
    try:
        # Try pipeline first
        summarizer = pipeline(
            "summarization",
            model=MODEL_NAME,
            device=device,
            truncation=True
        )
        return summarizer
    except:
        # Fallback to direct model loading
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

        if device == 0:
            model = model.cuda()

        class BartSummarizer:
            def __init__(self, model, tokenizer, device):
                self.model = model
                self.tokenizer = tokenizer
                self.device = device

            def __call__(self, text, max_length=150, min_length=30, **kwargs):
                inputs = self.tokenizer(text, return_tensors="pt",
                                       truncation=True, max_length=1024)
                if self.device == 0:
                    inputs = {k: v.cuda() for k, v in inputs.items()}

                with torch.no_grad():
                    summary_ids = self.model.generate(
                        inputs['input_ids'],
                        max_length=max_length,
                        min_length=min_length,
                        num_beams=4,
                        early_stopping=True,
                        no_repeat_ngram_size=3,
                        **kwargs
                    )

                summary = self.tokenizer.decode(summary_ids[0],
                                               skip_special_tokens=True)
                return [{"summary_text": summary}]

        return BartSummarizer(model, tokenizer, device)


@logger.catch
def clean_summary_output(result):
    """Extract clean string from various response formats"""
    if isinstance(result, list) and len(result) > 0:
        if 'summary_text' in result[0]:
            return result[0]['summary_text']
        elif 'generated_text' in result[0]:
            return result[0]['generated_text']
        else:
            return str(result[0])
    elif isinstance(result, dict):
        return result.get('summary_text', result.get('generated_text', str(result)))
    else:
        return str(result)


@logger.catch
def synthesize_executive_summary(sections, summarizer):
    """Create a flowing executive summary from all sections"""
    # Collect all section summaries and key points
    all_content = []
    for section in sections:
        all_content.append(section.get('summary', ''))
        all_content.extend(section.get('key_points', []))

    combined = " ".join(all_content)[:2000]

    if not combined:
        logger.error("Node 5: No summary available")
        return "No summary available."
        

    # Create a prompt-like input for better summaries
    prompt = f"Summarize the following interview content: {combined}"

    try:
        result = summarizer(
            prompt,
            max_length=180,
            min_length=80,
            do_sample=False
        )
        return clean_summary_output(result)
    except:
        # Fallback to first section summary
        return sections[0].get('summary', 'Summary unavailable.')


@logger.catch
def generate_tldr(sections, summarizer):
    """Generate a concise one-sentence TL;DR"""
    # Use first section as base
    first_section = sections[0].get('summary', '')[:300]

    if not first_section:
        return "Video summary."

    try:
        result = summarizer(
            first_section,
            max_length=40,
            min_length=15,
            do_sample=False
        )
        tldr = clean_summary_output(result)

        # Ensure it's a complete sentence
        if not tldr.endswith(('.', '!', '?')):
            tldr += '.'
        return tldr
    except:
        return sections[0].get('title', 'Summary') + '.'


@logger.catch
def format_section_content(section, index, video_id):
    """Format a single section with proper structure"""
    title = section.get('title', f'Section {index}')
    title = title.replace('-', '').strip()
    if not title or len(title) < 5:
        title = f"Part {index}"
    
    summary = section.get('summary', 'No summary available.')
    if not summary.endswith(('.', '!', '?')):
        summary += '.'

    key_points = section.get('key_points', [])
    if not key_points:
        key_points = ["Key insights from this section"]

    points_formatted = "\n".join([f"- {p}" for p in key_points if p])

    # Explanation 
    explanation = section.get('explanation', section.get('content', ''))
    explanation_section = f"\n**Explanation**\n\n{explanation}\n" if explanation and len(explanation) > len(summary) else ""

    return f"""
### {index}. {title}

**Summary**

{summary}
{explanation_section}
**Key Insights**

{points_formatted}
"""


@logger.catch
async def node_5_beautiful_presentation(state: AgenticState) -> AgenticState:
    """ Node 5: Beautiful Presentation witg local model
    """
    logger.info("🚀 Node 5: Beautiful Presentation (Local) started...")

    import asyncio
    structured = getattr(state, "structured_script", {})
    
    # Get metadata directly from state attributes
    sections = structured.get("sections", [])

    if not sections:
        state.errors.append({"type": "missing_structure"})
        logger.error("Mode 5: Missing structure")

        return state

    # Get metadata directly from state attributes
    video_metadata = getattr(state, "video_metadata", {}) or {}

    video_id = (
        getattr(state, "video_id", None)
        or video_metadata.get("video_id")
        or "UNKNOWN"
    )

    title = (
        getattr(state, "title", None)
        or video_metadata.get("title")
        or (sections[0].get("title") if sections else None)
        or "YouTube Video Summary"
    )

    channel = (
        getattr(state, "channel", None)
        or video_metadata.get("channel")
        or "Unknown Channel"
    )

    duration_human = (
        getattr(state, "duration_human", None)
        or video_metadata.get("duration_human")
        or None
    )

    # Upload date
    upload_date = (
        getattr(state, "upload_date", None)
        or video_metadata.get("upload_date")
        or None
    )

    # Fallback to section title if needed
    if not title or title == "Unknown Title" or title == "YouTube Video Summary":
        if sections and len(sections) > 0:
            title = sections[0].get("title", "YouTube Video Summary")

    # Load summarizer
    loop = asyncio.get_event_loop()
    summarizer = await loop.run_in_executor(None, load_bart_summarizer)

    
    # Executive Summary - Synthesize all sections
    
    logger.info("   Generating executive summary...")
    exec_summary = await loop.run_in_executor(
        None, synthesize_executive_summary, sections, summarizer)

    
    # TL;DR - One sentence
    
    logger.info("   Generating TL;DR...")
    tldr = generate_tldr(sections, summarizer)

    
    # Main Topics - From structured data
    
    topics_md = ""
    topics = structured.get("main_topics", [])
    if topics:
        # Clean topics
        clean_topics = [t.strip() for t in topics if t and len(t) > 3]
        if clean_topics:
            topics_md = "## Main Topics\n\n"
            topics_md += "\n".join(f"- {t}" for t in clean_topics[:8])

    
    # Table of Contents
    
    toc = "## Table of Contents\n\n"
    for i, sec in enumerate(sections, 1):
        title_text = sec.get('title', f'Section {i}')
        clean_title = title_text.replace('-', '').strip()
        if clean_title and not clean_title.startswith('The following'):
            toc += f"{i}. {clean_title}\n"

    
    # Sections - Properly formatted
    
    logger.info("   Formatting {sections} sections...", sections=len(sections))
    sections_md = []
    for i, sec in enumerate(sections, 1):
        sections_md.append(format_section_content(sec, i, video_id))

    
    # Quotes - Clean and deduplicate
    
    quotes_md = ""
    quotes = structured.get("key_quotes", [])
    if quotes:
        # Clean quotes
        clean_quotes = []
        for q in quotes:
            if q and len(q) > 10:
                # Remove any surrounding quotes
                q = q.strip('"').strip()
                if q not in clean_quotes:
                    clean_quotes.append(q)

        if clean_quotes:
            quotes_md = "## Key Quotes\n\n"
            for q in clean_quotes[:6]:
                quotes_md += f'> "{q}"\n\n'

    
    # Entities - Clean and sort
    
    entities_md = ""
    entities = structured.get("mentioned_entities", [])
    if entities:
        # Clean and deduplicate
        clean_entities = []
        for e in entities:
            if e and len(e) > 1:
                # Remove duplicates and clean
                if e not in clean_entities:
                    clean_entities.append(e)

        if clean_entities:
            entities_md = "## Key Mentions\n\n"
            for ent in sorted(clean_entities)[:20]:
                entities_md += f"- {ent}\n"

    
    # Final Markdown
    
    final_md = f"""# {title}

*Channel: {channel}*  
*Video ID: {video_id}*  
*Duration: {duration_human}*  
*Updated: {upload_date}*


---

## Executive Summary
{exec_summary}

## TL;DR
{tldr}

---

{topics_md}

---

{toc}

---

{chr(10).join(sections_md)}

---

{quotes_md}

---

{entities_md}

---

*Generated with YouTubeScriptMaster (Local AI Mode)*
"""

    # Clean up any remaining formatting issues
    final_md = final_md.replace('  ', ' ').replace('\n\n\n', '\n\n')

    state.final_formatted_markdown = final_md
    state.presentation_complete = True

    logger.info("✅ Node 5 complete")



    quotes_count = len(clean_quotes) if 'clean_quotes' in locals() else 0
    entities_count = len(clean_entities) if 'clean_entities' in locals() else 0

    logger.info(f"   Sections: {len(sections_md)}")
    logger.info(f"   Executive summary: {exec_summary[:100] if exec_summary else ''}...")
    logger.info(f"   TL;DR: {tldr}")
    logger.info(f"   Quotes: {quotes_count}")
    logger.info(f"   Entities: {entities_count}")

    return state