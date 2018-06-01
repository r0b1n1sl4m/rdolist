from flask import json, url_for


def validate_json_data(data, rules_list):
    """
    Validate JSON data.

    :param data: JSON data
    :param rules_list: Rules list to compare value
    :return: Boolean
    """

    for rule in rules_list:
        if rule[1] != data[rule[0]]:
            if len(rule) < 3:
                return False
    return True


def validate_login_required(client, route, request_type):
    """
    Test login required decorator.

    :param client: Test app client
    :param route: Route string
    :param request_type: Route request type
    """

    if request_type == 'POST':
        response = client.post(url_for(route))
    elif request_type == 'GET':
        response = client.get(url_for(route))
    elif request_type == 'PUT':
        response = client.put(url_for(route))
    else:
        response = client.delete(url_for(route))

    data = json.loads(response.data)

    assert validate_json_data(data, [
        ['status', 'failed'],
        ['code', 422],
        ['errors', None, 1],
    ])
    assert data['errors']['Access-Token']
