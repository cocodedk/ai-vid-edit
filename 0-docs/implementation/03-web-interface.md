# Web Interface

The system includes a Flask-based web application that provides a user-friendly browser interface for video processing.

## Main Application (`web_app/app.py`)

**VideoProcessingApp Class**:
- Main Flask application wrapper
- Handles configuration loading and directory creation
- Sets up CORS for cross-origin requests
- Manages in-memory job storage for tracking processing status
- Provides the main entry point for running the web server

**Key Features**:
- **File Upload**: Supports video file uploads up to 500MB
- **Background Processing**: Processes videos asynchronously without blocking the web interface
- **Status Tracking**: Users can check processing progress via job IDs
- **Download Management**: Provides processed video downloads
- **Preview Functionality**: Shows transcript analysis and what would be removed before processing

## Route Structure (`web_app/routes.py`)

**Main Routes**:
- **Index Page** (`/`): Simple upload interface using HTML template
- **File Upload** (`/api/upload`): Handles video file uploads via `upload_routes.py`
- **Status Check** (`/api/status/<job_id>`): Returns current processing status
- **Process Video** (`/api/process`): Starts video processing in background
- **File Download** (`/api/download/<job_id>`): Downloads completed processed videos
- **Preview Results** (`/api/preview/<job_id>`): Shows transcript analysis and silence detection results before processing

## Supporting Modules

**Upload Routes** (`web_app/upload_routes.py`):
- Validates uploaded files (format and size)
- Stores files in the uploads directory
- Generates unique job IDs for tracking

**Status Routes** (`web_app/status_routes.py`):
- Manages processing job lifecycle
- Provides status updates during processing
- Handles job queuing and completion

**Download Routes** (`web_app/download_routes.py`):
- Serves processed video files
- Manages file cleanup after download
- Provides preview information

**Background Processor** (`web_app/background_processor.py`):
- Handles the actual video processing in separate threads
- Updates job status throughout the process
- Manages error handling and cleanup

## User Experience

**Simple Workflow**:
1. User visits the web interface and uploads a video file
2. System validates the file and performs Whisper AI transcription analysis
3. User can monitor progress through status checks and preview transcript data
4. Once complete, user can preview speech segments and silence analysis before downloading
5. Processed videos preserve ambient audio while removing true silence between speech
6. Files are stored in organized directories (uploads/ and processed/)

## Technical Features

- **Job Management**: Uses in-memory storage for job tracking (could be upgraded to Redis/database)
- **Threading**: Background processing doesn't block the web interface
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **File Management**: Automatic directory creation and file organization
- **CORS Support**: Allows the web interface to be used from different domains
