from mongoengine import *
from utils import SERVER_COLLECTION
from .model_mixin import ModelMixin
from .member import Member

class Server(Document, ModelMixin):
    DB_COLUMNS = [
        'id',
        'members',
        'name',
        'avatar',
    ]

    id = IntField(primary_key=True)
    members = ListField(ReferenceField(Member))
    name = StringField()
    avatar = StringField()
    meta = {
        'collection' : SERVER_COLLECTION,
    }
