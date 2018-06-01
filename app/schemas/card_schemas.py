from app.extensions import ma

from app.models.card import Card

from .todo_schemas import TodoSchema


class CardSchema(ma.ModelSchema):
    class Meta:
        model = Card
        fields = ('id', 'date_created', 'date_modified', 'title',
                  'note', 'parent_card_id', 'owner_id', 'child_cards', 'todos')


class CardFeedsSchema(ma.ModelSchema):
    class Meta:
        model = Card
        fields = ('id', 'date_created', 'date_modified', 'title',
                  'note', 'parent_card_id', 'owner_id', 'child_cards', 'todos')

    child_cards = ma.Nested('self', many=True)
    todos = ma.Nested(TodoSchema, many=True)
