from abc import ABC, abstractmethod
from typing import List, Any


class BaseDBHandler(ABC):
    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def get_item(self, item_id: int, item_type: type('Item')) -> 'item_type':
        pass

    @abstractmethod
    def get_items_query(self, item_type: type('Item')) -> Any:
        pass

    @abstractmethod
    def add_item(self, item_data: 'Item'):
        pass

    @abstractmethod
    def add_items(self, items: List['Item']):
        pass

    @abstractmethod
    def update_item(self, item_data: 'Item'):
        pass

    @abstractmethod
    def delete_item(self, item_id: int, item_type: type('Item')):
        pass

    @abstractmethod
    def delete_items(self, item_ids: List[int], item_type: type('Item')):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def reset(self):
        pass
