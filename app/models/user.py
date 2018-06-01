import datetime

from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property

from app.utils import generate_secret_key, encode_jwt
from . import ModelMixin
from .card import Card
from .todo import Todo

from flask_login import UserMixin

from app.extensions import bcrypt


class User(db.Model, ModelMixin, UserMixin):
    __tablename__ = 'users'

    # User table fields
    first_name = db.Column(db.String(55), nullable=False)
    last_name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    _secret_code = db.Column(db.String(6), nullable=True)
    secret_key = db.Column(db.String(12), nullable=False)
    code_sent_at = db.Column(db.DateTime, nullable=True)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean(), default=False)

    # Relationships
    cards = db.relationship('Card', cascade='all, delete-orphan', backref='owner', lazy='dynamic')
    todos = db.relationship('Todo', cascade='all, delete-orphan', backref='owner', lazy='dynamic')

    def __init__(self, first_name, last_name, email, password, active=False):
        """
        Constructor function for User model.

        :param first_name: User first name
        :param last_name:  User last name
        :param email: User email address
        :param password: User password
        """
        self.first_name = first_name
        self.last_name = last_name,
        self.email = email
        self.password = password
        self.active = active

    def __repr__(self):
        """
        Human readable class name representation.
        :return: Model name with user email
        """
        return '<User %r>' % self.email

    @hybrid_property
    def password(self):
        """
        Create reference to _password
        :return: self._password
        """
        return self._password

    @password.setter
    def password(self, value):
        """
        Hash password when setter is triggered and generate new secret key.
        :param value: Raw password
        """

        # Generate password hash
        self._password = bcrypt.generate_password_hash(value)

        # Generate secret key on password change
        self.secret_key = generate_secret_key()

    @hybrid_property
    def secret_code(self):
        """
        Create reference to _secret_code.
        :return: self._secret_code
        """
        return self._secret_code

    @secret_code.setter
    def secret_code(self, value):
        """
        Set _secret_code and code_sent time.
        :param value: New code
        """

        # Set code
        self._secret_code = value

        # Reset code sent time
        if value:
            self.code_sent_at = datetime.datetime.now()

    @property
    def is_active(self):
        """
        Check user account status.
        :return: Boolean
        """
        return self.active

    @staticmethod
    def get_user_by_email(email):
        """
        Query user data using email.

        :param email: User email
        :return: User data or None
        """
        return User.query.filter_by(email=email).first()

    def verify_secret_code(self, code):
        """
        Verify user secret code

        :param code: Verification code
        :return: Boolean
        """

        time_diff = (datetime.datetime.now() - self.code_sent_at)
        time_diff = time_diff.total_seconds() / 60

        # Compare code and time
        if self.secret_code == code and time_diff <= 60:
            return True

        return False

    def confirm_email(self):
        """
        Confirm user account.
        """
        self.secret_code = None
        self.confirmed_at = datetime.datetime.now()
        self.active = True

        return True

    def generate_secret_code(self):
        """
        Generate new secret code.

        :return: Secret code or false
        """

        if self.code_sent_at:
            time_diff = (datetime.datetime.now() - self.code_sent_at)
            time_diff = time_diff.total_seconds() / 60

            if time_diff <= 5:
                return 0

        self.secret_code = generate_secret_key(6, False)

        return self.secret_code

    def verify_password(self, password):
        """
        Verify user password

        :param password: Raw password
        :return: Boolean
        """

        if bcrypt.check_password_hash(self.password, password):
            return True

        return False

    def generate_token(self):
        # Create payload for token
        """
        Generate user access token.
        :return: Token or false
        """

        payload = {
            'email': self.email,
            'secret': self.secret_key
        }

        return encode_jwt(payload)
