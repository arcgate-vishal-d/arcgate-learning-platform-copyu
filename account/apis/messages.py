def get_success_message():
    return "success"


def get_failed_message():
    return "failed"


def get_not_found_message():
    return "No matching results found."


def get_login_failed_message():
    return "Token is invalid Please login Again."


def get_bulk_update_success_message(updated_count, total_count):
    return f"Updated {updated_count} out of {total_count} users successfully"


def get_refresh_token_required_message():
    return "Refresh token is required."


def get_logout_message():
    return "Logout successfully."


def get_token_invalid_message():
    return "Token is invalid"
