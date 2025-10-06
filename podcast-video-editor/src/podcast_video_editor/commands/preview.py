"""
Preview command for video analysis
"""

import sys
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
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
def preview(
    input_video: str,
    config: Optional[str],
    whisper_model: str,
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

        # Create processor and analyze
        processor = VideoProcessor(config_obj, verbose=verbose)
        analysis = processor.analyze_video(input_video)

        click.echo("🎬 Video Analysis Results:")
        click.echo(f"   Duration: {analysis.duration:.2f}s")
        click.echo(f"   Silence periods: {len(analysis.silence_periods)}")
        click.echo(f"   Estimated output duration: {analysis.estimated_output_duration:.2f}s")
        click.echo(f"   Silence reduction: {analysis.silence_reduction_percent:.1f}%")

    except Exception as e:
        click.echo(f"❌ Error analyzing video: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
