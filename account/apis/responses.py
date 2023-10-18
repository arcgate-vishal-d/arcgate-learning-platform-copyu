from account.apis import messages


def success_response(data):
    return {
        "message": messages.get_success_message(),
        "error": False,
        "code": 200,
        "projects": [data],
    }


def failed_response():
    return {
        "message": messages.get_failed_message(),
        "error": True,
        "code": 200,
        "result": [],
    }


def error_response():
    return {
        "message": messages.get_not_found_message(),
        "error": True,
        "code": 200,
        "result": [],
    }


def Login_failed_response():
    return {
        "message": messages.get_login_failed_message(),
        "error": True,
        "code": 200,
        "result": [],
    }
