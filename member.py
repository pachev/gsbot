from mongoengine import *
from datetime import datetime
from configparser import ConfigParser  
from utils import collection


#This is the ODM that is provided by mongoengine. It's a cleaner way of
#adding and deleting data throughout the bot
class Member(Document):
    rank = StringField(max_lenght=50)
    fam_name = StringField(max_lenght=50)
    char_name = StringField(max_lenght=50)
    char_class = StringField(max_lenght=50)
    discord = IntField()
    server = StringField()
    level = IntField(max_lenght=4)
    ap = IntField(max_lenght=5)
    dp = IntField(max_lenght=5)
    gear_score = IntField(max_lenght=10)
    updated = DateTimeField(default=datetime.now)
    progress = IntField()
    gear_pic = URLField()
    server = IntField()
    meta = {'collection' : collection}
