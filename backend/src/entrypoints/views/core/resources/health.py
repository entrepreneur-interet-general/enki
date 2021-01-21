from flask import g
from flask_restful import Resource

from entrypoints.extensions import oidc


class HealthResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - core
    """

    decorators = [oidc.accept_token()]

    @oidc.accept_token(require_token=True, scopes_required=['openid'])
    def get(self):

        return {
            "ok": "ok",
            "data":g.oidc_token_info['sub']
        }
