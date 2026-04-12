# Configuration Management

The system uses a flexible configuration system that allows customization of all processing parameters through configuration files and command-line options.

## Main Configuration Class (`config.py`)

**Config Class**:
- Central configuration management for the entire system
- Loads settings from files or uses sensible defaults
- Provides easy access to all configuration parameters
- Supports runtime configuration updates

**Key Features**:
- **File-based Configuration**: Can load settings from JSON/YAML files
- **Environment Integration**: Reads settings from environment variables
- **Command-line Overrides**: Allows CLI options to override file settings
- **Validation**: Ensures configuration values are within acceptable ranges

## Configuration Models (`config/models.py`)

**WhisperConfig**:
- Controls OpenAI Whisper AI settings for audio transcription
- Configurable model size (tiny, base, small, medium, large)
- Language support with automatic detection or manual selection
- Supports 99+ languages including English, Spanish, French, German, Chinese, Japanese, and many more
- Device selection (CPU/GPU) for performance optimization

**SilenceDetectionConfig**:
- Controls how silence periods are identified
- Adjustable audio threshold in decibels (dB)
- Minimum silence duration to avoid cutting short pauses
- Fine-tunes detection sensitivity for different content types

**TransitionsConfig**:
- Manages video transition effects between segments
- Configurable transition type (crossfade, etc.)
- Adjustable transition duration in milliseconds
- Controls visual smoothness of the final output

**OutputConfig**:
- Defines the final video output specifications
- Output format selection (MP4, MOV, etc.)
- Quality settings for file size vs visual quality balance
- Options for including intro/outro segments

## Configuration Manager (`config/manager.py`)

**ConfigurationManager Class**:
- Handles loading, saving, and validation of configuration files
- Provides user-friendly configuration wizards
- Supports multiple configuration profiles
- Validates settings before applying them

**Key Methods**:
- **load_from_file()**: Reads configuration from disk files
- **save_to_file()**: Persists current settings to disk
- **validate()**: Ensures all settings are within valid ranges
- **merge_overrides()**: Combines file settings with command-line options

## Integration Points

**With CLI Interface**:
- Command-line options can override any configuration setting
- Preview command shows current configuration values
- Process command uses configuration for all processing decisions

**With Web Interface**:
- Web application loads configuration at startup
- Background processing uses configuration for job execution
- Status reporting includes configuration details

**With Processing Engine**:
- VideoProcessor uses configuration for all processing decisions
- AudioProcessor applies silence detection settings from configuration
- VideoSegmentProcessor uses transition settings for output creation

## Configuration Hierarchy

**Priority Order** (highest to lowest):
1. Command-line options (CLI only)
2. Environment variables
3. Configuration file settings
4. Built-in default values

**Example Usage**:
- User sets silence threshold via CLI: `--silence-threshold -35`
- Environment variable: `SILENCE_THRESHOLD_DB=-35`
- Configuration file: `"silence_detection": {"threshold_db": -35}`
- Default value: `-40.0`

## User Experience

**Easy Setup**:
- New users can start with sensible defaults
- Configuration wizard helps optimize settings for their content
- Settings can be adjusted without deep technical knowledge

**Persistence**:
- Settings are saved to files for reuse across sessions
- Different projects can have different configurations
- Teams can share configuration files

**Validation**:
- System prevents invalid configuration combinations
- Clear error messages when settings are out of range
- Suggestions for better configuration values when issues are detected
