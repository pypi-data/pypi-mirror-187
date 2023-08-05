from typing import List
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query

from .base_db_handler import BaseDBHandler


class SqlDBHandler(BaseDBHandler):
    db: SQLAlchemy

    def __init__(self):
        from . import global_session
        self.db = global_session

    @property
    def session(self):
        return self.db.session

    def init_db(self):
        self.db.init_app(current_app)
        self.db.create_all()

    def get_item(self, item_id: int, item_type: type('Item')) -> 'item_type':
        return self.session.query(item_type).filter_by(id=item_id).scalar()

    def get_items_query(self, item_type: type('Item')) -> Query:
        return self.session.query(item_type)

    def add_item(self, item_data: 'Item'):
        self.session.add(item_data)

    def add_items(self, items: List['Item']):
        self.session.add_all(items)

    def update_item(self, item_data: 'Item'):
        raise NotImplementedError('Have not implemented update item')

    def delete_item(self, item_id: int, item_type: type('Item')):
        self.session.query(item_type).filter_by(id=item_id).delete()

    def delete_items(self, item_ids: List[int], item_type: type('Item')):
        for item_id in item_ids:
            self.delete_item(item_id, item_type)

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def reset(self):
        pass
