import pytest
from unittest import mock
from cloudinary import config
from mongoengine import *


from models.character import Character
from models.member import Member
from models.server import Server

from cogs.listings import Listing

from utils import *

connect('gsbot_test')

if HAS_CLOUD_STORAGE:
    config(
        cloud_name = CLOUD_NAME,
        api_key = CLOUDINARY_API,
        api_secret = CLOUDINARY_SECRET
    )

## Test Characters Creation
char1 = Character.create({
    "rank" : "Member",
    "fam_name" : "Member1",
    "char_name" : "Char1",
    "char_class" : "wizard",
    "level" : 60,
    "ap" : 197,
    "aap" : 197,
    "dp" : 238,
    "gear_score" : 435,
    "progress" : 0.0,
    "gear_pic" : "https://i.imgur.com/UFViCXj.jpg",
    "server" : 1,
    "primary" : False,
    "member" : 1,
})

char2 = Character.create({
    "rank" : "Member",
    "fam_name" : "Member1",
    "char_name" : "Char2",
    "char_class" : "Musa",
    "level" : 60,
    "ap" : 197,
    "aap" : 197,
    "dp" : 238,
    "gear_score" : 435,
    "progress" : 0.0,
    "gear_pic" : "https://i.imgur.com/UFViCXj.jpg",
    "server" : 1,
    "primary" : True,
    "member" : 2,
})
char3 = Character.create({
    "rank" : "Member",
    "fam_name" : "Member2",
    "char_name" : "Char3",
    "char_class" : "Maehwa",
    "level" : 60,
    "ap" : 197,
    "aap" : 197,
    "dp" : 238,
    "gear_score" : 435,
    "progress" : 0.0,
    "gear_pic" : "https://i.imgur.com/UFViCXj.jpg",
    "server" : 2,
    "primary" : True,
    "member" : 2,
})

## Test Members Creation

member1 = Member.create({
    "discord" : 1,
    "servers" : [1],
    "name" : "Test1",
    "avatar" : "Some_Url1"

})
member1.characters.append(char1)
member1.characters.append(char2)

member2 = Member.create({
    "discord" : 2,
    "servers" : [2],
    "name" : "Test2",
    "avatar" : "Some_Url2"

})
member2.characters.append(char3)

## Dummy Server Creation

server1 = Server.create({
    "id": 1,
    "name": "test_server1",
    "avatar" : "Some_Url1"
})
server1.members.append(member1)

server2 = Server.create({
    "id": 2,
    "name": "test_server2",
    "avatar" : "Some_Url2"
})
server2.members.append(member2)

def test_list():
    pass

if __name__ == '__main__':
    test_list()
