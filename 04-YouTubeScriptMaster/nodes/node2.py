

from youtube_transcript_api import YouTubeTranscriptApi
from core.state import AgenticState
import asyncio
from loguru import logger


@logger.catch
async def node_2_transcript_extraction(state: AgenticState) -> AgenticState:
    """
    Node 2
    Extract transcript from YouTube using youtube-transcript-api
    """

    logger.info("🚀 Node 2: Transcript Extraction started...")

    video_id = state.video_id

    try:
        # Running the blocking API call in a thread pool
        transcript = await asyncio.to_thread(
            lambda vid: YouTubeTranscriptApi().fetch(vid, languages=["en", "de"]),
            video_id
        )

        # Convert subtitle segments to clean text
        segments = []

        for snippet in transcript:
            text = snippet.text.strip()

            # Remove newline artifacts inside subtitles
            text = text.replace("\n", " ")

            segments.append(text)

        transcript_text = " ".join(segments)

        state.raw_transcript_text = transcript_text
        state.transcript_source = "youtube_transcript_api"

        logger.info("✅ Node 2 Complete")
        logger.info(
            "✅ Node 2: Transcript extracted | chars={char_count}",
            char_count=len(transcript_text)
        )

    except Exception as e:
        logger.opt(exception=e, diagnose=False).error("Transcript extraction failed")
        state.raw_transcript_text = ""
        state.transcript_source = "failed"

    return state




