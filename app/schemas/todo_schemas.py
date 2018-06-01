from app.extensions import ma

from app.models.todo import Todo


class TodoSchema(ma.ModelSchema):
    class Meta:
        model = Todo
        fields = ('id', 'date_created', 'date_modified', 'title', 'note',
                  'due_date', 'completed_at', 'card_id', 'owner_id', 'completed')
