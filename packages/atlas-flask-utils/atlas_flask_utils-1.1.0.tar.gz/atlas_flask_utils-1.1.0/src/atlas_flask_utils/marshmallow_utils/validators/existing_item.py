from ...db_utils.queries import get_item_or_abort
from marshmallow.validate import Validator


class ExistingItemValidator(Validator):
    def __init__(self, item_type: type('Item')):
        self.item_type = item_type

    def __call__(self, value: str):
        get_item_or_abort(value, self.item_type)
