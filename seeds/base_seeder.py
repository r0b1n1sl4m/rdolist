from . import Seeder

from .users_seeder import UsersSeeder
from .cards_seeder import CardsSeeder
from .todos_seeder import TodosSeeder


class BaseSeeder(Seeder):
    def __init__(self, seeder_name=None):
        """
        Run a single seeder.
        :param seeder_name: Seeder class name.
        """
        self.seeder_name = seeder_name

    def run(self):
        """
        Run base database seeder.
        """

        # Run single seeder if seeder_name exists
        if self.seeder_name:
            self.call(eval(self.seeder_name))
        else:
            self.call(UsersSeeder)
            self.call(CardsSeeder)
            self.call(TodosSeeder)
