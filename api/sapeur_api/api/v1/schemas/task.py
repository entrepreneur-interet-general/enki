from ....domain.models import Task
from ....extensions import ma, db


class TaskSchema(ma.SQLAlchemySchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Task
        sqla_session = db.session
        load_instance = True
