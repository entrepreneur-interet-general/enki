from flask import request, current_app, g
from flask_restful import Resource

from domain.users.command import CreateContact
from domain.users.services.contact_service import ContactService
from entrypoints.extensions import event_bus
from entrypoints.middleware import user_info_middleware


class WithContactRepoResource(Resource):
    def __init__(self):
        pass


class ContactListResource(WithContactRepoResource):
    """Get all contacts
    ---
    get:
      tags:
        - contacts
      responses:
        200:
          description: Return a list of contacts
          content:
            application/json:
              schema:
                type: array
                items: ContactSchema
    post:
      description: Creating a contact
      tags:
        - contacts
      requestBody:
        content:
          application/json:
            schema:  ContactSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters
    """

    method_decorators = [user_info_middleware]

    def get(self):
        return {
                   "data": ContactService.list_contacts(current_app.context),
                   "message": "success",
               }, 200

    def post(self):
        body = request.get_json()
        body["creator_id"] = g.user_info["id"]
        command = CreateContact(data=body)
        result = event_bus.publish(command, current_app.context)
        return {
                   "message": "success",
                   "data": result[0]
               }, 201


class ContactResource(WithContactRepoResource):
    """Get specific contact
    ---
    get:
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Contact id
      tags:
        - contacts
      responses:
        200:
          description: Return specific contact
          content:
            application/json:
              schema: ContactSchema
        404:
            description: Contact not found
    """

    def get(self, uuid: str):
        return {
                   "data": ContactService.get_by_uuid(uuid, current_app.context),
                   "message": "success"
               }, 200
