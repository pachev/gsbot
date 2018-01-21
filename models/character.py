from mongoengine import *
from datetime import datetime
from configparser import ConfigParser  
from utils import CHARACTER_COLLECTION
from .model_mixin import ModelMixin
from .historical import Historical

class Character(Document, ModelMixin):
    DB_COLUMNS = [
        'rank',
        'fam_name',
        'char_name', 
        'char_class', 
        'server',
        'level', 
        'ap', 
        'dp', 
        'gear_score', 
        'updated', 
        'progress', 
        'gear_pic', 
        'primary',
        'member',
        'hist_data'
    ]

    rank = StringField(max_lenght=50)
    fam_name = StringField(max_lenght=50)
    char_name = StringField(max_lenght=50)
    char_class = StringField(max_lenght=50)
    level = IntField(max_lenght=4)
    ap = IntField(max_lenght=5)
    dp = IntField(max_lenght=5)
    gear_score = IntField(max_lenght=10)
    updated = DateTimeField(default=datetime.now)
    progress = FloatField(default=0.0)
    gear_pic = URLField(default="https://i.imgur.com/UFViCXj.jpg")
    server = IntField()
    primary = BooleanField()
    member = IntField()
    hist_data = ListField(ReferenceField(Historical))
    meta = {
        'collection' : CHARACTER_COLLECTION,
    }

    @queryset_manager
    def objects(doc_cls, queryset):
        # default order is gear score descending
        return queryset.order_by('-gear_score')

    @queryset_manager
    def primary_chars(doc_cls, queryset):
        # default order is gear score descending
        return queryset.filter(primary=True)
