"""
Background video processing logic
"""

from pathlib import Path

from ..processor import VideoProcessor


def process_video_job(app, job_id: str):
    """Process a video job in the background"""
    job = app.jobs[job_id]
    file_path = job['file_path']

    try:
        # Analyze video first
        app.jobs[job_id]['message'] = 'Analyzing video...'
        app.jobs[job_id]['progress'] = 10

        processed_root = Path(app.app.config['PROCESSED_FOLDER'])
        run_directory = VideoProcessor.create_run_directory(Path(file_path), processed_root)

        # Generate output path with job ID to prevent collisions
        output_filename = f"edited_{job_id}_{Path(job['original_filename']).name}"
        output_path = run_directory / output_filename

        with VideoProcessor(app.config, verbose=True, run_directory=run_directory) as processor:
            # Analyze video first
            analysis = processor.analyze_video(file_path)

            # Store analysis for preview
            job['analysis'] = {
                'duration': analysis.duration,
                'silence_periods': len(analysis.silence_periods),
                'estimated_output_duration': analysis.estimated_output_duration,
                'silence_reduction_percent': analysis.silence_reduction_percent,
                'transcript_segments': len(analysis.transcript_segments) if analysis.transcript_segments else 0
            }

            app.jobs[job_id]['progress'] = 30
            app.jobs[job_id]['message'] = 'Processing video...'

            # Process video
            result_path = processor.process_video(file_path, str(output_path))

        # Update job status
        app.jobs[job_id]['status'] = 'completed'
        app.jobs[job_id]['progress'] = 100
        app.jobs[job_id]['message'] = 'Processing completed successfully'
        app.jobs[job_id]['processed_path'] = result_path
        app.jobs[job_id]['run_directory'] = str(run_directory)

    except Exception as e:
        # Handle errors properly - update job status to error
        app.jobs[job_id]['status'] = 'error'
        app.jobs[job_id]['message'] = f'Processing failed: {str(e)}'
        app.jobs[job_id]['error_details'] = str(e)
        print(f"Error processing job {job_id}: {e}")
        raise  # Re-raise to ensure the background thread handler knows about the failure
