from .repository import AbstractMaireRepository
from .entity import MaireEntity


class MaireService:
    @staticmethod
    def add_mairee(maire_data: dict, repo: AbstractMaireRepository):
        maire = MaireEntity(**maire_data)
        repo.add(maire)
