import abc

from ...domain.entities.task import Task

class AbstractRepository(abc.ABC):

    def __init__(self):
        pass

    def save(self, task : Task):
        raise NotImplementedError
    
    def get_by_uuid(self, uuid : str):
        raise NotImplementedError
