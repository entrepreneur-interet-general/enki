from flask import current_app, request

from flask_restful import Resource, reqparse

from .....domain.elus.maires.service import MaireService


class MairesResource(Resource):
    """Single object resource

    ---
    post:
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