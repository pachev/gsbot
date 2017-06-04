from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser  
from tabulate import tabulate


import asyncio
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

members = session.query(Member).order_by(Member.gear_score.desc()).all()

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

@bot.event
async def on_message(message):
    if message.content.startswith('gsbot add'):
        await bot.send_message(message.channel,"Addin player")
        print(message.author)
    elif message.content.startswith('gsbot sleep'):
        await asyncio.sleep(5)
        await bot.send_message(message.channel, 'Done sleeping for 5')

    await bot.process_commands(message)

@bot.command()
async def list(num=10):
    """List all the members and their gear score with optional limit. 
    eg. ?list returns first 10 by default  and ?list 5 first 5 sorted by
    gear score"""

    data =tabulate([[u.fam_name,u.char_name, u.gear_score] for u in members[:num]], 
                   ['Family', 'Character', 'GearScore'],
                   'simple',
                   stralign='center')
    await bot.say(data)


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
