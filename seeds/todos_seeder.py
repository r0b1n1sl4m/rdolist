import random

from faker import Faker

from app.extensions import db
from app.models.todo import Todo
from app.models.card import Card
from .seeder import Seeder


class TodosSeeder(Seeder):
    def run(self):
        """
        Run TodosSeeder actions.
        """

        # Drop all collections
        db.session.query(Todo).delete()

        # Generate cards id list
        cards = Card.query.all()
        card_ids = list(map(lambda card: card.id, cards))

        # Generate fake data
        faker = Faker()

        for todo in range(180):
            card = random.choice(cards)
            todo = Todo(**{
                'owner_id': card.owner_id,
                'title': faker.sentence(),
                'note': faker.paragraph(nb_sentences=2),
                'card_id': card.id,
            })
            db.session.add(todo)

        # Commit db session
        db.session.commit()
