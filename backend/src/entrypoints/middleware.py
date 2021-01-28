from functools import wraps
from flask import Response, request, g, current_app
import base64
import json


def user_info_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_app.logger.info(request.headers.get("X-Userinfo"))
        user_info = json.loads(base64.b64decode(request.headers.get("X-Userinfo")))
        current_app.logger.info(user_info)
        g.user_info = user_info
        return func(*args, **kwargs)
    return decorated_function
