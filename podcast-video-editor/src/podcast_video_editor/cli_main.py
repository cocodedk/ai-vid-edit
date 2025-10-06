"""
Main CLI entry point for Podcast Video Editor
"""

import os
import sys
from pathlib import Path

import click
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Podcast Video Editor - AI-powered video editing platform"""
    pass


# Import and register command groups
from .commands.process import process
from .commands.preview import preview
from .commands.configure import configure

main.add_command(process)
main.add_command(preview)
main.add_command(configure)


if __name__ == "__main__":
    main()
