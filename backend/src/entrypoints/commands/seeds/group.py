from flask import current_app
import click
from flask.cli import with_appcontext

from domain.users.entities.group import GroupEntity, GroupType


@click.command()
@with_appcontext
def create_group():
    uow = current_app.context

