from datetime import datetime

from functools import wraps

from webargs import fields, validate

from flask_login import current_user

from app.utils.views_utils import json_response_with_error

from .card_utils import validate_card_existent, validate_ownership

from app.models.todo import Todo


# Utilities
def validate_todo_id(f):
    """
    Validate todo id decorator.
    :param f: Route function
    :return: Route function | Error
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        todo = Todo.query.get(kwargs['todo_id'])

        # Check existent and ownership
        error = None
        if todo:
            if not todo.owner_id == current_user.id:
                error = ['You are not the real owner of this Todo.']
        else:
            error = ['Invalid Todo id.']

        # Through error response
        if error:
            return json_response_with_error(
                code=422,
                errors={
                    'todo_id': error
                },
                message='Todo ID is invalid or access denied.'
            )

        return f(*args, **kwargs)

    return decorated_function


def get_todo_list(state='all'):
    """
    Get todo list.
    :param state: Todo sate
    :return Todo lists
    """

    if state == 'completed':
        todos = Todo.query.filter_by(owner_id=current_user.id, completed=True).all()

    elif state == 'incomplete':
        todos = Todo.query.filter_by(owner_id=current_user.id, completed=False).all()

    elif state == 'delayed':
        todos = Todo.query.filter(Todo.owner_id == current_user.id, Todo.completed < 1,
                                  Todo.due_date < datetime.now()).all()

    else:
        todos = Todo.query.filter_by(owner_id=current_user.id).all()

    return todos


# Reusable args
title = fields.String(validate=[validate.Length(max=255)],
                      required=True)

note = fields.String(missing=None, required=False)

due_date = fields.DateTime(missing=None, required=False)

card_id = fields.Integer(validate=[validate_card_existent, validate_ownership],
                         missing=None, required=False)


# Create todo args
create_todo_args = {
    'title': title,
    'note': note,
    'due_date': due_date,
    'card_id': card_id
}

# Update todo args
update_todo_args = {
    'title': title,
    'note': note,
    'due_date': due_date
}

# Change Card ID args
change_card_id_args = {
    'card_id': fields.Integer(validate=[validate_card_existent, validate_ownership],
                              required=True)
}

