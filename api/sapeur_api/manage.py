import click
from flask.cli import FlaskGroup

from .app import create_app


def create_sapeur_api(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_sapeur_api)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new admin user
    """
    from .extensions import db
    from .domain.models import User

    click.echo("create user")
    user = User(username="sapeuradmin", email="r.courivaud@gmail.com", password="sapeurpassword", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
