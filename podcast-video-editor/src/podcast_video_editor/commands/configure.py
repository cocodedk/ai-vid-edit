"""
Configure command for settings management
"""

from pathlib import Path
from typing import Optional

import click

from ..config import Config


@click.command()
@click.option(
    "--config-file", "-c",
    type=click.Path(),
    help="Configuration file to create/edit"
)
def configure(config_file: Optional[str]):
    """Configure podcast editor settings"""

    if not config_file:
        config_file = ".podcast-editor.json"

    config_path = Path(config_file)

    if config_path.exists():
        click.echo(f"📝 Opening existing config: {config_path}")
        # TODO: Open in editor or show current settings
    else:
        click.echo(f"📄 Creating new config: {config_path}")
        config_obj = Config()
        config_obj.save(config_path)
        click.echo("✅ Configuration file created!")
