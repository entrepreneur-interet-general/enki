import itertools
from uuid import uuid4

from flask import current_app
import click
from flask.cli import with_appcontext
import os
from domain.users.entities.group import LocationEntity, LocationType, GroupEntity, GroupType
import json

dir_path = os.path.dirname(os.path.realpath(__file__))


# data from https://github.com/gregoiredavid/france-geojson

mapping = {'Ain': "de l'", 'Aisne': "de l'", 'Allier': "de l'", 'Alpes-de-Haute-Provence': 'des ', 'Hautes-Alpes': 'des ', 'Alpes-Maritimes': 'des ', 'Ardèche': "de l'", 'Ardennes': 'des ', 'Ariège': "de l'", 'Aube': "de l'", 'Aude': "de l'", 'Aveyron': "de l'", 'Bouches-du-Rhône': 'des ', 'Calvados': 'du ', 'Cantal': 'du ', 'Charente': 'de ', 'Charente-Maritime': 'de ', 'Cher': 'du ', 'Corrèze': 'de la ', "Côte-d'Or": 'de ', "Côtes-d'Armor": 'des ', 'Creuse': 'de la ', 'Dordogne': 'de ', 'Doubs': 'du ', 'Drôme': 'de la ', 'Eure': "de l'", 'Eure-et-Loir': "d'", 'Finistère': 'du ', 'Corse-du-Sud': 'de ', 'Haute-Corse': 'de ', 'Gard': 'du ', 'Haute-Garonne': 'de ', 'Gers': 'du ', 'Gironde': 'de ', 'Hérault': "de l'", 'Ille-et-Vilaine': "d'", 'Indre': "de l'", 'Indre-et-Loire': "de l'", 'Isère': "de l'", 'Jura': 'du ', 'Landes': 'des ', 'Loir-et-Cher': 'du ', 'Loire': 'de la ', 'Haute-Loire': 'de ', 'Loire-Atlantique': 'de ', 'Loiret': 'du ', 'Lot': 'du ', 'Lot-et-Garonne': 'du ', 'Lozère': 'de la ', 'Maine-et-Loire': 'du ', 'Manche': 'de la ', 'Marne': 'de la ', 'Haute-Marne': 'de la ', 'Mayenne': 'de ', 'Meurthe-et-Moselle': 'de ', 'Meuse': 'de la ', 'Morbihan': 'du ', 'Moselle': 'de ', 'Nièvre': 'de la ', 'Nord': 'du ', 'Oise': "de l'", 'Orne': "de l'", 'Pas-de-Calais': 'du ', 'Puy-de-Dôme': 'du ', 'Pyrénées-Atlantiques': 'des ', 'Hautes-Pyrénées': 'des ', 'Pyrénées-Orientales': 'des ', 'Bas-Rhin': 'du ', 'Haut-Rhin': 'du ', 'Rhône': 'du ', 'Haute-Saône': 'de ', 'Saône-et-Loire': 'de ', 'Sarthe': 'de la ', 'Savoie': 'de ', 'Haute-Savoie': 'de ', 'Paris': 'de ', 'Seine-Maritime': 'de ', 'Seine-et-Marne': 'de ', 'Yvelines': 'des ', 'Deux-Sèvres': 'des ', 'Somme': 'de la ', 'Tarn': 'du ', 'Tarn-et-Garonne': 'du ', 'Var': 'du ', 'Vaucluse': 'du ', 'Vendée': 'de ', 'Vienne': 'de la ', 'Haute-Vienne': 'de la ', 'Vosges': 'des ', 'Yonne': "de l'", 'Territoire de Belfort': 'du ', 'Essonne': "de l'", 'Hauts-de-Seine': 'des ', 'Seine-Saint-Denis': 'de ', 'Val-de-Marne': 'du ', "Val-d'Oise": 'du '}

@click.command("create-groups-and-locations")
@with_appcontext
def create_group_and_locations():
    uow = current_app.context

    communes_path = dir_path + "/data/communes-version-simplifiee.geojson"
    dept_path = dir_path + "/data/departements-version-simplifiee.geojson"

    with open(communes_path) as f:
        communes_data = json.load(f)["features"]

        communes = [LocationEntity(uuid=str(uuid4()),
                                   label=commune_data["properties"]["nom"],
                                   external_id=commune_data["properties"]["code"],
                                   type=LocationType.VILLE,
                                   # polygon=commune_data["geometry"]["coordinates"]
                                   ) for commune_data in communes_data if commune_data["geometry"]]
    with open(dept_path) as f:
        depts_data = json.load(f)["features"]

        depts = [LocationEntity(uuid=str(uuid4()),
                                label=dept_data["properties"]["nom"],
                                external_id=dept_data["properties"]["code"],
                                type=LocationType.DEPARTEMENT,
                                # polygon=dept_data["geometry"]["coordinates"]
                                ) for dept_data in depts_data]
    prefectures_groups = [
        GroupEntity(
            uuid=str(uuid4()),
            label=f"Préfecture {mapping[dept.label]}{dept.label}",
            type=GroupType.PREFECTURE
        )
        for dept in depts
    ]
    mairies_groups = [
        GroupEntity(
            uuid=str(uuid4()),
            label=f"Mairie de {commune.label}",
            type=GroupType.MAIRIE
        )
        for commune in communes
    ]

    with uow:
        uow.session.add_all(communes)
        uow.session.add_all(depts)
        uow.session.add_all(prefectures_groups)
        uow.session.add_all(mairies_groups)

        for mairie, commune in zip(mairies_groups, communes):
            mairie.location = commune
        for prefecture, dept in zip(prefectures_groups, depts):
            prefecture.location = dept