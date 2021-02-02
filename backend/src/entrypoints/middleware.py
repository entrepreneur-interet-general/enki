from functools import wraps
from flask import Response, request, g, current_app
import base64
import json


def user_info_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_info = request.headers.get("X-Userinfo")
        if user_info:
            user_info = json.loads(base64.b64decode(user_info))
            current_app.logger.info(f"User info provided : {user_info}")
            g.user_info = user_info
        else:
            current_app.logger.info("No user info provided...")
            g.user_info = {
                "id": "my-test-user-id"
            }

        current_app.logger.info(func)
        return func(*args, **kwargs)

    return decorated_function


def user_object_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        uow = current_app.context
        with uow:
            g.user = uow.user.get_by_uuid(g.user_info["id"])
        return func(*args, **kwargs)

    return decorated_function
