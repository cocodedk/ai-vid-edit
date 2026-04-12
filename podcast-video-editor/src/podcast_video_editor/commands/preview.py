"""
Preview command for video analysis
"""

import sys
from pathlib import Path
from typing import Optional

import click

from ..config import Config
from ..processor import VideoProcessor


@click.command()
@click.argument("input_video", type=click.Path(exists=True))
@click.option(
    "--config", "-c",
    type=click.Path(exists=True),
    help="Configuration file path"
)
@click.option(
    "--whisper-model",
    type=click.Choice(["tiny", "base", "small", "medium", "large"]),
    default="base",
    help="Whisper model size to use"
)
@click.option(
    "--language",
    type=str,
    default=None,
    help="Language code for transcription (e.g., 'en', 'es', 'fr'). Leave empty for auto-detection"
)
@click.option(
    "--device",
    type=click.Choice(["auto", "cpu", "cuda"]),
    default="auto",
    help="Select processing device (auto chooses CUDA when available)"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
def preview(
    input_video: str,
    config: Optional[str],
    whisper_model: str,
    language: Optional[str],
    device: str,
    verbose: bool
):
    """Preview video processing results without actually processing"""

    try:
        # Load configuration
        if config:
            config_obj = Config.from_file(config)
        else:
            config_obj = Config()

        config_obj.whisper.model = whisper_model
        if language is not None:
            config_obj.whisper.language = language
        config_obj.whisper.device = device

        input_path = Path(input_video)
        run_directory = VideoProcessor.create_run_directory(input_path)

        # Create processor and analyze (using context manager for temp directory management)
        with VideoProcessor(
            config_obj,
            verbose=verbose,
            run_directory=run_directory,
            cleanup_run_directory=True,
        ) as processor:
            analysis = processor.analyze_video(input_video)

        click.echo("🎬 Video Analysis Results:")
        click.echo(f"   Duration: {analysis.duration:.2f}s")
        click.echo(f"   Silence periods: {len(analysis.silence_periods)}")
        click.echo(f"   Estimated output duration: {analysis.estimated_output_duration:.2f}s")
        click.echo(f"   Silence reduction: {analysis.silence_reduction_percent:.1f}%")

        # Show transcript information if available
        if analysis.transcript_segments:
            click.echo(f"   Transcript segments: {len(analysis.transcript_segments)}")
            if len(analysis.transcript_segments) > 0:
                sample_text = analysis.transcript_segments[0].text[:50] + "..." if len(analysis.transcript_segments[0].text) > 50 else analysis.transcript_segments[0].text
                click.echo(f"   Sample transcript: '{sample_text}'")
        else:
            click.echo("   Transcript: Not available (processing may have failed)")

    except Exception as e:
        click.echo(f"❌ Error analyzing video: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
