from flask import Flask

import os
from os.path import join, dirname

from dotenv import load_dotenv

from instance.config import app_config

from .extensions import (
    db,
    ma,
    login_manager,
    bcrypt,
    mail
)

from webargs.flaskparser import use_args

from app.utils import decode_jwt
from app.utils.views_utils import json_response_with_error
from app.utils.user_utils import user_login_args

from app.models.user import User

from .views.index_view import IndexView
from .views.users_views import UsersView
from .views.cards_views import CardsView
from .views.todos_views import TodosView

# Load .env file
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)


def create_app():
    """
    Create a Flask app using the app factory pattern.

    :return: Flask app
    """

    app = Flask(__name__, instance_relative_config=True)

    # Choose config
    mode = os.getenv('MODE')
    app.config.from_object(app_config[mode])
    app.config.from_pyfile('config.py')
    app.config['MODE'] = mode

    # Register extensions
    register_extensions(app, [
        db,
        ma,
        login_manager,
        bcrypt,
        mail
    ])

    # App helper setup
    setup_app_helper(app)

    # Register error handlers
    register_error_handler(app)

    # Register views
    register_views(app)

    # Remove database session on app teardown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app


def register_extensions(app, extensions):
    """
    Register installed extensions.

    :param app: Flask app
    """

    for extension in extensions:
        extension.init_app(app)


def register_views(app):
    """
    Register API Views.

    :param app: Flask app
    """

    IndexView.register(app, route_base='/')
    UsersView.register(app, route_prefix='/api/')
    CardsView.register(app, route_prefix='/api/')
    TodosView.register(app, route_prefix='/api/')


def register_error_handler(app):
    """
    Handle errors.

    :param app: Flask app
    """

    @app.errorhandler(404)
    def page_not_found(error):
        """
        404 request handler.

        :param error: Errors
        :return: JSON response
        """
        return json_response_with_error(
            message='Requested endpoint not found.'
        )

    @app.errorhandler(422)
    def handle_unprocessable_entity(error):
        """
        Return formatted output for 422 error.

        :param error: Errors
        :return: Error response
        """

        data = getattr(error, 'data')

        return json_response_with_error(
            code=422,
            errors=data['messages'],
            message='Input validation error.'
        )

    @app.errorhandler(401)
    def handle_unauthorized(error):
        return json_response_with_error(
            status='unauthorized',
            code=401,
            errors={
                'Access-Token': ['Invalid access token.']
            },
            message='Authentication failed.'
        )


def setup_app_helper(app):
    # Login user
    @login_manager.request_loader
    @use_args(user_login_args, locations=('headers',))
    def load_user_from_request(request, args):
        """
        Load user using access-token.

        :param request: App request
        :param args: Input data
        :return: User
        """

        access_token = args['Access-Token']

        try:
            # Decode payload
            payload = decode_jwt(access_token)

            return User.query.filter_by(email=payload['email'],
                                        secret_key=payload['secret']).first()

        except Exception as e:
            return None
