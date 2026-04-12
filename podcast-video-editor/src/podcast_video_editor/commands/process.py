"""
Process command for video editing
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
    "--output", "-o",
    type=click.Path(),
    help="Output file name (stored inside the run directory)"
)
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
    "--silence-threshold",
    type=float,
    default=-40.0,
    help="Silence detection threshold in dB"
)
@click.option(
    "--min-silence-duration",
    type=float,
    default=0.5,
    help="Minimum silence duration in seconds"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
def process(
    input_video: str,
    output: Optional[str],
    config: Optional[str],
    whisper_model: str,
    language: Optional[str],
    device: str,
    silence_threshold: float,
    min_silence_duration: float,
    verbose: bool
):
    """Process a podcast video file"""

    try:
        # Load configuration
        if config:
            config_obj = Config.from_file(config)
        else:
            config_obj = Config()

        # Override config with command line options
        config_obj.whisper.model = whisper_model
        if language is not None:
            config_obj.whisper.language = language
        config_obj.whisper.device = device
        config_obj.silence_detection.threshold_db = silence_threshold
        config_obj.silence_detection.min_duration_ms = int(min_silence_duration * 1000)

        input_path = Path(input_video)
        run_directory = VideoProcessor.create_run_directory(input_path)

        # Determine output path inside run directory
        if output:
            output_name = Path(output).name
        else:
            output_name = input_path.with_stem(f"{input_path.stem}_edited").name

        output_path = run_directory / output_name

        # Create processor and run (using context manager for temp directory management)
        with VideoProcessor(config_obj, verbose=verbose, run_directory=run_directory) as processor:
            result_path = processor.process_video(input_video, str(output_path))

        click.echo(f"✅ Processing completed! Output saved to: {result_path}")
        click.echo(f"📂 Run directory: {run_directory}")

    except Exception as e:
        click.echo(f"❌ Error processing video: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
