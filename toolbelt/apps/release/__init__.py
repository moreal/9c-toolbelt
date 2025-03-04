from typing import Optional

import typer

from toolbelt.utils.typer import network_arg, platforms_arg

from .release_player import release as release_player
from .update_latest_metadata import update as update_latest_metadata

release_app = typer.Typer()


@release_app.command()
def player(
    commit_hash: str,
    version: int,
    network: str = network_arg,
    platform: str = platforms_arg,
    signing: bool = False,
    slack_channel: Optional[str] = None,
    run_id: Optional[str] = None,
):
    release_player(
        commit_hash,
        platform,  # type:ignore
        version,
        network,  # type:ignore
        signing,
        slack_channel,
        run_id
    )

@release_app.command()
def update_latest(
    commit_hash: str,
    version: int,
    network: str,
    slack_channel: Optional[str] = None,
):
    update_latest_metadata(
        version,
        commit_hash,
        network,
        slack_channel,
    )
