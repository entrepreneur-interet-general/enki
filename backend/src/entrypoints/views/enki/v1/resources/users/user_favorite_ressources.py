from typing import Dict, Any

from flask import current_app, g
from flask_restful import Resource

from domain.users.services.user_service import UserService
from entrypoints.middleware import user_info_middleware


class WithUserRepoResource(Resource):
    def __init__(self):
        pass


class UserContactListResource(WithUserRepoResource):
    """Get user's contacts
    ---
    get:
      tags:
        - users <> contacts
      responses:
        200:
          description: Return a list of contacts
          content:
            application/json:
              schema:
                type: array
                items: ContactSchema

    """
    method_decorators = [user_info_middleware]

    def get(self):
        uuid = g.user_info["id"]
        contacts = UserService.list_contacts(uuid, uow=current_app.context)
        return {"data": contacts, "user": "success"}, 200


class UserContactResource(WithUserRepoResource):
    """Add, Delete and get specific user's contact
    ---
    get:
      description: Building a relation between a contact and a user
      tags:
        - users <> contacts
      parameters:
        - in: path
          name: contact_uuid
          schema:
            type: string
          required: true
          description: Contact id
      responses:
        200:
          description: Return relation

        404:
            description: relation not found
    put:
      description: Building a relation between a contact and a user
      tags:
        - users <> contacts
      parameters:
        - in: path
          name: contact_uuid
          schema:
            type: string
          required: true
          description: Contact id
      responses:
        201:
          description: Successfully added relation
        404:
            description: relation not found
    delete:
      description: Deleting a relation between a contact and a user
      tags:
        - users <> contacts
      parameters:
        - in: path
          name: contact_uuid
          schema:
            type: string
          required: true
          description: Contact id
      responses:
        202:
          description: Successfully deleted relation
        404:
            description: relation not found
    """
    method_decorators = [user_info_middleware]

    def get(self, contact_uuid: str):
        uuid = g.user_info["id"]
        contact: Dict[str, Any] = UserService.get_user_contact(uuid,
                                                               contact_uuid=contact_uuid,
                                                               uow=current_app.context)
        return {"data": contact, "user": "success"}, 200

    def put(self, contact_uuid: str):
        uuid = g.user_info["id"]
        UserService.add_contact_to_user(uuid,
                                        contact_uuid=contact_uuid,
                                        uow=current_app.context)
        contacts = UserService.list_contacts(uuid, uow=current_app.context)
        return {
                   "message": f"contact {contact_uuid} successfully added from user {uuid}",
                   "data": contacts

               }, 201

    def delete(self, contact_uuid: str):
        uuid = g.user_info["id"]
        UserService.remove_contact_to_user(uuid,
                                           contact_uuid=contact_uuid,
                                           uow=current_app.context)
        contacts = UserService.list_contacts(uuid, uow=current_app.context)
        return {"message": f"contact {contact_uuid} successfully deleted from user {uuid}",
                "data": contacts}, 202
