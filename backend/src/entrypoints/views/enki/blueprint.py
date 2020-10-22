from flask import Blueprint
from .v1.blueprint import enki_v1_blueprint

enki_blueprint = Blueprint(name="enki", import_name=__name__, url_prefix="/api/enki/")
enki_blueprint.add

