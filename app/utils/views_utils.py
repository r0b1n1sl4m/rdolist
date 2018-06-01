from flask import jsonify


#  Create consistent json response
def json_response(
        status='success',
        code=200,
        errors=None,
        message='OK',
        data=None
        ):
    """
    Create consistent json response.

    :param status: Response status
    :param code: Response status code
    :param errors: Response errors
    :param message: Response custom message
    :param data: Response data
    :return: JSON response
    """

    response = {
        'status': status,
        'code': code,
        'errors': errors,
        'message': message,
        'data': data
    }

    return jsonify(response), code


# Create consistent json response with error
def json_response_with_error(
        status='failed',
        code=404,
        errors=True,
        message='',
        data=None
        ):
    """
    Create consistent JSON response with error.

    :param status: Response status
    :param code: Response status code
    :param errors: Response errors
    :param message: Response custom message
    :param data: Response data
    :return:
    """

    return json_response(status, code, errors, message, data)
