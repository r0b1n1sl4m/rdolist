from flask import jsonify
from flask_classful import FlaskView, route
from webargs.flaskparser import use_args
from flask_login import login_required, current_user

from app.extensions import db

from app.models.user import User
from app.utils import generate_secret_key
from app.utils.user_utils import (
    create_user_args,
    confirm_user_args,
    request_user_code_args,
    reset_user_password,
    authenticate_user_args,
    update_user_args
)
from app.utils.views_utils import json_response, json_response_with_error

from app.schemas.user_schemas import UserSchema


class UsersView(FlaskView):

    @route('/', methods=['POST'])
    @use_args(create_user_args)
    def create(self, args):
        """
        Perform user signup.

        :param args: New user validated information
        :return: New user account information
        """

        # Create new user
        user = User(**args)
        user.secret_code = generate_secret_key(6, False)
        user.save()
        db.session.commit()

        # Send welcome email
        from app.tasks.user_tasks import send_welcome_email
        send_welcome_email.delay(user.email)

        # Send verification code
        from app.tasks.user_tasks import send_verification_code_email
        send_verification_code_email.delay(user.email, user.secret_code)

        # Respond with user data
        user_schema = UserSchema()
        return json_response(
            code=201,
            message='Successfully created an user account.',
            data=[user_schema.dump(user).data]
        )

    @route('/', methods=['GET'])
    @login_required
    def read(self):
        """
        Read user account information.
        :return: User account information.
        """
        user_schema = UserSchema()

        return json_response(
            message='User account information enquiry was successful.',
            data=[user_schema.dump(current_user).data]
        )

    @route('/', methods=['PUT'])
    @login_required
    @use_args(update_user_args)
    def update(self, args):
        """
        Update user information.
        :param args: Input data
        :return: Updated information.
        """

        # Update new info
        user = current_user
        user.first_name = args['first_name']
        user.last_name = args['last_name']
        user.save()
        db.session.commit()

        user_schema = UserSchema()

        return json_response(
            message='Account information has been successfully updated.',
            data=[user_schema.dump(user).data]
        )

    @route('/request_code/', methods=['GET'])
    @use_args(request_user_code_args)
    def request_code(self, args):
        """
        Send new secret code.

        :param args: Input data
        :return: Request Status
        """

        email = args['email']

        user = User.get_user_by_email(email)

        # Return new code or false
        code = user.generate_secret_code()

        if code:
            # Send email with new verification code
            from app.tasks.user_tasks import send_verification_code_email
            send_verification_code_email.delay(email, code)

            # Save new code
            user.save()
            db.session.commit()

            return json_response(
                message='Verification code has been sent.'
            )

        return json_response_with_error(
            code=403,
            errors={
                'limit': ['You must wait 5 minutes before you can request another code.']
            },
            message='You can only request new code after each 5 minutes.'
        )

    @route('/confirm/', methods=['POST'])
    @use_args(confirm_user_args)
    def confirm(self, args):
        """
        Confirm user account with valid verification code.

        :param args: Input data
        :return: Confirmation status
        """

        email = args['email']
        code = args['code']

        user = User.get_user_by_email(email)

        # Check if already confirmed
        if user.confirmed_at:
            return json_response(
                message='Account has been already verified.'
            )

        # Verify and confirm account
        if user.verify_secret_code(code):
            user.confirm_email()
            user.save()
            db.session.commit()

            return json_response(
                message='Verification has been completed.'
            )

        # Output error for incorrect verification code
        return json_response_with_error(
            code=422,
            errors={
                'code': ['Incorrect verification code.']
            },
            message='Incorrect verification code or has expired.'
        )

    @route('/reset_password/', methods=['POST'])
    @use_args(reset_user_password)
    def reset_password(self, args):
        """
         Reset user password.

        :param args: Input data
        :return: Request status
        """

        email = args['email']
        password = args['password']
        code = args['code']

        user = User.get_user_by_email(email)

        # Verify and reset password
        if user.verify_secret_code(code):
            user.password = password
            user.secret_code = None
            user.save()
            db.session.commit()

            return json_response(
                message='Password has been successfully changed.'
            )

        # Output error for incorrect verification code
        return json_response_with_error(
            code=422,
            errors={
                'code': ['Incorrect verification code.']
            },
            message='Incorrect verification code or has expired.'
        )

    @route('/authenticate/', methods=['POST'])
    @use_args(authenticate_user_args)
    def authenticate(self, args):
        """
        Authenticate and return user access token.

        :param args: Input data
        :return: Access token or errors
        """

        email = args['email']
        password = args['password']

        user = User.get_user_by_email(email)

        # Verify user password
        if user.verify_password(password):
            # Create token
            token = user.generate_token()

            return json_response(
                message='Successfully authenticated.',
                data={
                    'access_token': token.decode()
                }
            )

        return json_response_with_error(
            status='unauthorized',
            code=401,
            errors={
                'password': ['Password mismatch.']
            },
            message='Unable to authenticate user account.'
        )

    @route('/authenticate/', methods=['GET'])
    @login_required
    def validate_auth(self):
        """
        Validate authorization access token.
        :return: User email with status code 200
        """
        return jsonify({
            'email': current_user.email
        }), 200
