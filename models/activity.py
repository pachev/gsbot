from mongoengine import *
from .model_mixin import ModelMixin
from datetime import datetime

class Activity(Document, ModelMixin):
    DB_COLUMNS = [
        'message',
        'timestamp',
        'user',
    ]

    message = StringField()
    timestamp = DateTimeField(default=datetime.now)
    user = StringField()
