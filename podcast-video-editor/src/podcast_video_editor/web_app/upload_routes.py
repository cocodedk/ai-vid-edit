"""
Upload route handlers
"""

import uuid
from pathlib import Path

from flask import request, jsonify, url_for

from .utils import allowed_file


def upload_file(app):
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    # Generate unique job ID
    job_id = str(uuid.uuid4())

    # Save file
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    file_path = Path(app.app.config['UPLOAD_FOLDER']) / f"{job_id}_{filename}"
    file.save(file_path)

    # Initialize job
    app.jobs[job_id] = {
        'status': 'uploaded',
        'file_path': str(file_path),
        'original_filename': filename,
        'progress': 0,
        'message': 'File uploaded successfully'
    }

    return jsonify({
        'job_id': job_id,
        'message': 'File uploaded successfully',
        'status_url': url_for('get_status', job_id=job_id)
    })
