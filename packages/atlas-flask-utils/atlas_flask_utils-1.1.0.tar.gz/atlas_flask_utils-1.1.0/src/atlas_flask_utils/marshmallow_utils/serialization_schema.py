from .schema_validation import BaseSchema


class SerializationSchema(BaseSchema):
    __data: dict

    def __init__(self, **kwargs):
        super().__init__()
        self.__data = {}
        for field in self.fields:
            self.__data[field] = kwargs.pop(field)

    def serialize(self) -> dict:
        return self.dump(self.__data)