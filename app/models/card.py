from app.extensions import db

from . import ModelMixin
from .todo import Todo

class Card(db.Model, ModelMixin):
    __tablename__ = 'cards'

    # Card table fields
    title = db.Column(db.String(255), nullable=False)
    note = db.Column(db.Text, nullable=True)
    parent_card_id = db.Column(db.Integer, db.ForeignKey('cards.id', ondelete='CASCADE'), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    child_cards = db.relationship('Card', cascade='all', backref=db.backref('parent_card', remote_side='Card.id'), lazy='dynamic')
    todos = db.relationship('Todo', cascade='all, delete-orphan', backref='card', lazy='dynamic')

    def __init__(self, owner_id, title, note=None, parent_card_id=None):
        """
        Constructor function for Card model.

        :param owner_id: Card owner id
        :param title: Card title
        :param note: Card note
        :param parent_card_id: Parent Card id
        """
        self.owner_id = owner_id
        self.title = title
        self.note = note
        self.parent_card_id = parent_card_id

    def __repr__(self):
        """
        Human readable class name representation.
        :return: Model name with card title
        """
        return '<Card %r>' % self.title

    def is_parent_of(self, child_card_id):
        """
        Check if card has a child with ID of the child card.
        :param child_card_id: Child card ID
        :return: Boolean
        """

        # Get child cards
        child_cards = self.child_cards.all()

        # Iterate through child cards and check parent ID
        for child_card in child_cards:
            if child_card.id == child_card_id:
                return True

            # Check ID inside nested child cards
            return child_card.is_parent_of(child_card_id)

        return False

    def change_parent(self, parent_card_id):
        """
        Change parent card ID.
        :param parent_card_id: Parent card ID
        :return: Boolean
        """
        if not self.is_parent_of(parent_card_id):
            # Change parent card ID
            self.parent_card_id = parent_card_id

            return True

        return False
