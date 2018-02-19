from mongoengine import *
from datetime import datetime
from configparser import ConfigParser  
from utils import HIST_COLLECTION
from .model_mixin import ModelMixin

class Historical(Document, ModelMixin):
    DB_COLUMNS = [
        'type',
        'char_class',
        'timestamp',
        'level',
        'ap',
        'aap',
        'dp',
        'gear_score'
    ]

    type = StringField(max_lenght=50)
    char_class = StringField(max_lenght=50)
    timestamp = DateTimeField(default=datetime.now)
    level = FloatField()
    aap = IntField(max_lenght=5)
    ap = IntField(max_lenght=5)
    dp = IntField(max_lenght=5)
    gear_score = IntField(max_lenght=10)
    meta = {
        'collection' : HIST_COLLECTION,
    }