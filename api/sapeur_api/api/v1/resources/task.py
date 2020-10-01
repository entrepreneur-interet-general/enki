from flask_restful import Resource
from flask import current_app
from ....domain.models import Task
from ..schemas import TaskSchema
from hashlib import sha1


class TaskList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """

    def get(self):
        schema = TaskSchema()
        task = Task(id=sha1().hexdigest())
        current_app.context.task_repository.add(task=task)

        return {"msg": "user created", "user": schema.dump(task)}, 201
