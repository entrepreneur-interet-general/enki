from datetime import datetime
from tempfile import NamedTemporaryFile

from flask import current_app, send_file
from flask_restful import Resource, reqparse

from domain.evenements.services.evenement_service import EvenementService
from entrypoints.middleware import user_info_middleware


class WithEvenementRepoResource(Resource):
    def __init__(self):
        pass


class EvenementExportResource(WithEvenementRepoResource):
    """Get specific evenement
    ---
    get:
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Event id
      tags:
        - events
      responses:
        200:
          description: Return specific evenement
          content:
            application/json:
              schema: EvenementSchema
    """

    method_decorators = [user_info_middleware]

    def get(self, uuid: str):
        parser = reqparse.RequestParser()
        parser.add_argument('format', type=str, required=True)

        args = parser.parse_args()
        format_: str = args.get("format")

        df = EvenementService.create_dataframe(uuid, current_app.context)
        with NamedTemporaryFile(suffix=f".{format_}") as f:
            if format_ == "csv":
                df.to_csv(f.name, index=False)
            if format_ == "excel":
                df.to_excel(f.name)
            if format_ == "json":
                df.to_json(f.name)
            if format_ == "html":
                df.to_html(f.name)

            return send_file(f.name, f"export_evenement_{uuid}_{datetime.now()}.{format_}", as_attachment=True)
