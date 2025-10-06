"""
Flask web application for Podcast Video Editor

This module provides the main web application entry point using the web_app package.
"""

import click

# Import the main web application from the web_app package
from .web_app import VideoProcessingApp, create_app

__all__ = ["VideoProcessingApp", "create_app"]


@click.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=5000, type=int, help="Port to bind to")
@click.option("--debug", is_flag=True, help="Run in debug mode")
@click.option("--config", "config_path", help="Configuration file path")
def main(host: str, port: int, debug: bool, config_path: str):
    """Start the Podcast Video Editor web application"""
    app = create_app(config_path)
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
