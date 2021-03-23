import json
import os
import random
from datetime import datetime
from typing import List
from uuid import uuid4

import click
from cisu.entities.commons import Severity, CoordType, LocationType
from cisu.entities.commons.location_type import LocationShape
from cisu.factories.alert_factory import PrimaryAlertFactory
from cisu.factories.uid_factory import UidFactory
from flask import current_app
from flask.cli import with_appcontext
from shapely.geometry import Polygon, Point

from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity

dir_path = os.path.dirname(os.path.realpath(__file__))


def generate_random(number: int, polygon: Polygon):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points


@click.command("create-affairs")
@click.option('--number', type=int, default=10)
@click.option('--insee_code', type=str)
@click.option('--dept_code', type=str)
@with_appcontext
def create_affairs(number: int, insee_code: str = None, dept_code: str = None):
    uow = current_app.context

    communes_path = dir_path + "/data/communes-version-simplifiee.geojson"
    dept_path = dir_path + "/data/departements-version-simplifiee.geojson"

    if insee_code:
        with open(communes_path) as f:
            data = json.load(f)["features"]
        code = insee_code
    elif dept_code:
        with open(dept_path) as f:
            data = json.load(f)["features"]
        code = dept_code

    else:
        code = "77"
        with open(dept_path) as f:
            data = json.load(f)["features"]

    selected_shape = [feature for feature in data if feature["properties"]["code"] == code][0]
    polygon = Polygon(selected_shape["geometry"]["coordinates"][0])
    points: List[Point] = generate_random(number=number, polygon=polygon)
    affairs = []
    for point in points:
        affair = AffairEntity(
            eventId=UidFactory().build(),
            createdAt=datetime.now(),
            severity=Severity.random(),
            eventLocation=LocationType(
                name="ok",
                address=["test"],
                coord=CoordType(point.y, point.x, height=0),
                type=LocationShape.POINT
            ),
            primaryAlert=PrimaryAlertFactory().build(),
            otherAlert=[],
        )
        simple_affair_entity: SimpleAffairEntity = SimpleAffairEntity(
            uuid=str(uuid4()),
            sge_hub_id=affair.uuid,
            default_affair=affair
        )
        affairs.append(simple_affair_entity)
    with uow:
        uow.session.add_all(affairs)
