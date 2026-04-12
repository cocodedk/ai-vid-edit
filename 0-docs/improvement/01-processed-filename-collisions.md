# Processed Filename Collisions

- **Location**: `podcast-video-editor/src/podcast_video_editor/web_app/background_processor.py:20`
- **Issue**: The output filename was generated as `edited_{original_filename}` without the job ID or any other unique identifier. Two separate jobs that upload files with the same original name would write to the same target (`processed/edited_<name>`), so the later job would overwrite the earlier one.
- **Impact**: Users could download the wrong processed video, and concurrent jobs would clobber each other in the `processed/` directory.
- **Status**: ✅ **FIXED** - Updated to use `f"edited_{job_id}_{original_filename}"` for guaranteed per-job isolation.
- **Fix Applied**: Modified `process_video_job()` function to include job_id in output filename, preventing collisions between concurrent jobs.
