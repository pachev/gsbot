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
        'aap',
        'dp',
        'gear_score',
        'renown_score',
        'fame',
        'updated',
        'progress', 
        'gear_pic', 
        'primary',
        'member',
        'hist_data'
    ]

    rank = StringField(max_length=50)
    fam_name = StringField(max_length=50)
    char_name = StringField(max_length=50)
    char_class = StringField(max_length=50)
    level = IntField(max_length=4)
    aap = IntField(max_length=5)
    ap= IntField(max_length=5)
    dp = IntField(max_length=5)
    gear_score = IntField(max_length=10)
    renown_score = IntField(max_length=10)
    fame = IntField(min_value=0, max_value=5, default=0)
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
        return queryset.filter(primary=True).order_by('-gear_score')
