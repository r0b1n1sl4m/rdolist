from datetime import datetime

from functools import wraps

from webargs import fields, validate, ValidationError

from flask_login import current_user

from .views_utils import json_response_with_error

from app.models.card import Card
from app.models.todo import Todo


# Utilities
def validate_card_id(f):
    """
    Validate card id decorator.
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        card = Card.query.get(kwargs['card_id'])

        # Check existent and ownership
        error = None
        if card:
            if not card.owner_id == current_user.id:
                error = ['You do not have access to use this card.']
        else:
            error = ['Invalid card id.']

        # Through error response
        if error:
            return json_response_with_error(
                code=422,
                errors={
                    'card_id': error
                },
                message='Card ID is invalid or access denied.'
            )

        return f(*args, **kwargs)

    return decorated_function


# Request validators
def validate_card_existent(id):
    """
    Check card existent.
    :param id: Parent card ID
    """
    card = Card.query.get(id)

    if not card:
        raise \
            ValidationError('Invalid parent card id.')


def validate_ownership(id):
    """
    Check if user has access to the parent card.
    :param id: Parent card ID
    """
    card = Card.query.get(id)

    if card:
        if not card.owner_id == current_user.id:
            raise \
                ValidationError('You do not have access to use this card.')


def get_todo_list(card_id, state='all'):
    """
    Get todo list.
    :param card_id: Card ID
    :param state: Todo sate
    :return Todo lists
    """

    if state == 'completed':
        todos = Todo.query.filter_by(owner_id=current_user.id, card_id=card_id,
                                     completed=True).all()

    elif state == 'incomplete':
        todos = Todo.query.filter_by(owner_id=current_user.id, card_id=card_id,
                                     completed=False).all()

    elif state == 'delayed':
        todos = Todo.query.filter(Todo.owner_id == current_user.id,
                                  Todo.card_id == card_id, Todo.completed < 1,
                                  Todo.due_date < datetime.now()).all()

    else:
        todos = Todo.query.filter_by(owner_id=current_user.id, card_id=card_id).all()

    return todos


# Reusable args
card_title_arg = fields.String(validate=[validate.Length(max=255)],
                               required=True)

card_note_arg = fields.String(missing=None, required=False)

parent_card_id_arg = fields.Integer(validate=[validate_card_existent, validate_ownership])

# Create card args
create_card_args = {
    'title': card_title_arg,
    'note': card_note_arg,
    'parent_card_id': parent_card_id_arg
}

# Update card args
update_card_args = {
    'title': card_title_arg,
    'note': card_note_arg
}

# Update parent card args
update_parent_card_args = {
    'parent_card_id': fields.Integer(validate=[validate_card_existent, validate_ownership],
                                     required=True)
}
