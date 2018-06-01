from faker import Faker

from app.extensions import db
from app.models.user import User
from .seeder import Seeder


class UsersSeeder(Seeder):
    def run(self):
        """
        Run UsersSeeder actions.
        """

        # Drop all collections
        db.session.query(User).delete()

        # Generate fake data
        faker = Faker()

        for user in range(30):
            user = User(**{
                'first_name': faker.first_name(),
                'last_name': faker.last_name(),
                'email': faker.email(),
                'password': faker.password(),
                'active': True,
            })
            db.session.add(user)

        # Commit db session
        db.session.commit()
