"""
Status and processing route handlers
"""

from flask import request, jsonify, url_for


def get_status(app, job_id: str):
    """Get processing status"""
    if job_id not in app.jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = app.jobs[job_id]

    # Check if processing is complete
    if job['status'] == 'completed':
        download_url = url_for('download_file', job_id=job_id)
        return jsonify({
            'status': job['status'],
            'progress': 100,
            'message': job.get('message', 'Processing completed'),
            'download_url': download_url
        })

    return jsonify({
        'status': job['status'],
        'progress': job.get('progress', 0),
        'message': job.get('message', 'Processing...')
    })


def process_video(app):
    """Start video processing"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    job_id = data.get('job_id')
    if not job_id or job_id not in app.jobs:
        return jsonify({'error': 'Invalid job ID'}), 400

    # Update job status
    app.jobs[job_id]['status'] = 'processing'
    app.jobs[job_id]['progress'] = 0
    app.jobs[job_id]['message'] = 'Starting processing...'

    # Start processing in background
    try:
        from .routes import _process_video_background
        _process_video_background(app, job_id)
        return jsonify({'message': 'Processing started'})
    except Exception as e:
        app.jobs[job_id]['status'] = 'error'
        app.jobs[job_id]['message'] = f'Processing failed: {str(e)}'
        return jsonify({'error': str(e)}), 500
