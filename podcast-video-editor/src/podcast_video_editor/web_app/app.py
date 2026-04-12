"""
Main Flask application class
"""

import os
from typing import Dict, Optional

from flask import Flask
from flask_cors import CORS

from ..config import Config


class VideoProcessingApp:
    """Flask web application for video processing"""

    def __init__(self, config_path: Optional[str] = None):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
        self.app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
        self.app.config['UPLOAD_FOLDER'] = 'uploads'
        self.app.config['PROCESSED_FOLDER'] = 'processed'

        # Enable CORS
        CORS(self.app)

        # Load configuration
        self.config = Config.from_file(config_path) if config_path else Config()

        # Create directories
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(self.app.config['PROCESSED_FOLDER'], exist_ok=True)

        # In-memory job storage (in production, use Redis/database)
        self.jobs: Dict[str, Dict] = {}

        # Setup routes
        from .routes import setup_routes
        setup_routes(self)

    def run(self, host='127.0.0.1', port=5000, debug=False):
        """Run the Flask application"""
        self.app.run(host=host, port=port, debug=debug)


def create_app(config_path: Optional[str] = None) -> VideoProcessingApp:
    """Create and configure the Flask application"""
    return VideoProcessingApp(config_path)
