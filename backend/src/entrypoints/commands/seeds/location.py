from uuid import uuid4

from flask import current_app
import click
from flask.cli import with_appcontext

from domain.users.entities.group import LocationType, LocationEntity


@click.command("create-groups")
@with_appcontext
def create_group():
    uow = current_app.context


    with uow:
        uow.session.add_all(groups)
