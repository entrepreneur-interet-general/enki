from flask import request, current_app, g
from flask_restful import Resource, reqparse

from domain.users.command import CreateInvitation
from domain.users.services.invitation_service import InvitationService
from entrypoints.extensions import event_bus
from entrypoints.middleware import user_info_middleware


class WithInvitationRepoResource(Resource):
    def __init__(self):
        pass


class ValidateInvitationResource(WithInvitationRepoResource):
    """

    Validate invitation
    ---
    post:
      description: Creating a invitation
      invitations:
        - invitations
      requestBody:
        content:
          application/json:
            schema:  InvitationSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)

        args = parser.parse_args()
        token: str = args.get("token")
        result = InvitationService.get_invitation_info(token=token, uow=current_app.context)
        return {
                   "message": "success",
                   "data": result
               }, 201


class InvitationResource(WithInvitationRepoResource):
    """Create invitation
    ---
    post:
      description: Creating a invitation
      invitations:
        - invitations
      requestBody:
        content:
          application/json:
            schema:  InvitationSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters
    """

    method_decorators = [user_info_middleware]

    def post(self):
        body = request.get_json()
        body["creator_id"] = g.user_info["id"]
        command = CreateInvitation(data=body)
        result = event_bus.publish(command, current_app.context)
        return {
                   "message": "success",
                   "data": result[0]
               }, 201
