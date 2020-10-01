from ..task_repository import AbstractRepository
from sapeur_api.domain.entities.task import Task

class SqlTaskRRepository(AbstractRepository): 
    def __init__(self, session : str):
        self.session = session 
    def save(self, task : Task): 
        self.session.add(task)
    def get_by_uuid(self, uuid): 
        self.session.query()