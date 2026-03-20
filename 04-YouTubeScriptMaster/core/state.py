from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document





class AgenticState(BaseModel):
    """
    Unified state for the YouTube Script Extraction Pipeline
    """
    
    # Initial Fields
    
    youtube_url: str = Field(..., description="Raw YouTube URL provided by user")
    
    llm: Optional[Any] = None 
    
    # Node 1
    
    video_id: str = Field(default="", description="Extracted YouTube video ID (11 chars)")
    title: str = Field(default="Unknown", description="Video title")
    channel: str = Field(default="Unknown", description="Channel name or handle")
    upload_date: Optional[str] = Field(None, description="Upload date (YYYY-MM-DD)")
    duration_seconds: Optional[int] = Field(None, description="Duration in seconds")
    duration_human: Optional[str] = Field(None, description="Pretty duration (e.g. 4:20)")
    has_manual_captions: str = Field("unknown", description="yes / no / auto-only / unknown")
    language: str = Field("unknown", description="Primary language code")
    is_live: bool = Field(False, description="Is or was a live stream")
    best_transcript_source: str = Field("unknown", description="Recommended method: youtube-builtin / api / yt-dlp / whisper-fallback")
    source_confidence: float = Field(0.0, description="Confidence in best source (0.0–1.0)")
    extraction_warnings: List[str] = Field(default_factory=list, description="Warnings from metadata extraction")
    metadata_ready: bool = Field(False, description="Whether metadata is complete")

    
    # Node 2
    
    raw_transcript_text: str = Field(default="", description="Raw transcript text with timestamps if available")
    transcript_source: str = Field(default="unknown", description="Which method won: youtube-transcript-api, etc.")
    transcript_language: str = Field(default="unknown", description="Detected transcript language code")
    has_timestamps: bool = Field(False, description="Does raw transcript have timestamps?")
    confidence_score: float = Field(0.0, description="Estimated transcript quality (0.0–1.0)")
    next_extraction_strategy: Optional[str] = Field(None, description="Recommended next extraction strategy from Node 1")

    use_api_for_structuring: bool = Field(True)
    use_api_for_presentation: bool = Field(True) # Node 5: True -> API

    
    # Node 3
    
    cleaned_transcript: str = Field(default="", description="Cleaned transcript text")
    speaker_segments: Optional[List[Dict[str, Any]]] = Field(None, description="List of speaker segments if detected")
    cleaned_timestamp_map: Optional[List[Dict[str, Any]]] = Field(None, description="Normalized timestamps map")

    
    # Node 4
    
    structured_script: Dict[str, Any] = Field(default_factory=dict, description="Nested dict of sections with title, start_time, content, summary, key_points")
    chapter_list: List[Dict[str, Any]] = Field(default_factory=list, description="List of chapters with timestamps")
    key_quotes: List[str] = Field(default_factory=list, description="Extracted key quotes")
    mentioned_entities: List[str] = Field(default_factory=list, description="Extracted named entities")
    main_topics: List[str] = Field(default_factory=list, description="Main topics")



    key_statistics: List[str] = Field(default_factory=list, description="Detected statistics")


    
    # Node 5
    
    final_formatted_markdown: Optional[str] = Field(None, description="Final beautiful markdown output")
    json_export: Optional[Dict[str, Any]] = Field(None, description="Optional JSON export of structured data")
    presentation_complete: bool = Field(False, description="Whether presentation is complete")

    
    # Pipeline Control & Errors
    
    documents: List[Document] = Field(default_factory=list, description="Any document objects")
    errors: List[Dict[str, str]] = Field(default_factory=list, description="List of errors")
    processed_count: int = Field(default=0, description="Number of processed items")