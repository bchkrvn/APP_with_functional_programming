import marshmallow_dataclass

from data_classes import UserRequest

user_request_schema = marshmallow_dataclass.class_schema(UserRequest)
