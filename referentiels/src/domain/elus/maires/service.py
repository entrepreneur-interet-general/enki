from typing import List, Dict

from .repository import AbstractMaireRepository
from .entity import MaireEntity


class MaireService:
    @staticmethod
    def add_maire(maire_data: dict, repo: AbstractMaireRepository):
        maire = MaireEntity(**maire_data)
        repo.add(maire)

    @staticmethod
    def list_maires(from_: int, to_: int, repo: AbstractMaireRepository) -> List[Dict]:
        maires = repo.get_all(from_, to_)
        return [maire.to_dict() for maire in maires]

    @staticmethod
    def list_maires_by_dept_code(dept_code: str, from_: int, to_: int, repo: AbstractMaireRepository):
        maires = repo.get_by_dept_code(dept_code=dept_code, from_=from_, to_=to_)
        return [maire.to_dict() for maire in maires]

    @staticmethod
    def get_maire_by_code_insee(uuid: str, repo: AbstractMaireRepository):
        maire = repo.get_by_uuid(uuid=uuid)
        return maire.to_dict()
