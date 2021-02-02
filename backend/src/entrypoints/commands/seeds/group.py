import itertools

from flask import current_app
import click
from flask.cli import with_appcontext

from domain.users.entities.group import GroupEntity, GroupType, LocationEntity, LocationType


@click.command("create-groups-and-locations")
@with_appcontext
def create_group_and_locations():
    uow = current_app.context

    locations = [
        LocationEntity(uuid="ville_77108",
                       name="Chelles",
                       external_id="77108",
                       type=LocationType.VILLE,
                       ),
        LocationEntity(uuid="dept_77",
                       name="Seine-et-Marne",
                       external_id="77",
                       type=LocationType.DEPARTEMENT,
                       )
        ]

    groups = [
        GroupEntity(uuid="prefecture_uuid",
                    name="Prefecture de Seine et Marne",
                    type=GroupType.PREFECTURE,
                    location_id="dept_77",
        ),
        GroupEntity(uuid="sdis_uuid",
                    name="SDIS",
                    type=GroupType.SDIS,
                    location_id="dept_77",
        ),
        GroupEntity(uuid="mairie_uuid",
                    name="Mairie Chelles",
                    type=GroupType.MAIRIE,
                    location_id="ville_77108",
        )
    ]

    with uow:
        # uow.session.add_all(list(groups_and_locations.keys()))
        # for location, groups in groups_and_locations.items():
        #     for group in groups:
        #         uow.session.add(group)
        #         group.location = location
        #         uow.session.commit()
        uow.session.add_all(locations)
        uow.session.add_all(groups)
        for group in groups:
            group.location = locations[0]