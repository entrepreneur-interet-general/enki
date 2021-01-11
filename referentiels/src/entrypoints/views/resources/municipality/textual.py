from flask import current_app

from flask_restful import Resource, reqparse

from .....domain.geometry.municipality.textual_search_service import MunicipalityTextualSearchService


class MunicipalitiesTextualSearchResource(Resource):
    """Single object resource

    ---

    get:
        description: Getting all current french mayors
        parameters:
          - in: query
            name: query
            schema:
              type: string
            required: true
            description: As you type query
        tags:
            - Municipality

    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, required=True, help='As you type query like : Pari')
        args = parser.parse_args()
        query = args.get("q", 0)

        matches = MunicipalityTextualSearchService.list_cities_by_query(query)
        return {
                   "msg": "success",
                   "results": matches
               }, 200
