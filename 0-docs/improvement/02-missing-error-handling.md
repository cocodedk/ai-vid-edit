# Missing Error Handling In `process_video_job`

- **Location**: `podcast-video-editor/src/podcast_video_editor/web_app/background_processor.py:23-39`
- **Issue**: The function did not catch exceptions raised by `VideoProcessor.analyze_video` or `VideoProcessor.process_video`. Any ffmpeg/Whisper failure would bubble up, leaving progress stuck at 10/30 and relying on the caller to patch the job state. Documentation (`0-docs/implementation/07-background-jobs.md`) specifies that `process_video_job()` itself should transition jobs to `'error'` with a meaningful message.
- **Impact**: When the function was reused outside the current `_process_video_background` wrapper—or if that wrapper was bypassed—jobs would remain in `'processing'` with stale progress, and users would never receive an error message.
- **Status**: ✅ **FIXED** - Added comprehensive try/except error handling around all VideoProcessor operations.
- **Fix Applied**:
  - Wrapped entire processing logic in try/except block
  - On error: Sets `job['status'] = 'error'` and `job['message']` with descriptive error
  - Added `job['error_details']` for debugging information
  - Proper exception re-raising to ensure background thread handler knows about failures
  - Maintains documented expectation that function handles its own error states
