# Core Processing Engine

The core of the system is the `VideoProcessor` class that coordinates the entire video editing workflow.

## VideoProcessor Class (`processor.py`)

**Main Responsibilities**:
- Coordinates the entire video processing workflow
- Manages temporary files and cleanup
- Provides both analysis and processing capabilities
- Handles error conditions and edge cases

**Key Methods**:

**analyze_video()**:
- Takes a video file path and returns comprehensive analysis results
- Extracts video duration using FFmpeg
- Uses `AudioProcessor` to extract audio and perform Whisper AI transcription
- Intelligently detects silence periods based on speech transcription (gaps between words)
- Calculates estimated output duration and silence reduction percentage
- Returns a `VideoAnalysis` object with transcript segments and silence analysis

**process_video()**:
- Takes input and output file paths for video processing
- Uses `AudioProcessor` for Whisper AI transcription and intelligent silence detection
- Identifies silence periods as gaps between transcribed speech segments
- Leverages `VideoSegmentProcessor` to extract precise speech segments based on transcript timing
- Creates final output by concatenating only segments containing actual speech
- Preserves ambient audio and background sounds while removing true silence
- Returns the path to the intelligently processed video file

## Supporting Classes

**VideoAnalysis** (`processing/models.py`):
- Comprehensive data structure holding detailed analysis results
- Contains original duration, intelligently detected silence periods, and estimated output
- Includes transcript segments with word-level timing from Whisper AI
- Provides calculated reduction percentage and transcript data for user feedback

**Context Management**:
- Implements context manager protocol (`__enter__`/`__exit__`)
- Automatically creates and cleans up temporary directories
- Ensures no leftover files after processing

## Processing Flow

**Analysis Phase**:
1. Probe video file to get duration information using FFmpeg
2. Extract audio track to temporary WAV file for processing
3. Perform Whisper AI transcription to identify actual speech segments with precise word-level timing
4. Intelligently detect silence as gaps between transcribed speech segments
5. Calculate comprehensive statistics including transcript-based silence reduction

**Processing Phase**:
1. Extract audio for Whisper AI transcription and analysis
2. Use transcript data to identify precise speech segments and true silence periods
3. Leverage VideoSegmentProcessor to extract video segments based on transcript timing
4. Concatenate only segments containing actual speech, preserving ambient audio
5. Generate final output video with intelligent silence removal
6. Clean up temporary files and maintain transcript data for user reference

## Integration Points

- **Configuration**: Uses `Config` class for Whisper AI settings and processing parameters
- **Audio Processing**: Delegates to `AudioProcessor` for Whisper transcription and intelligent silence detection
- **Video Processing**: Uses `VideoSegmentProcessor` for precise transcript-based segment extraction
- **Whisper AI**: Leverages OpenAI Whisper for accurate speech-to-text with word-level timestamps
- **FFmpeg**: Utilizes FFmpeg for audio extraction, video probing, and format processing
- **File Management**: Handles temporary file creation, cleanup, and transcript data management

## Error Handling

- Validates input file existence and format compatibility
- Handles FFmpeg errors during video probing and audio extraction
- Manages Whisper AI transcription failures with graceful fallback to volume-based detection
- Provides intelligent fallback behavior when transcript-based silence detection fails
- Ensures temporary files and transcript data are properly cleaned up even if processing fails
- Maintains robust error reporting with detailed context for troubleshooting
