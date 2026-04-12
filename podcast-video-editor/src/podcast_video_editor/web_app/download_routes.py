"""
Download and preview route handlers
"""

from flask import jsonify, send_file


def download_file(app, job_id: str):
    """Download processed file"""
    if job_id not in app.jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = app.jobs[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'Processing not completed'}), 400

    processed_path = job.get('processed_path')
    if not processed_path:
        return jsonify({'error': 'Processed file not found'}), 404

    return send_file(
        processed_path,
        as_attachment=True,
        download_name=f"edited_{job['original_filename']}"
    )


def preview_results(app, job_id: str):
    """Preview processing results"""
    if job_id not in app.jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = app.jobs[job_id]
    if job.get('analysis'):
        return jsonify(job['analysis'])
    else:
        return jsonify({'error': 'No preview data available'}), 404
