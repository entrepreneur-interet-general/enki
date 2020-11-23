from flask import current_app, request

from flask_restful import Resource, reqparse

from .....domain.elus.maires.service import MaireService


class MairesResource(Resource):
    """Single object resource

    ---

    get:
        description: Getting all current french mayors
        parameters:
          - in: query
            name: code_insee
            schema:
              type: string
            required: false
            description: City code
          - in: query
            name: dept_code
            schema:
              type: string
            required: false
            description: Department code
          - in: query
            name: from
            schema:
              type: int
            required: false
            default: 0
            description: From Pagination
          - in: query
            name: to
            schema:
              type: int
            default: 10
            required: false
            description: To Pagination
        tags:
            - Maires

    """

    def get(self):
        # maires = MaireService.list_maires(repo=current_app.context.maire)

        parser = reqparse.RequestParser()
        parser.add_argument('code_insee', type=str, help='Insee code')
        parser.add_argument('dept_code', type=str, help='Insee code')
        parser.add_argument('from', type=int, help='Insee code')
        parser.add_argument('to', type=int, help='Insee code')


        args = parser.parse_args()
        from_ = args.get("from", 0)
        to_ = args.get("to_", 10)

        if args["code_insee"]:
            matches = MaireService.get_maire_by_code_insee(uuid=args["code_insee"],
                                                           repo=current_app.context.maire)
        elif args["dept_code"]:
            matches = MaireService.list_maires_by_dept_code(dept_code=args["dept_code"],
                                                            from_=from_, to_=to_,
                                                            repo=current_app.context.maire)
        else:
            matches = MaireService.list_maires(from_=from_,
                                               to_=to_,
                                               repo=current_app.context.maire)
        return {
                   "msg": "success",
                   "maires": matches
               }, 200