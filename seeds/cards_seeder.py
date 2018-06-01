import random

from faker import Faker

from app.extensions import db
from app.models.card import Card
from app.models.user import User
from .seeder import Seeder


class CardsSeeder(Seeder):
    def run(self):
        """
        Run CardsSeeder actions.
        """

        # Drop all collections
        db.session.query(Card).delete()

        # Generate users id list
        users = User.query.all()
        user_ids = list(map(lambda user: user.id, users))

        # Generate fake data
        faker = Faker()

        for card in range(60):
            card = Card(**{
                'owner_id': random.choice(user_ids),
                'title': faker.sentence(),
                'note': faker.paragraph(nb_sentences=2),
            })
            db.session.add(card)

        # Commit db session
        db.session.commit()

        # Generate parent cards id list
        cards = Card.query.all()
        card_ids = list(map(lambda i: cards[i].id, range(10)))

        # Assign parent card id
        for j in range(10, 60):
            cards[j].parent_card_id = random.choice(card_ids)

        # Commit db session
        db.session.commit()
