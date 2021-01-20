from uuid import uuid4
from flask import current_app
import click
from flask.cli import with_appcontext

from domain.phonebook.entities.group import GroupEntity


@click.command()
@with_appcontext
def create_group():
    uow = current_app.context
    groups = [
        GroupEntity(uuid="mairie_uuid",
                    name="Mairie",
                    description="Mairie",
                    ),
        GroupEntity(uuid="prefecture_uuid",
                    name="Prefecture",
                    description="Prefecture",
                    ),
        GroupEntity(uuid="sdis_uuid",
                    name="SDIS",
                    description="Service d'incendie et de secours",
                    ),
        GroupEntity(uuid="coz_uuid",
                    name="COZ",
                    description="Centre opérationel zonal",
                    ),
    ]
    with uow:
        for group in groups:
            uow.session.add(group)
