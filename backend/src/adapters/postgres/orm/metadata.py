import logging

from datetime import datetime
from sqlalchemy import Table, MetaData, Column, String, ForeignKey, Integer, TIMESTAMP, Enum
from sqlalchemy_searchable import make_searchable


logger = logging.getLogger(__name__)

metadata = MetaData()

make_searchable(metadata=metadata)
