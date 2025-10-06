"""
Route handlers for the Flask web application
"""

import uuid
from pathlib import Path

from flask import request, jsonify, render_template, send_file, url_for

from ..processor import VideoProcessor
from .utils import allowed_file


def setup_routes(app: 'VideoProcessingApp'):
    """Setup Flask routes for the application"""

    @app.app.route('/')
    def index():
        """Main upload page"""
        return render_template('index.html')

    @app.app.route('/api/upload', methods=['POST'])
    def upload_file_route():
        """Handle file upload"""
        from .upload_routes import upload_file
        return upload_file(app)

    @app.app.route('/api/status/<job_id>')
    def get_status_route(job_id: str):
        """Get processing status"""
        from .status_routes import get_status
        return get_status(app, job_id)

    @app.app.route('/api/process', methods=['POST'])
    def process_video_route():
        """Start video processing"""
        from .status_routes import process_video
        return process_video(app)

    @app.app.route('/api/download/<job_id>')
    def download_file_route(job_id: str):
        """Download processed file"""
        from .download_routes import download_file
        return download_file(app, job_id)

    @app.app.route('/api/preview/<job_id>')
    def preview_results_route(job_id: str):
        """Preview processing results"""
        from .download_routes import preview_results
        return preview_results(app, job_id)


def _process_video_background(app: 'VideoProcessingApp', job_id: str):
    """Process video in background"""
    import threading

    def process():
        try:
            from .background_processor import process_video_job
            process_video_job(app, job_id)
        except Exception as e:
            app.jobs[job_id]['status'] = 'error'
            app.jobs[job_id]['message'] = f'Processing failed: {str(e)}'
            print(f"Error processing job {job_id}: {e}")

    # Start background processing
    thread = threading.Thread(target=process)
    thread.daemon = True
    thread.start()
