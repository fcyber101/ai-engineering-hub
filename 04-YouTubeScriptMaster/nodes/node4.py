import json
import re


from core.state import AgenticState
from loguru import logger


@logger.catch
async def node_4_intelligent_structuring_api(state: AgenticState) -> AgenticState:

    logger.info("🚀 Node 4: Intelligent Structuring started")

    transcript = state.cleaned_transcript or ""
    

    
    # Debug: Check if state has other expected fields
    logger.info(f"   - State summary: url={state.youtube_url}, transcript_len={len(state.cleaned_transcript)}")

    # Or convert to dict with safe values
    safe_state = {
        "youtube_url": state.youtube_url,
        "video_id": state.video_id,
        "transcript_len": len(state.cleaned_transcript),
        "use_api": state.use_api_for_structuring
    }
    logger.info(f"   - State: {safe_state}")
    
    # Debug: Check for errors in state
    if isinstance(state, dict):
        errors = state.get('errors', [])

    else:
        errors = getattr(state, 'errors', [])
    
    if errors:
        logger.error("⚠️ Existing errors in state")
        for i, error in enumerate(errors):
            logger.error(
                "Node 4: Existing error #{i} → {msg}",
                i=i,
                msg=error.get("message", str(error)) if isinstance(error, dict) else str(error)
            )


    


    if not transcript:
        state.errors.append({"type": "no_transcript"})
        logger.error("Node 4: ⚠️ No transcript")
        return state


    llm = state.llm 
    if not llm:
        state.errors.append("LLM not available in state")
        logger.error("Node 4: LLM not available in state")
        return state
    
    # Config
    

    MODEL_LIMIT = 7500 # Save zone
    PROMPT_TOKENS = 1800
    CHARS_PER_TOKEN = 3.5

    MAX_CHARS = int((MODEL_LIMIT - PROMPT_TOKENS) * CHARS_PER_TOKEN)

    OVERLAP = 800
    MAX_CHUNKS = 40


    
    # Save json parse
    

    def safe_json(text):

        if "```" in text:
            parts = text.split("```")
            text = parts[1]
            if text.startswith("json"):
                text = text[4:]

        text = text.strip()

        try:
            return json.loads(text)
        except:
            # fallback extraction
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise


    
    # Save chunking
    

    logger.info("Creating chunks")

    chunks = []

    pos = 0
    length = len(transcript)

    while pos < length and len(chunks) < MAX_CHUNKS:

        end = min(pos + MAX_CHARS, length)

        if end < length:

            boundary = transcript.rfind(". ", pos, end)

            if boundary != -1 and boundary > pos:
                end = boundary + 2

        chunk = transcript[pos:end]

        chunks.append(chunk)

        new_pos = end - OVERLAP

        if new_pos <= pos:
            new_pos = end

        pos = new_pos

    logger.info("   chunks created: {chunk_count}", chunk_count=len(chunks))


    
    # Map step
    

    chunk_summaries = []
    sections = []
    quotes = []
    entities = []
    topics = []

    for i, chunk in enumerate(chunks):

        logger.info(
            "   analyzing chunk {current}/{total}",
            current=i + 1,
            total=len(chunks)
        )

        prompt = f"""
You are analyzing a segment of a long podcast transcript.

Extract meaningful structure and ideas.

Return JSON only.

{{
 "chunk_summary":"4-5 sentence explanation of the main ideas",
 "sections":[
  {{
   "title":"descriptive section title",
   "summary":"3 sentence explanation",
   "key_points":[
    "important insight",
    "important insight",
    "important insight",
    "important insight"
   ]
  }}
 ],
 "quotes":["memorable quote from speaker"],
 "entities":["people companies technologies books"],
 "topics":["specific conceptual topics discussed"]
}}

Rules:
- focus on meaningful ideas
- avoid generic phrases
- insights must be specific
- section titles must describe the topic

TRANSCRIPT:
{chunk}
"""

        try:

            response = llm.invoke(prompt)

            text = response.content if hasattr(response,"content") else str(response)

            data = safe_json(text)

        except Exception as e:

            logger.opt(exception=e).error("Node 4: ⚠️ chunk failed")
            continue


        chunk_summaries.append(data.get("chunk_summary",""))

        sections.extend(data.get("sections",[]))
        quotes.extend(data.get("quotes",[]))
        entities.extend(data.get("entities",[]))
        topics.extend(data.get("topics",[]))


    
    # Global reduce
    

    logger.info("Building global structure")

    summary_text = "\n".join(chunk_summaries[:30])

    reduce_prompt = f"""
These are summaries of segments from a long podcast.

{summary_text}

Your task:

Create the GLOBAL structure of the full conversation.

Return JSON:

{{
 "executive_summary":"8 sentence explanation of the entire episode",

 "sections":[
  {{
   "title":"section title",
   "summary":"4 sentence summary",
   "key_points":[
    "insight",
    "insight",
    "insight",
    "insight"
   ]
  }}
 ]
}}

Rules:
- produce 8 to 12 sections
- titles must reflect the real discussion topics
- insights must be concrete and specific
"""

    try:

        response = llm.invoke(reduce_prompt)

        text = response.content if hasattr(response,"content") else str(response)

        data = safe_json(text)

        final_sections = data.get("sections",[])[:14]
        executive_summary = data.get("executive_summary","")

    except Exception as e:


        logger.opt(exception=e).error("Node 4: ⚠️ reduce step failed")

        final_sections = sections[:14]
        executive_summary = ""


    
    # Deput helper
    

    def dedup(lst, limit):

        out = []

        for x in lst:

            x = str(x).strip()

            if not x:
                continue

            if x not in out:
                out.append(x)

            if len(out) >= limit:
                break

        return out


    def dedup_quotes(qs):

        out = []

        for q in qs:

            q = str(q).strip()

            if len(q) < 20:
                continue

            duplicate = False

            for e in out:

                w1 = set(q.lower().split())
                w2 = set(e.lower().split())

                if w1 and w2:

                    overlap = len(w1 & w2) / max(len(w1), len(w2))

                    if overlap > 0.75:
                        duplicate = True
                        break

            if not duplicate:
                out.append(q)

            if len(out) >= 10:
                break

        return out


    
    # Topic consolidation
    

    topics = dedup(topics, 30)

    topic_prompt = f"""
These are topics extracted from a podcast.

{topics}

Group and consolidate them into the 12 most important conceptual topics.

Return JSON:

{{
 "topics":["topic","topic","topic"]
}}
"""

    try:

        response = llm.invoke(topic_prompt)

        text = response.content if hasattr(response,"content") else str(response)

        data = safe_json(text)

        topics = data.get("topics", topics)

    except:

        topics = topics


    
    # Final structure
    

    structured = {

        "executive_summary": executive_summary,

        "sections": final_sections,

        "chapter_list":[
            {"title": s["title"], "start_time": None}
            for s in final_sections
        ],

        "key_quotes": dedup_quotes(quotes),

        "mentioned_entities": dedup(entities, 30),

        "main_topics": topics
    }


    
    # Write state
    

    state.structured_script = structured
    state.chapter_list = structured["chapter_list"]
    state.key_quotes = structured["key_quotes"]
    state.mentioned_entities = structured["mentioned_entities"]
    state.main_topics = structured["main_topics"]


    logger.info("\n✅ Node 4 finished")

    logger.info("   Sections: {count}", count=len(structured["sections"]))
    logger.info("   Quotes: {count}", count=len(structured["key_quotes"]))
    logger.info("   Topics: {count}", count=len(structured["main_topics"]))
    logger.info("   Entities: {count}", count=len(structured["mentioned_entities"]))

    return state