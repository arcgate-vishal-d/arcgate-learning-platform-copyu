from account.apis import messages
from account.apis.serializers import PermissionsSerializer


def success_response(data):
    return {
        "message": messages.get_success_message(),
        "code": 200,
        "projects": data,
    }


def failed_response():
    return {
        "message": messages.get_failed_message(),
        "code": 200,
        "results": [],
    }


def error_response():
    return {
        "message": messages.get_not_found_message(),
        "code": 200,
        "results": [],
    }


def login_failed_response():
    return {
        "message": messages.get_login_failed_message(),
        "code": 200,
        "results": [],
    }


def bulk_update_success_response(updated_users, total_users):
    return {
        "message": f"Updated {len(updated_users)} out of {total_users} users successfully",
        "code": 200,
        "results": PermissionsSerializer(updated_users, many=True).data,
    }


def logout_response():
    return {
        "message": messages.get_logout_message(),
        "code": 200,
        "results": [],
    }


def invalid_token_response():
    return {
        "message": messages.get_token_invalid_message(),
        "code": 200,
        "results": [],
    }


def detail_success_response(common_data, project_data):
    return {
        "message": "success",
        "code": 200,
        **common_data,
        "projects": project_data,
    }


def get_not_found_message_response(pagination_data=None):
    message = {"message": messages.get_not_found_message(), "code": 200, "results": []}
    if pagination_data:
        message["pagination"] = pagination_data
    return message
