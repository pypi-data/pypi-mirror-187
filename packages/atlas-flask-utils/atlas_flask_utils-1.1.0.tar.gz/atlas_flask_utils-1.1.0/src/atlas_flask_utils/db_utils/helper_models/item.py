from abc import ABC, abstractmethod
from typing import Union

from ..db_handlers import global_session


class AbstractSqlAlchemyMetaClass(type(ABC), type(global_session.Model)):
    pass


class Item(ABC, global_session.Model, metaclass=AbstractSqlAlchemyMetaClass):
    __abstract__ = True

    id: Union[int, global_session.Column] = global_session.Column('Id', global_session.Integer, primary_key=True,
                                                                  autoincrement=True)

    def __init__(self, item_id: int):
        self.id = item_id

    @abstractmethod
    def _serialize(self, *args, **kwargs) -> dict:
        pass

    def serialize(self, *args, **kwargs) -> dict:
        return {
            'id': self.id,
            **self._serialize(*args, **kwargs)
        }
