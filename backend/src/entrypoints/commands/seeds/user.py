from flask import current_app
import click
from flask.cli import with_appcontext

from domain.users.entities.group import GroupEntity, GroupType
from domain.users.entities.user import UserEntity


@click.command("create-users")
@with_appcontext
def create_group():
    uow = current_app.context

    users = [
        UserEntity(uuid="my-test-user-id",
                   first_name="Enki",
                   last_name="Enki",
                   postion="boss"
                   ),
    ]
    with uow:
        uow.session.add_all(users)
