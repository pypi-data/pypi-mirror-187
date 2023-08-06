"""obsidian-metadata CLI."""


from pathlib import Path
from typing import Optional

import typer
from rich import print

from obsidian_metadata._config import Config
from obsidian_metadata._utils import alerts, docstring_parameter, version_callback
from obsidian_metadata.models import Application

app = typer.Typer(add_completion=False, no_args_is_help=True, rich_markup_mode="rich")

typer.rich_utils.STYLE_HELPTEXT = ""

HELP_TEXT = """
"""


@app.command()
@docstring_parameter(__package__)
def main(
    vault_path: Path = typer.Option(
        None,
        help="Path to Obsidian vault",
        show_default=False,
    ),
    config_file: Path = typer.Option(
        Path(Path.home() / f".{__package__}.toml"),
        help="Specify a custom path to a configuration file",
        show_default=False,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Dry run - don't actually change anything",
    ),
    log_file: Path = typer.Option(
        Path(Path.home() / "logs" / "obsidian_metadata.log"),
        help="Path to log file",
        show_default=True,
        dir_okay=False,
        file_okay=True,
        exists=False,
    ),
    log_to_file: bool = typer.Option(
        False,
        "--log-to-file",
        help="Log to file",
        show_default=True,
    ),
    verbosity: int = typer.Option(
        0,
        "-v",
        "--verbose",
        show_default=False,
        help="""Set verbosity level (0=WARN, 1=INFO, 2=DEBUG, 3=TRACE)""",
        count=True,
    ),
    version: Optional[bool] = typer.Option(
        None, "--version", help="Print version and exit", callback=version_callback, is_eager=True
    ),
) -> None:
    r"""A script to make batch updates to metadata in an Obsidian vault.

    [bold] [/]
    [bold underline]Features:[/]

      - [code]in-text tags:[/] delete every occurrence
      - [code]in-text tags:[/] Rename tag ([dim]#tag1[/] -> [dim]#tag2[/])
      - [code]frontmatter:[/] Delete a key matching a regex pattern and all associated values
      - [code]frontmatter:[/] Rename a key
      - [code]frontmatter:[/] Delete a value matching a regex pattern from a specified key
      - [code]frontmatter:[/] Rename a value from a specified key
      - [code]inline metadata:[/] Delete a key matching a regex pattern and all associated values
      - [code]inline metadata:[/] Rename a key
      - [code]inline metadata:[/] Delete a value matching a regex pattern from a specified key
      - [code]inline metadata:[/] Rename a value from a specified key
      - [code]vault:[/] Create a backup of the Obsidian vault.

    [bold underline]Usage:[/]
    [tan]Obsidian-metadata[/] allows you to make batch updates to metadata in an Obsidian vault.  Once you have made your changes, review them prior to committing them to the vault.  The script provides a menu of available actions. Make as many changes as you require and review them as you go.  No changes are made to the Vault until they are explicitly committed.

    [bold underline]It is strongly recommended that you back up your vault prior to committing changes.[/] This script makes changes directly to the markdown files in your vault. Once the changes are committed, there is no ability to recreate the original information unless you have a backup.  Follow the instructions in the script to create a backup of your vault if needed.  The author of this script is not responsible for any data loss that may occur. Use at your own risk.

    Configuration is specified in a configuration file. On First run, this file will be created at [tan]~/.{0}.env[/]. Any options specified on the command line will override the configuration file.
    """
    # Instantiate logger
    alerts.LoggerManager(  # pragma: no cover
        log_file,
        verbosity,
        log_to_file,
    )

    config: Config = Config(config_path=config_file, vault_path=vault_path)
    application = Application(dry_run=dry_run, config=config)

    banner = r"""
   ___  _         _     _ _
  / _ \| |__  ___(_) __| (_) __ _ _ __
 | | | | '_ \/ __| |/ _` | |/ _` | '_ \
 | |_| | |_) \__ \ | (_| | | (_| | | | |
  \___/|_.__/|___/_|\__,_|_|\__,_|_| |_|
 |  \/  | ___| |_ __ _  __| | __ _| |_ __ _
 | |\/| |/ _ \ __/ _` |/ _` |/ _` | __/ _` |
 | |  | |  __/ || (_| | (_| | (_| | || (_| |
 |_|  |_|\___|\__\__,_|\__,_|\__,_|\__\__,_|
"""
    print(banner)
    application.main_app()


if __name__ == "__main__":
    app()
