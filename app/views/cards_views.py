from flask import request
from flask_classful import FlaskView, route
from webargs.flaskparser import use_args
from flask_login import login_required, current_user

from app.extensions import db

from app.models.card import Card
from app.utils.card_utils import (
    create_card_args,
    validate_card_id,
    update_card_args,
    update_parent_card_args,
    get_todo_list
)

from app.utils.views_utils import json_response, json_response_with_error

from app.schemas.card_schemas import CardSchema, CardFeedsSchema
from app.schemas.todo_schemas import TodoSchema


class CardsView(FlaskView):

    @route('/', methods=['POST'])
    @login_required
    @use_args(create_card_args)
    def create(self, args):
        """
        Create new card.

        :param args: New card validated information
        :return: New card data
        """

        # Create new card
        args['owner_id'] = current_user.id
        card = Card(**args)
        card.save()
        db.session.commit()

        # Respond with new card data
        card_schema = CardSchema()
        return json_response(
            code=201,
            message='Successfully created a new card.',
            data=[card_schema.dump(card).data]
        )

    @route('/<int:card_id>/', methods=['GET'])
    @login_required
    @validate_card_id
    def read(self, card_id):
        """
        Read single card.
        :param card_id: Card ID
        :return: JSON response
        """

        # Fetch card
        card = Card.query.get(card_id)

        # Define schema
        card_schema = CardSchema()

        # Return output
        return json_response(
            code=200,
            message='Card enquiry was successful.',
            data=card_schema.dump(card).data
        )

    @route('/<int:card_id>/todos/', methods=['GET'])
    @login_required
    @validate_card_id
    def todos(self, card_id):
        """
        Read specific card todos.
        :param card_id: Card ID
        :return: Card todo list
        """

        # Get args
        state = request.args.get(key='state', default='all', type=str)

        # Fetch todo list
        todos = get_todo_list(card_id, state)

        # Define schema
        todos_schema = TodoSchema(many=True)

        # Return output
        return json_response(
            code=200,
            message='Card todos enquiry was successful.',
            data=todos_schema.dump(todos).data
        )

    @route('/feed/<int:card_id>/')
    @login_required
    @validate_card_id
    def card_feeds(self, card_id):
        """
        Read single card feeds.
        :param card_id: Card ID
        :return: JSON Response
        """

        # Fetch card
        card = Card.query.get(card_id)

        # Define schema
        card_feeds_schema = CardFeedsSchema()

        # Return output
        return json_response(
            code=200,
            message='Card feeds enquiry was successful.',
            data=card_feeds_schema.dump(card).data
        )

    @route('/feed/', methods=['GET'])
    @login_required
    def cards_feed(self):
        """
        Fetch cards with child cards and todo list.
        :return: JSON response
        """

        # Fetch cards
        cards = Card.query.filter_by(parent_card=None, owner_id=current_user.id)

        # Define schema
        cards_feed_schema = CardFeedsSchema(many=True)

        # Return output
        return json_response(
            code=200,
            message='Cards feed enquiry was successful.',
            data=cards_feed_schema.dump(cards).data
        )

    @route('/<int:card_id>/', methods=['PUT'])
    @login_required
    @validate_card_id
    @use_args(update_card_args)
    def update(self, args, card_id):
        """
        Update card info.
        :param args: Validated input
        :param card_id: Card ID
        :return: Status with updated info
        """

        # Extract args
        title = args['title']
        note = args['note']

        # Update card
        changed = False
        card = Card.query.get(card_id)

        if not title == card.title:
            card.title = title
            changed = True

        if note and not note == card.note:
            card.note = note
            changed = True

        # Save new record
        if changed:
            card.save()
            db.session.commit()

        # Define schema
        card_schema = CardSchema()

        # Return output
        return json_response(
            code=200,
            message='Card information has been successfully updated.',
            data=card_schema.dump(card).data
        )

    @route('/<int:card_id>/change_parent/', methods=['PUT'])
    @login_required
    @validate_card_id
    @use_args(update_parent_card_args)
    def change_parent(self, args, card_id):
        """
        Change card parent ID.
        :param args: Validated input
        :param card_id: Card ID
        :return: Status with new info
        """

        # Fetch card
        card = Card.query.get(card_id)

        if card.change_parent(args['parent_card_id']):
            # Save updated info
            card.save()
            db.session.commit()

            # Define schema
            card_schema = CardSchema()

            # Return output
            return json_response(
                code=200,
                message='Card information has been successfully updated.',
                data=card_schema.dump(card).data
            )

        # Return error output
        return json_response_with_error(
            code=422,
            errors={
                'parent_card_id': ['Invalid parent card id.']
            },
            message='You can not use child card as a parent card.'
        )

    @route('/<int:card_id>/', methods=['DELETE'])
    @login_required
    @validate_card_id
    def delete(self, card_id):
        """
        Delete card and associate child cards with todo list.
        :param card_id: Card ID
        :return: Action status
        """

        # Delete card
        card = Card.query.get(card_id)
        db.session.delete(card)
        db.session.commit()

        # Return output
        return json_response(
            code=200,
            message='Card has been deleted successfully.',
        )
