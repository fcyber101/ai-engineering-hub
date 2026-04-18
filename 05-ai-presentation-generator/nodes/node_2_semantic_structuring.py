
from loguru import logger
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import re
import asyncio
from collections import Counter

from core.state import PresentationState
from config.settings import get_llm


class SimpleSection(BaseModel):
    title: str = Field(..., description="Section title")
    points: List[str] = Field(default_factory=list, description="Key points")
    importance: int = Field(3, ge=1, le=5)
    type: str = Field("background", description="problem/solution/evidence/case_study/background/conclusion")
    summary: str = Field("", description="2-3 sentence summary")

class ChunkResult(BaseModel):
    sections: List[SimpleSection] = Field(default_factory=list)
    summary: str = Field("", description="Executive summary for this chunk")
    theme: str = Field("General", description="Theme for this chunk")



async def process_chunk(chunk_text: str, chunk_num: int, total: int) -> ChunkResult:
    """Process one text chunk and return structured data"""

    logger.info(f"  Processing chunk {chunk_num}/{total} ({len(chunk_text)} chars)")

    llm = get_llm(temperature=0.3)

    prompt = f"""Extract EVERY important detail from this text. Create RICH, DETAILED sections.

TEXT CHUNK:
{chunk_text[:4000]}

Return ONLY valid JSON with this structure:
{{
  "sections": [
    {{
      "title": "Clear, descriptive title",
      "points": [
        "First specific insight with details",
        "Second important point with context",
        "Third key takeaway with examples",
        "Fourth supporting point",
        "Fifth actionable insight",
        "Sixth relevant detail",
        "Seventh connection to other ideas",
        "Eighth practical implication",
        "Ninth statistic or evidence",
        "Tenth concluding point"
      ],
      "importance": 5,
      "type": "solution",
      "summary": "7-10 sentence comprehensive summary that explains the concept thoroughly, includes specific examples, discusses implications, provides context, connects to broader themes, and ends with actionable takeaways."
    }}
  ],
  "summary": "8-10 sentence overall synthesis of ALL sections. Capture the complete narrative, highlight every major insight, connect related concepts, and provide comprehensive conclusions.",
  "theme": "Powerful 3-5 word theme"
}}

CRITICAL RULES:
- Extract 8-15 key points PER SECTION (be VERY thorough!)
- Write 7-10 sentences PER SECTION SUMMARY
- Write 8-10 sentences for the OVERALL SUMMARY
- Include specific examples, numbers, statistics from text
- Use importance=5 for critical insights, 4 for important ones
- BE GENEROUS with points - if text has details, ADD THEM

DO NOT be brief. DO NOT skip details. EXTRACT EVERYTHING valuable.

Return ONLY valid JSON. Make it RICH and COMPREHENSIVE!"""

    try:
        response = await llm.ainvoke(prompt)

        # Clean markdown code blocks
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        # Extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())

            sections = []
            for s in data.get('sections', []):
                sections.append(SimpleSection(
                    title=s.get('title', 'Untitled'),
                    points=s.get('points', []),
                    importance=s.get('importance', 3),
                    type=s.get('type', 'background'),
                    summary=s.get('summary', '')
                ))

            # Log richness
            total_points = sum(len(s.points) for s in sections)
            logger.info(f"Extracted {len(sections)} sections with {total_points} points")

            return ChunkResult(
                sections=sections,
                summary=data.get('summary', ''),
                theme=data.get('theme', 'General')
            )
    except Exception as e:
        logger.warning(f"Chunk {chunk_num} failed: {e}")

    return ChunkResult()


def merge_results(results: List[ChunkResult]) -> dict:
    """Merge all chunk results into final output"""

    all_sections = []
    all_points = []
    themes = []
    summaries = []

    for r in results:
        all_sections.extend(r.sections)
        if r.theme and r.theme != "General":
            themes.append(r.theme)
        if r.summary:
            summaries.append(r.summary)

    # Flatten all points
    for section in all_sections:
        for point in section.points:
            all_points.append({
                "point": point,
                "importance": section.importance
            })

    # Most common theme
    theme = "General Presentation"
    if themes:
        theme = Counter(themes).most_common(1)[0][0]

    # Best summary
    if summaries:
        exec_summary = max(summaries, key=len)
    else:
        exec_summary = "Key insights from the presentation."

    # Convert to state format
    structured_sections = []
    for s in all_sections:
        structured_sections.append({
            "section_title": s.title,
            "key_points": s.points,
            "importance": s.importance,
            "section_type": s.type,
            "hierarchy_level": 1,
            "relationships": None,
            "section_summary": s.summary
        })

    logger.info(f"Merged: {len(structured_sections)} sections, {len(all_points)} points")

    return {
        "structured_sections": structured_sections,
        "refined_key_points": all_points,
        "executive_summary": exec_summary,
        "presentation_theme": theme,
        "audience_type": "mixed",
        "total_insights": len(structured_sections)
    }



async def node_2_semantic_structuring(state: PresentationState) -> PresentationState:
    """Process all chunks and merge results"""

    logger.info("Node 2: Starting semantic structuring")

    # Get chunks from state
    chunks = state.get("text_chunks", [])
    if not chunks:
        chunks = [state.get("cleaned_text", "")]

    if not chunks or not chunks[0]:
        logger.warning("No text to process")
        return {
            **state,
            "structured_sections": [],
            "refined_key_points": [],
            "executive_summary": "No content provided.",
            "presentation_theme": "General",
            "audience_type": "mixed",
            "total_insights": 0
        }

    logger.info(f"Processing {len(chunks)} chunks...")

    # Process all chunks
    results = []
    for i, chunk in enumerate(chunks):
        if chunk.strip():
            result = await process_chunk(chunk, i+1, len(chunks))
            results.append(result)
            # Small delay to avoid rate limits
            await asyncio.sleep(0.5)

    # Merge results
    if results:
        merged = merge_results(results)
    else:
        logger.error("No chunks processed successfully")
        merged = {
            "structured_sections": [],
            "refined_key_points": [],
            "executive_summary": "Failed to process content.",
            "presentation_theme": "General",
            "audience_type": "mixed",
            "total_insights": 0
        }

    logger.success(f"Node 2 completed | {merged['total_insights']} sections | {len(merged['refined_key_points'])} points | Theme: {merged['presentation_theme']}")

    return {
        **state,
        **merged
    }