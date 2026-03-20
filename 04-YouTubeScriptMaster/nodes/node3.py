import re
from core.state import AgenticState
from loguru import logger



def ts_to_seconds(ts: str) -> int:
    m, s = ts.split(":")
    return int(m) * 60 + int(s)



@logger.catch
async def node_3_transcript_cleaning_and_normalization(state: AgenticState) -> AgenticState:
    """
    Node 3: Transcript Cleaning & Normalization
    """

    logger.info("🚀 Node 3: Cleaning transcript...")

    raw_text = state.raw_transcript_text

    if not raw_text:
        state.errors.append(
            {"type": "missing_transcript", "message": "No raw transcript from Node 2"}
        )
        logger.error("No raw transcript from Node 2")

        return state

    cleaned = raw_text

    # Remove noise
    cleaned = re.sub(r"\[(music|applause|laughter)\]", "", cleaned, flags=re.IGNORECASE)

    # Fix repeated punctuation
    cleaned = re.sub(r"[.!?]{2,}", ".", cleaned)

    # Common ASR corrections
    fixes = {
        "gonna": "going to",
        "wanna": "want to",
        "kinda": "kind of",
        "ya": "you",
    }

    for wrong, right in fixes.items():
        cleaned = re.sub(rf"\b{wrong}\b", right, cleaned, flags=re.IGNORECASE)

    lines = cleaned.split("\n")

    cleaned_lines = []
    timestamp_map = []
    speaker_segments = []

    current_speaker = "Unknown"
    segment_start = 0

    timestamp_pattern = re.compile(r"\[(\d+:\d+)\s*-\s*(\d+:\d+)\]")

    for i, line in enumerate(lines):

        line = line.strip()

        if not line:
            continue

        ts_match = timestamp_pattern.match(line)

        if ts_match:

            start_ts = ts_match.group(1)
            end_ts = ts_match.group(2)

            start_sec = ts_to_seconds(start_ts)
            end_sec = ts_to_seconds(end_ts)

            timestamp_map.append(
                {
                    "start": start_sec,
                    "end": end_sec,
                    "pretty": f"{start_ts}-{end_ts}",
                }
            )

            line = line[ts_match.end():].strip()

        speaker_match = re.match(r"([A-Z][a-zA-Z ]{2,}):", line)

        if speaker_match:

            speaker = speaker_match.group(1).strip()

            if speaker != current_speaker:

                speaker_segments.append(
                    {
                        "speaker": current_speaker,
                        "start_line": segment_start,
                        "end_line": i - 1,
                    }
                )

                current_speaker = speaker
                segment_start = i

            line = line[speaker_match.end():].strip()

        cleaned_lines.append(line)

    if cleaned_lines:
        speaker_segments.append(
            {
                "speaker": current_speaker,
                "start_line": segment_start,
                "end_line": len(cleaned_lines) - 1,
            }
        )

    cleaned_transcript = "\n".join(cleaned_lines)

    state.cleaned_transcript = cleaned_transcript
    state.cleaned_timestamp_map = timestamp_map
    state.speaker_segments = speaker_segments

    logger.info(
        "✅ Node 3 complete | chars={char_count} | segments={segment_count}",
        char_count=len(cleaned_transcript),
        segment_count=len(speaker_segments)
    )

    return state


