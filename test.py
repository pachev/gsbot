# Main connection function offered by mongoengine defaults are localhost:27017
from cloudinary import config
from mongoengine import *

import models.character
from utils import *

connect('gsbot_test')

if HAS_CLOUD_STORAGE:
    config(
        cloud_name = CLOUD_NAME,
        api_key = CLOUDINARY_API,
        api_secret = CLOUDINARY_SECRET
    )


character = models.character.Character(ap = 220)
character.save()

print (character.ap)
