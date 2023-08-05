from abc import ABC, abstractmethod
from typing import Type

from ..db_utils.db_handlers import db
from ..db_utils.helper_models.item import Item


class SerializerError(Exception):
    pass


class BaseSerializer(ABC):
    _model: Item

    def __init__(self, model: Item = None, model_id: int = None):
        self._model = model

        if not model:
            if model_id:
                self._model = db.get_item(model_id, self._model_type)
            else:
                raise SerializerError('Serializer received neither a model nor an id.')

    @property
    @abstractmethod
    def _model_type(self) -> Type[Item]:
        pass

    @abstractmethod
    def _fetch_sub_models(self):
        pass

    @abstractmethod
    def _make_dict(self) -> dict:
        pass

    def serialize(self) -> dict:
        self._fetch_sub_models()
        return self._make_dict()
