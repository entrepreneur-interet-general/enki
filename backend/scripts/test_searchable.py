from sqlalchemy_searchable import search
from flask import current_app
from domain.users.entities.group import GroupEntity

uow = current_app.context
with uow:
    query = uow.session.query(GroupEntity)
    query = search(query, "Pré")
    print(query.all())
