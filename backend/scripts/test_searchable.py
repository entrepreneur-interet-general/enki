from sqlalchemy_searchable import search
from flask import current_app
from sqlalchemy import func

from domain.users.entities.group import GroupEntity

uow = current_app.context
with uow:
    query = uow.session.query(GroupEntity).filter(GroupEntity.search_vector.op('@@')(func.plainto_tsquery('Pré')))
    print(query.all())
    query = search(query, "Pré")
