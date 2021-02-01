import itertools

from flask import current_app
import click
from flask.cli import with_appcontext

from domain.users.entities.group import GroupEntity, GroupType, LocationEntity, LocationType


@click.command("create-groups-and-locations")
@with_appcontext
def create_group_and_locations():
    uow = current_app.context

