import re

from webargs import fields, validate, ValidationError

from app.models.user import User


# Utils


# Request validators
def validate_unique_email(email):
    """
    Request parser unique email validator.

    :param email: Input email
    """

    if (User.get_user_by_email(email)):
        raise \
            ValidationError('User associated with this email already exists.')


def validate_user_email_exist(email):
    """
    Request parser user email exist validator.

    :param email: User email
    """

    if not (User.get_user_by_email(email)):
        raise \
            ValidationError('User does not exists associated with this email.')


def validate_strong_password(password):
    """
    Validate request parser password.

    :param password: Input password
    """

    # Validation rules
    xp = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[\S]{6,}$')

    # Match password
    if not xp.match(password):
        raise ValidationError('Enter a combination of at least 6 numbers,'
                              '(upper and lowercase) letters.')


# Reusable args
user_email_arg = fields.String(validate=[validate.Email(),
                                         validate.Length(max=255),
                                         validate_user_email_exist],
                               required=True)

user_password_arg = fields.String(validate=[validate.Length(max=255),
                                            validate_strong_password],
                                  required=True)

user_secret_code_arg = fields.String(validate=[validate.Length(min=6)],
                                     required=True)

user_name_arg = fields.String(validate=[validate.Length(max=55)],
                              required=True)

# User create args
create_user_args = {
    'first_name': user_name_arg,
    'last_name': user_name_arg,
    'email': fields.String(validate=[validate.Email(),
                                     validate.Length(max=255),
                                     validate_unique_email],
                           required=True),
    'password': user_password_arg,
}

# User confirm args
confirm_user_args = {
    'email': user_email_arg,
    'code': user_secret_code_arg,
}

# Request code args
request_user_code_args = {
    'email': user_email_arg,
}

# Password change args
reset_user_password = {
    'email': user_email_arg,
    'password': user_password_arg,
    'code': user_secret_code_arg,
}

# Authenticate user args
authenticate_user_args = {
    'email': user_email_arg,
    'password': user_password_arg,
}

# Login args
user_login_args = {
    'Access-Token': fields.String(required=True)
}

# User update args
update_user_args = {
    'first_name': user_name_arg,
    'last_name': user_name_arg
}
