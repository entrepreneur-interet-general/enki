from uuid import uuid4
from flask import current_app
import click
from flask.cli import with_appcontext

from domain.users.entities.company import CompanyEntity, CompanyType


@click.command()
@with_appcontext
def create_group():
    uow = current_app.context

    companies = [
        CompanyEntity(uuid="mairie_uuid",
                    name="Mairie Chelles",
                  type=CompanyType.MAIRIE
                    ),
        CompanyEntity(uuid="prefecture_uuid",
                    name="Prefecture",
                      type=CompanyType.MAIRIE
                    ),
        CompanyEntity(uuid="sdis_uuid",
                    name="SDIS",
                      type=CompanyType.SDIS
                    ),
    ]
    with uow:
        for company in companies:
            uow.session.add(company)
