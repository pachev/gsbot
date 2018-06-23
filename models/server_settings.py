from mongoengine import *
from .model_mixin import ModelMixin

class ServerSettings(DynamicDocument, ModelMixin):
    DB_COLUMNS = [
        'officer_mode',
        'officer_role',
        'server',
    ]

    officer_mode = BooleanField(default=False)
    officer_role = StringField(default="Officers")
    server = IntField()
