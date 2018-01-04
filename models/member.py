from mongoengine import *
from datetime import datetime
from utils import MEMBER_COLLECTION
from .model_mixin import ModelMixin
from .character import Character

class Member(Document, ModelMixin):
    DB_COLUMNS = [
        'characters',
        'discord',
        'servers',
    ]

    discord = IntField()
    characters = ListField(ReferenceField(Character))
    servers = ListField(IntField())
    meta = {
        'collection' : MEMBER_COLLECTION,
    }
