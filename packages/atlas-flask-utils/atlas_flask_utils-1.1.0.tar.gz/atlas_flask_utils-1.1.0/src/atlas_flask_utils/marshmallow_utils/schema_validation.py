from typing import List

from marshmallow import Schema, EXCLUDE, ValidationError
from flask import request
from werkzeug.exceptions import BadRequest


def unpack_not_none_to_dict(value: any, target: dict):
    if value is not None:
        return {**target, **value}

    return target


class BaseSchema(Schema):
    """
    Meta.strict True means a validation error is thrown if something doesn't fit.
    Meta.unknown Exclude means that instead of throwing an error on bonus data, the bonus data is just ignored.
    """
    class Meta:
        strict = True
        unknown = EXCLUDE


def get_data_groups() -> List:
    data_groups: List = []
    try:
        data_groups.append(request.json)
    except BadRequest:
        pass

    try:
        data_groups.append(request.values)
    except BadRequest:
        pass

    try:
        data_groups.append(request.files)
    except BadRequest:
        pass

    return data_groups


def load_schema(schema, unpack=True):
    """
    Taking the parameters from request json, view_args, args by this order and passing it to the schema for validation.
    :param schema: The resource schema to validate
    :param unpack: Should or shouldn't return values as validate_data or ever value in its own key in the kwargs
    """
    def wrap(f):
        def decorator(*args, **kwargs):
            try:
                data = {}
                data_groups = [kwargs, *get_data_groups()]

                for data_item in data_groups:
                    data = unpack_not_none_to_dict(data_item, data)

                schema_instance: dict = schema().load(data=data)

                if unpack:
                    kwargs.update(**schema_instance)
                else:
                    kwargs.update({'valid_data': schema_instance})
                return f(*args, **kwargs)
            except ValidationError as err:
                return {'error': err.messages}, 400

        return decorator

    return wrap
