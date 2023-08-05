from flask_sqlalchemy import SQLAlchemy

from .base_db_handler import BaseDBHandler
from .sql_db_handler import SqlDBHandler

global_session = SQLAlchemy()
db: BaseDBHandler = SqlDBHandler()
