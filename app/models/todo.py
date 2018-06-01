from app.extensions import db

from . import ModelMixin


class Todo(db.Model, ModelMixin):
    __tablename__ = 'todos'

    # Todo table fields
    title = db.Column(db.String(255), nullable=False)
    note = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    notified = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id', ondelete='CASCADE'), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, owner_id, title, note=None, due_date=None, card_id=None):
        """
        Constructor function for Todo model.

        :param card_id: Card id
        :param title: Todo title
        :param note: Todo note
        :param due_date: Todo due date
        """
        self.owner_id = owner_id
        self.title = title
        self.note = note
        self.due_date = due_date
        self.card_id = card_id

    def __repr__(self):
        """
        Human readable class name representation.
        :return: Model name with todo title
        """
        return '<Todo %r>' % self.title

