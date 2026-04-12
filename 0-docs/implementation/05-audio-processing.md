# Audio Processing and Silence Detection

The system analyzes audio tracks to identify periods of silence that can be removed from podcast videos.

## AudioProcessor Class (`processing/audio_processing.py`)

**Main Responsibilities**:
- Extracts audio tracks from video files
- Analyzes audio to detect silence periods
- Provides detailed information about silence segments
- Works with configuration settings for customizable detection

**Key Methods**:

**extract_audio()**:
- Takes a video file path and extracts the audio track
- Uses FFmpeg to separate audio from video container
- Saves audio as temporary WAV file for analysis
- Returns path to extracted audio file

**transcribe_audio()**:
- Uses Whisper AI to transcribe audio with precise word-level timestamps
- Supports multiple languages with automatic language detection
- Extracts audio from video using FFmpeg first
- Returns list of `TranscriptSegment` objects with start/end times for each word
- Provides confidence scores for transcription accuracy
- Enables precise editing decisions based on actual speech content in any supported language

**detect_silence()**:
- Analyzes audio file to find silence periods using intelligent speech detection
- Uses Whisper transcription to identify gaps between actual speech
- Returns list of `SilencePeriod` objects representing true silence (no speech)
- Distinguishes between speech and ambient noise/background sounds

## Silence Detection Strategies

**Primary Detector** (`processing/ffmpeg_silence_detector.py`):
- Uses FFmpeg's built-in silence detection capabilities
- Fast and reliable for most audio types
- Configurable threshold and duration parameters
- Leverages FFmpeg's audio analysis algorithms

**Fallback Detector** (`processing/fallback_silence_detector.py`):
- Alternative detection method for edge cases
- Useful when FFmpeg detection fails or produces poor results
- Implements custom audio analysis algorithms
- Provides backup capability for robust operation

**Detector Interface** (`processing/silence_detection.py`):
- Abstract interface for different detection methods
- Allows easy swapping of detection strategies
- Provides consistent API for all detection approaches

## Supporting Components

**TranscriptSegment Model** (`processing/models.py`):
- Data structure representing transcribed speech segments
- Contains precise start/end times for each word or sentence
- Includes transcribed text and confidence scores
- Enables word-level timing for precise video editing

**SilencePeriod Model** (`processing/models.py`):
- Data structure representing periods of true silence (no speech)
- Contains start time, end time, and duration information
- Used throughout the system for intelligent silence removal

**Audio Analysis**:
- Processes audio waveforms to identify low-volume segments
- Considers both absolute volume thresholds and relative quiet periods
- Filters out very brief pauses that shouldn't be considered silence

## Configuration Integration

**Threshold Settings** (`SilenceDetectionConfig`):
- Configurable silence threshold in decibels (dB)
- Adjustable minimum silence duration in milliseconds
- Allows fine-tuning for different types of content

**Processing Parameters**:
- Integrates with the main configuration system
- Can be overridden via command-line options
- Supports different settings for different audio types

## Workflow Integration

**With VideoProcessor**:
- Called during both analysis and processing phases
- Provides silence data for output duration estimation
- Supplies timing information for video segment extraction

**Error Handling**:
- Handles cases where audio extraction fails
- Provides fallback detection when primary method fails
- Validates audio file integrity before processing

## Performance Considerations

- **Temporary Files**: Audio extraction creates temporary files that are automatically cleaned up
- **Memory Usage**: Processes audio in chunks to handle large files efficiently
- **Speed Optimization**: Uses efficient algorithms and FFmpeg for fast processing
- **Accuracy Trade-offs**: Balances detection accuracy with processing speed
