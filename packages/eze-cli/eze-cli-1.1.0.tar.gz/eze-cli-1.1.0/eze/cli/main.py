"""
Entry point for command line interface
"""

import click

from eze import __version__
from eze.cli.commands.housekeeping_commands import housekeeping_group
from eze.cli.commands.reporter_commands import reporters_group
from eze.cli.commands.tool_commands import tools_group
from eze.cli.commands.test_commands import (
    test_command,
)
from eze.core.reporter import ReporterManager
from eze.core.tool import ToolManager
from eze.utils.package import get_plugins

import signal
import atexit

from eze.utils.io.file import delete_tempfile_folder
from eze.utils.log import log_error

# see https://click.palletsprojects.com/en/7.x/api/#click.Context
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
@click.pass_context
def cli(ctx) -> None:
    """Eze Command line interface"""

    # initialise plugins
    installed_plugins = get_plugins()
    ToolManager.set_instance(installed_plugins)
    ReporterManager.set_instance(installed_plugins)


cli.add_command(housekeeping_group)
cli.add_command(tools_group)
cli.add_command(reporters_group)
cli.add_command(test_command)


def handle_exit(*args):
    """handle application exit"""
    try:
        delete_tempfile_folder()
    except Exception as error:
        log_error(f"Failed to delete temp folder: '{error}'")
        pass


atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)
