from flask_api import status
from flask_restful import abort

from .db_handlers import db
from .helper_models.item import Item


def get_item_or_abort(item_id: str, item_type: type(Item)) -> Item:
    item: Item = db.get_item(item_id, item_type)
    if not item:
        abort(status.HTTP_404_NOT_FOUND, error=f'Item of type {item_type.__name__} with id {item_id} not found.')

    return item
