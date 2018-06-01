from abc import ABC, abstractmethod


class Seeder(ABC):
    def call(self, cls_name):
        """
        Call seeder class.
        :param cls_name: Seeder class name
        """
        print("Seeding: " + cls_name.__name__)

        seeder_obj = cls_name()
        seeder_obj.run()

    @abstractmethod
    def run(self):
        """
        Required seeder runnable function.
        """
        pass
