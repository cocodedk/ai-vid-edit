"""
Background video processing logic
"""

from pathlib import Path

from ..processor import VideoProcessor


def process_video_job(app, job_id: str):
    """Process a video job in the background"""
    job = app.jobs[job_id]
    file_path = job['file_path']

    # Analyze video first
    app.jobs[job_id]['message'] = 'Analyzing video...'
    app.jobs[job_id]['progress'] = 10

    processor = VideoProcessor(app.config, verbose=True)
    analysis = processor.analyze_video(file_path)

    # Store analysis for preview
    job['analysis'] = {
        'duration': analysis.duration,
        'silence_periods': len(analysis.silence_periods),
        'estimated_output_duration': analysis.estimated_output_duration,
        'silence_reduction_percent': analysis.silence_reduction_percent
    }

    app.jobs[job_id]['progress'] = 30
    app.jobs[job_id]['message'] = 'Processing video...'

    # Generate output path
    output_filename = f"edited_{job['original_filename']}"
    output_path = Path(app.app.config['PROCESSED_FOLDER']) / output_filename

    # Process video
    result_path = processor.process_video(file_path, str(output_path))

    # Update job status
    app.jobs[job_id]['status'] = 'completed'
    app.jobs[job_id]['progress'] = 100
    app.jobs[job_id]['message'] = 'Processing completed successfully'
    app.jobs[job_id]['processed_path'] = result_path
