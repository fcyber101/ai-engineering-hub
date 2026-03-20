from core.state import AgenticState
import json
from loguru import logger


@logger.catch
async def node_5_beautiful_presentation_api(state: AgenticState) -> AgenticState:
    """
    Node 5 Prepare nice presentation with API
    """


    logger.info("🚀 Node 5: Beautiful Presentation started...")

    llm = state.llm 
    if not llm:
        state.errors.append("LLM not available in state")
        logger.error("LLM not available in state")
        return state

    structured = getattr(state, "structured_script", {})
    metadata = getattr(state, "video_metadata", {})

    if not structured:
        state.errors.append({"type": "missing_structure", "message": "No structured script"})
        logger.error("No structured script")
        return state

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
    # Build summary prompt
    content_sample = "\n".join(
        sec.get("summary", "") for sec in structured.get("sections", [])
    )[:3000]

    prompt = f"""
You are a professional content summarizer.

Generate:

1. Executive summary (3-5 sentences)
2. TLDR (one powerful sentence)

Return JSON:

{{
 "executive_summary": "...",
 "tldr": "..."
}}

CONTENT:
{content_sample}
"""

    try:
        response = llm.invoke(prompt)

        json_str = response.content if hasattr(response, "content") else str(response)

        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()

        summaries = json.loads(json_str)

        exec_summary = summaries.get("executive_summary", "")
        tldr = summaries.get("tldr", "")

    except Exception as e:
        state.errors.append({"type": "summary_failed", "message": str(e)})
        exec_summary = "Summary unavailable."
        tldr = "TLDR unavailable."
        logger.error("Summary unavailable")

    # Table of contents
    toc = "## Table of Contents\n"
    for i, sec in enumerate(structured.get("sections", []), 1):
        toc += f"{i}. {sec.get('title','Section')}\n"

    # Sections
    sections_md = []

    for i, sec in enumerate(structured.get("sections", []), 1):

        title_sec = sec.get("title", f"Section {i}")
        summary = sec.get("summary", "")
        content = sec.get("content", "")
        key_points = sec.get("key_points", [])
        start_time = sec.get("start_time")

        timestamp = f"⏱ {start_time}\n\n" if start_time else ""

        section_md = f"""

### {i}. {title_sec}

{timestamp}

**Summary**

{summary}

**Explanation**

{content}

**Key Insights**

{chr(10).join(f"- {p}" for p in key_points[:5])}


"""

        sections_md.append(section_md)

    # Topics
    topics_md = ""
    if state.main_topics:
        topics_md = "## Main Topics\n" + "\n".join(f"- {t}" for t in state.main_topics)

    # Quotes
    quotes_md = ""
    if state.key_quotes:
        quotes_md = "## Key Quotes\n\n"  
        for q in state.key_quotes:
            quotes_md += f'> "{q}"\n\n'  

    # Entities 
    entities_md = ""
    if state.mentioned_entities:
        entities_md = "## Key Mentions\n\n"  
        for e in state.mentioned_entities:
            entities_md += f"- {e}\n"  

    final_md = f"""
# {title}

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

*Generated with Groq API + YouTubeScriptMaster 2026*
"""

    state.final_formatted_markdown = final_md
    state.presentation_complete = True

    logger.info(" ✅ Node 5 complete | Markdown size: {len_final_md}", len_final_md=len(final_md))

    return state