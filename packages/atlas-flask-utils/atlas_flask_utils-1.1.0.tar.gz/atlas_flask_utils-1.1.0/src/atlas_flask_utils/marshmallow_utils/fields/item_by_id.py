from ...db_utils.helper_models.item import Item
from ...db_utils.queries import get_item_or_abort
from marshmallow import fields


class ItemByIdField(fields.Int):
    def __init__(self, item_type: type('Item'), **kwargs):
        super(ItemByIdField, self).__init__(**kwargs)
        self.__item_type = item_type

    def _deserialize(self, value, attr, data, **kwargs) -> Item:
        return get_item_or_abort(value, self.__item_type)

