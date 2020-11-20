from datetime import datetime

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class MaireEntity:
    """
    dept_code:str = 'Code du département (Maire)'
    dept_label:str = 'Libellé de département (Maires)'
    insee_code = 'Code Insee de la commune'
    city_label = 'Libellé de la commune'
    name = "Nom de l'élu"
    firstname = "Prénom de l'élu"
    sexe = 'Code sexe'
    birthdate = 'Date de naissance'
    work_code = 'Code profession'
    work_label = 'Libellé de la profession'
    start_at = 'Date de début du mandat'
    end_at = 'Date de début de la fonction'
    """

    dept_code: str
    dept_label: str
    insee_code: int
    city_label: str
    name: str
    firstname: str
    sexe: str
    birthdate: datetime
    work_code: float
    work_label: str
    start_position_at: datetime
    start_mandat_at: datetime
