from mongoengine import *
from .model_mixin import ModelMixin

class ServerSettings(DynamicDocument, ModelMixin):
    DB_COLUMNS = [
        'officer_mode',
        'server',
    ]

    officer_mode = BooleanField(default=False)
    server = IntField()
