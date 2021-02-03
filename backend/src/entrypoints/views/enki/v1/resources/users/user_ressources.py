from flask import request, current_app, g
from flask_restful import Resource

from domain.users.command import CreateUser
from domain.users.services.user_service import UserService
from entrypoints.extensions import event_bus
from entrypoints.middleware import user_info_middleware


class WithUserRepoResource(Resource):
    def __init__(self):
        pass


class UserListResource(WithUserRepoResource):
    """Get all users
    ---
    get:
      tags:
        - users
      security:
        - jwt: []
      responses:
        200:
          description: Return a list of users
          content:
            application/json:
              schema:
                type: array
                items: UserSchema
    post:
      description: Creating a user
      security:
        - jwt: []
      tags:
        - users
      requestBody:
        content:
          application/json:
            schema:  UserSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters
    """

    method_decorators = [user_info_middleware]

    def get(self):
        return {
                   "data": UserService.list_users(current_app.context),
                   "message": "success",
               }, 200

    def post(self):
        body = request.get_json()
        body["uuid"] = g.user_info["id"]
        command = CreateUser(data=body)
        result = event_bus.publish(command, current_app.context)
        return {
                   "message": "success",
                   "data": result[0]
               }, 201


class UserResource(WithUserRepoResource):
    """Get specific user
    ---
    get:
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: User id
      tags:
        - users
      responses:
        200:
          description: Return specific user
          content:
            application/json:
              schema: UserSchema
        404:
            description: User not found
    """

    def get(self, uuid: str):
        return {
                   "data": UserService.get_by_uuid(uuid, current_app.context),
                   "message": "success"
               }, 200
