import string
import random
import jwt

from flask import current_app


def generate_secret_key(size=12, allow_string=True):
    """
    Generate secret key

    :param size: Secret key size
    :param allow_string: Include string inside generated key
    :return: Random string
    """

    # Create choices
    if allow_string:
        chars = string.ascii_letters + string.digits
    else:
        chars = string.digits

    return ''.join(random.choice(chars) for _ in range(size))


# JWT Utils
def encode_jwt(paylaod):
    return jwt.encode(paylaod, current_app.config['SECRET_KEY'])


def decode_jwt(encoded_key):
    return jwt.decode(encoded_key, current_app.config['SECRET_KEY'])
