from adapters.postgres.orm.user_groups import start_mappers as user_start_mappers
from adapters.postgres.orm.messages import start_mappers as message_start_mappers
from adapters.postgres.orm.metadata import metadata


def start_mappers():
    user_start_mappers()
    message_start_mappers()
    metadata

