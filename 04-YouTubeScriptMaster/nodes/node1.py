import re
from urllib.parse import urlparse, parse_qs
from datetime import datetime


import yt_dlp
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)
from loguru import logger
from core.state import AgenticState


@logger.catch
async def node_1_video_metadata_and_source_detection(state: AgenticState) -> AgenticState:
    """
    Node 1: YouTube Metadata + Transcript Source Detection
    """

    logger.info("🚀 Node 1: Video Metadata & Source Detection")

    url = getattr(state, "youtube_url", None)

    if not url:
        state.errors.append({
            "type": "invalid_input",
            "message": "Missing YouTube URL"
        })
        return state

    
    # Extract Video ID
    

    video_id = None

    try:
        parsed = urlparse(url)

        if "youtu.be" in parsed.netloc:
            video_id = parsed.path.lstrip("/")

        elif "youtube.com" in parsed.netloc:
            video_id = parse_qs(parsed.query).get("v", [None])[0]

        if not video_id or not re.match(r"^[a-zA-Z0-9_-]{11}$", video_id):
            raise ValueError("Invalid YouTube video ID")

        state.video_id = video_id
        logger.info("   ✓ Video ID: {video_id}", video_id=video_id)

    except Exception as e:
        state.errors.append({
            "type": "url_parse_failed",
            "message": str(e)
        })
        logger.opt(exception=e, diagnose=False).error("Url parse failed")
        return state

    
    # Metadata Extraction (yt-dlp)
    

    try:

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        state.title = info.get("title")
        state.channel = info.get("channel")
        state.duration_seconds = info.get("duration")
        state.is_live = info.get("is_live", False)

        upload = info.get("upload_date")

        if upload:
            state.upload_date = datetime.strptime(upload, "%Y%m%d").date().isoformat()
        else:
            state.upload_date = None

        if state.duration_seconds:
            mins, sec = divmod(state.duration_seconds, 60)
            hrs, mins = divmod(mins, 60)

            if hrs:
                state.duration_human = f"{hrs}h {mins}m {sec}s"
            else:
                state.duration_human = f"{mins}m {sec}s"

        logger.info("   ✓ Metadata extracted")

    except Exception as e:

        state.extraction_warnings.append(
            f"Metadata extraction failed: {str(e)[:120]}"
        )
        logger.opt(exception=e, diagnose=False).error("Metadata extraction failed")

        state.title = "Unknown"
        state.channel = "Unknown"
        state.duration_seconds = None
        state.duration_human = None
        state.upload_date = None
        state.is_live = False

    
    # Caption Detection
    

    try:

        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        transcripts = list(transcript_list)

        manual = [t for t in transcripts if not t.is_generated]
        generated = [t for t in transcripts if t.is_generated]

        if manual:

            state.has_manual_captions = "yes"
            state.language = manual[0].language_code

        elif generated:

            state.has_manual_captions = "auto-only"
            state.language = generated[0].language_code

        else:

            state.has_manual_captions = "no"
            state.language = "unknown"

        logger.info("   ✓ Captions: {has_manual_captions} ({language})", has_manual_captions=state.has_manual_captions, language=state.language)

    except TranscriptsDisabled:

        state.has_manual_captions = "no"
        state.language = "unknown"
        state.extraction_warnings.append("Captions disabled")

    except NoTranscriptFound:

        state.has_manual_captions = "no"
        state.language = "unknown"
        state.extraction_warnings.append("No transcripts available")

    except Exception as e:

        state.has_manual_captions = "unknown"
        state.language = "unknown"

        state.extraction_warnings.append(
            f"Caption check failed: {str(e)[:120]}"
        )
        logger.opt(exception=e, diagnose=False).error("Caption check failed")
    
    # Decide Best Transcript Source
    

    if state.is_live:

        state.best_transcript_source = "none"
        state.source_confidence = 0.0

        state.extraction_warnings.append(
            "Live streams usually have no transcripts"
        )

    elif state.has_manual_captions == "yes":

        state.best_transcript_source = "youtube_manual"
        state.source_confidence = 0.95

    elif state.has_manual_captions == "auto-only":

        state.best_transcript_source = "youtube_auto"
        state.source_confidence = 0.80

    else:

        state.best_transcript_source = "whisper"
        state.source_confidence = 0.60

        state.extraction_warnings.append(
            "No captions → Whisper fallback recommended"
        )

    
    # Control Flags
    

    state.metadata_ready = True
    state.next_extraction_strategy = state.best_transcript_source

    
    # Logging
    

    logger.info("✅ Node 1 Complete")
    logger.info("   Title: {title}", title=state.title)
    logger.info("   Channel: {channel}", channel=state.channel)
    logger.info("   Duration: {duration_human}", duration_human=state.duration_human)
    logger.info("   Captions: {has_manual_captions}", has_manual_captions=state.has_manual_captions)
    logger.info("   Language: {language}", language=state.language)
    logger.info("   Source: {best_transcript_source}", best_transcript_source=state.best_transcript_source)
    logger.info("   Confidence: {source_confidence}", source_confidence=state.source_confidence)

    if state.extraction_warnings:
            logger.warning("   Warnings: {count} warnings", count=len(state.extraction_warnings))
            for warning in state.extraction_warnings:
                logger.warning("      - {warning}", warning=warning)

    return state