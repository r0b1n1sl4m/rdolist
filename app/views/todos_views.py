from datetime import datetime

from flask import request
from flask_classful import FlaskView, route
from webargs.flaskparser import use_args
from flask_login import login_required, current_user

from app.extensions import db

from app.models.todo import Todo

from app.utils.todo_utils import (
    create_todo_args,
    validate_todo_id,
    update_todo_args,
    change_card_id_args,
    get_todo_list
)

from app.utils.views_utils import json_response, json_response_with_error

from app.schemas.todo_schemas import TodoSchema

class TodosView(FlaskView):
    @route('/', methods=['POST'])
    @login_required
    @use_args(create_todo_args)
    def create(self, args):
        """
        Create new todo.

        :param args: New todo validated information
        :return: New todo data
        """

        # Create new todo
        args['owner_id'] = current_user.id
        todo = Todo(**args)
        todo.save()
        db.session.commit()

        # Respond with new todo data
        todo_schema = TodoSchema()
        return json_response(
            code=201,
            message='Successfully created a new todo.',
            data=[todo_schema.dump(todo).data]
        )

    @route('/<int:todo_id>/', methods=['GET'])
    @login_required
    @validate_todo_id
    def read(self, todo_id):
        """
        Read single todo.
        :param todo_id: Todo ID
        :return: JSON response
        """

        # Fetch todo
        todo = Todo.query.get(todo_id)

        # Define schema
        todo_schema = TodoSchema()

        # Return output
        return json_response(
            code=200,
            message='Todo enquiry was successful.',
            data=todo_schema.dump(todo).data
        )

    @route('/', methods=['GET'])
    @login_required
    def read_all(self):
        """
        Read all todo list.
        :return: Todo list data
        """

        # Get arg
        state = request.args.get(key='state', default='all', type=str)

        # Fetch todo list
        todos = get_todo_list(state)

        # Define schema
        todos_schema = TodoSchema(many=True)

        # Return output
        return json_response(
            code=200,
            message='Todo list enquiry was successful.',
            data=todos_schema.dump(todos).data
        )

    @route('/<int:todo_id>/', methods=['PUT'])
    @login_required
    @validate_todo_id
    @use_args(update_todo_args)
    def update(self, args, todo_id):
        """
        Update todo info.
        :param args: Validated input
        :param todo_id: Todo ID
        :return: Updated information
        """

        # Get args
        title = args['title']
        note = args['note']
        due_date = args['due_date']

        # Update todo
        changed = False
        todo = Todo.query.get(todo_id)

        if title and not title == todo.title:
            todo.title = title
            changed = False

        if note and not note == todo.note:
            todo.note = note
            changed = False

        if due_date and not due_date == todo.due_date:
            todo.due_date = due_date
            changed = False

        # Save new record
        if changed:
            todo.save()
            db.session.commit()

        # Define schema
        todo_schema = TodoSchema()

        # Return output
        return json_response(
            code=200,
            message='Todo information has been successfully updated.',
            data=todo_schema.dump(todo).data
        )

    @route('/<int:todo_id>/mark_complete/', methods=['PUT'])
    @login_required
    @validate_todo_id
    def mark_complete(self, todo_id):
        """
        Mark todo as completed.
        :param todo_id: Todo ID
        :return: Action status
        """

        # Fetch todo
        todo = Todo.query.get(todo_id)

        # Mark complete
        todo.completed_at = datetime.now()
        todo.completed = True
        todo.save()
        db.session.commit()

        # Return output
        return json_response(
            code=200,
            message='Todo has been marked completed.',
        )

    @route('/<int:todo_id>/', methods=['PUT'])
    @login_required
    @validate_todo_id
    @use_args(change_card_id_args)
    def change_card_id(self, args, todo_id):
        """
        Change todo card ID.
        :param args: Validated input
        :param todo_id: Todo ID
        :return: Action status with new info
        """

        # Fetch todo
        todo = Todo.query.get(todo_id)

        # Update card ID
        if not args['card_id'] == todo.card_id:
            todo.card_id = args['card_id']
            todo.save()
            db.session.commit()

        # Define schema
        todo_schema = TodoSchema()

        # Return output
        return json_response(
            code=200,
            message='Todo information has been successfully updated.',
            data=todo_schema.dump(todo).data
        )

    @route('/<int:todo_id>/', methods=['DELETE'])
    @login_required
    @validate_todo_id
    def delete(self, todo_id):
        """
        Delete todo.
        :param todo_id: Todo ID
        :return Action status
        """

        # Delete todo
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()

        # Return output
        return json_response(
            code=200,
            message='Card has been deleted successfully.',
        )
