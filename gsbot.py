from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser  


import discord
from discord.ext import commands
import random


#Connecting to the sqlite database that holds the user information
#Note: The database table has already been populated
engine = create_engine('sqlite:///gsbot.db', echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

config = ConfigParser()  
config.read('config.ini')  
token = config.get('auth', 'token') 

#this is where I declare the class for the ORM based on the original spreadsheet
class Member(Base):
    __tablename__ = 'score_sheet'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, nullable=False)
    fam_name = Column(String)
    char_name = Column(String)
    notes = Column(String)
    updated = Column(String)
    char_class = Column(String)
    rank = Column(String)
    level = Column(Integer)
    ap = Column(Integer)
    dp = Column(Integer)
    gear_score = Column(Integer)



description = '''
This the official Gear Score bot of the Legendary Guild Sazerac.
Made by drawven(drawven@gmail.com)
'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

@cool.command(name='drawven')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yep, he is cool.')

bot.run(token)
