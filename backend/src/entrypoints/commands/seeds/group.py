from flask import current_app
import click
from flask.cli import with_appcontext

from domain.users.entities.group import GroupEntity, GroupType


@click.command()
@with_appcontext
def create_group():
    uow = current_app.context

    companies = [
        GroupEntity(uuid="mairie_uuid",
                    name="Mairie Chelles",
                    type=GroupType.MAIRIE
                    ),
        GroupEntity(uuid="prefecture_uuid",
                    name="Prefecture",
                    type=GroupType.MAIRIE
                    ),
        GroupEntity(uuid="sdis_uuid",
                    name="SDIS",
                    type=GroupType.SDIS
                    ),
    ]
    with uow:
        for group in companies:
            uow.session.add(group)
