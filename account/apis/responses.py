from account.apis import messages


def success_response(data):
    return {
        "message": messages.get_success_message(),
        "error": False,
        "code": 200,
        "projects": data,
    }


def failed_response():
    return {
        "message": messages.get_failed_message(),
        "error": True,
        "code": 400,
        "result": [],
    }


def error_response():
    return {
        "message": messages.get_not_found_message(),
        "error": True,
        "code": 400,
        "result": [],
    }


def login_failed_response():
    return {
        "message": messages.get_login_failed_message(),
        "error": True,
        "code": 400,
        "result": [],
    }


def refresh_token_required_response():
    return {
        "message": messages.get_refresh_token_required_message(),
        "error": True,
        "code": 400,
        "result": [],
    }
