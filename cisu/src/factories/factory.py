from abc import ABC, abstractmethod
from faker import Faker


class AbstractFactory(ABC):
    faker = Faker('fr_FR')

    @abstractmethod
    def generate(self):
        raise NotImplementedError
