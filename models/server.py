from mongoengine import *
from datetime import datetime
from utils import MEMBER_COLLECTION
from .model_mixin import ModelMixin
from .member import Member

class Server(Document, ModelMixin):
    DB_COLUMNS = [
        'id',
        'members',
    ]

    id = IntField
    members = ListField(ReferenceField(Member))
    meta = {
        'collection' : MEMBER_COLLECTION,
    }
