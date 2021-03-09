from uuid import uuid4

import click
from flask import current_app
from flask.cli import with_appcontext

from domain.users.entities.group import GroupType, PositionGroupTypeEntity


@click.command("create-position-groups")
@with_appcontext
def create_position_group():
    uow = current_app.context
    positions_groups = {
        GroupType.MAIRIE: ["Maire", "Adjoint", "Chef Sécurité"],
        GroupType.PREFECTURE: ["Préfet", "Directeur de cabinet", "Chef site PC"],
    }

    positions = [PositionGroupTypeEntity(
        uuid=str(uuid4()),
        label=position,
        group_type=group_type
    ) for group_type, positions in positions_groups.items() for position in positions]

    with uow:
        uow.session.add_all(positions)
