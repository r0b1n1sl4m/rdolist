import pytest

from app import create_app
from app.extensions import db as _db


@pytest.yield_fixture(scope='session')
def app(request):
    """
    Create a Flask Test app, this only gets executed once.

    :param request: Flask app
    """

    # Create app
    _app = create_app()

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app test client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app test client
    """

    yield app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    """
    Initialize and reset database for testing.

    :param app: Flask app
    """

    # Initialize database
    _db.app = app
    _db.drop_all()
    _db.create_all()

    # Seed database

    yield _db
