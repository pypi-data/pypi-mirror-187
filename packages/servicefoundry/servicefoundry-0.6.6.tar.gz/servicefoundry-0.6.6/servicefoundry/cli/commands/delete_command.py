import logging

import rich_click as click

from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.cli.display_util import print_json
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.lib.dao import workspace as workspace_lib

logger = logging.getLogger(__name__)

# TODO (chiragjn): --json should disable all non json console prints


@click.group(name="delete", cls=GROUP_CLS)
def delete_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Servicefoundry delete resource

    \b
    Supported resources:
    - Workspace
    - Service
    """
    pass


@click.command(name="workspace", cls=COMMAND_CLS, help="Delete a Workspace")
@click.argument("name", type=click.STRING)
@click.option(
    "-c",
    "--cluster",
    type=click.STRING,
    default=None,
    help="cluster to delete the workspace from",
)
@click.option("--force", is_flag=True, default=False, help="force delete the workspace")
@click.confirmation_option(prompt="Are you sure you want to delete this workspace?")
@handle_exception_wrapper
def delete_workspace(name, cluster, force: bool = False):
    # Tests:
    # - Set Context -> delete workspace -> Should give error to give workspace name
    # - Set Context -> delete workspace valid_name -> Should delete
    # - Set Context -> delete workspace invalid_name -> Should give error no such workspace in set cluster
    # - Set Context -> delete workspace name -c 'invalid_cluster_name' -> Should give error invalid cluster
    # - Set Context -> delete workspace invalid_name -c 'cluster_name' -> Should give error invalid workspace
    # - Set Context -> delete workspace valid_name -c 'cluster_name' -> Should delete
    # - No Context -> delete workspace -> Should give error to give workspace name
    # - No Context -> delete workspace valid_name -> Try to resolve, if only one exists then delete
    #                 otherwise error to give cluster
    # - No Context -> delete workspace invalid_name -> Tries to resolve, if only one exists then delete
    #                 otherwise error to give cluster
    # - No Context -> delete workspace name -c 'invalid_cluster_name' -> Should give error invalid cluster
    # - No Context -> delete workspace invalid_name -c 'cluster_name' -> Should give error invalid workspace
    # - No Context -> delete workspace valid_name -c 'cluster_name' -> Should delete
    response = workspace_lib.delete_workspace(
        name_or_id=name,
        cluster_name_or_id=cluster,
        force=force,
        non_interactive=True,
    )
    if CliConfig.get("json"):
        print_json(data=response)


def get_delete_command():
    delete_command.add_command(delete_workspace)
    return delete_command
