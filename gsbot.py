from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser  
from tabulate import tabulate
import numpy as np


import asyncio
import discord
from discord.ext import commands
import random


#Connecting to the sqlite database that holds the user information
#Note: The database table has already been populated
engine = create_engine('sqlite:///gsbot.db', echo=False)

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
    members = session.query(Member).order_by(Member.gear_score.desc()).all()
    if num > 45:
        nums = 45
    else:
        nums = num
    data =tabulate([[u.fam_name,u.char_name, u.gear_score] for u in members[:nums]], 
                   ['Family', 'Character', 'GearScore'],
                   'simple',
                   stralign='center')
    await bot.say(data)

@bot.command()
async def over(num=350):
    """List all the members over a certain gear score"""
    members = session.query(Member).order_by(Member.gear_score.desc()).all()
    data =tabulate([[u.fam_name,u.char_name, u.gear_score] for u in members[1:40] if u.gear_score > num], 
                   ['Family', 'Character', 'GearScore'],
                   'simple',
                   stralign='center')
    print(data)
    await bot.say(data)

@bot.command()
async def lookup(name=""):
    """Looks up a guild member by their family name for score"""


    member = session.query(Member).filter(Member.fam_name.ilike('%'+name+'%')).all()
    data =tabulate([[u.fam_name,u.char_name, u.gear_score] for u in member], 
                   ['Family', 'Character', 'GearScore'],
                   'simple',
                   stralign='center')
    print(data)
    await bot.say(data)

@bot.command()
async def average():
    """Gives the current guild score average"""

    members = session.query(Member).order_by(Member.gear_score.desc()).all()
    gear_scores = [u.gear_score for u in members[1:]]
    average = np.average(gear_scores)
    print(average)
    await bot.say(average)

@bot.command()
async def info():
    """List important gear score info. Lowest, highest, average, newest(not yet), oldest, total users, total officers, total members"""

    info = []
    members = session.query(Member).order_by(Member.gear_score.desc()).all()
    officers = session.query(Member).filter(Member.rank == 'officer').count()
    memb = session.query(Member).filter(Member.rank == 'member').count()
    gear_scores = [u.gear_score for u in members[ 1: ]]
    average = np.average(gear_scores)
    lowest = members[-1]
    highest = members[1]
    info.append(['Average', round(average,2)])
    info.append(['Lowest', lowest.gear_score, lowest.fam_name, lowest.char_name])
    info.append(['Higest', highest.gear_score, highest.fam_name, highest.char_name])
    info.append(['Total Officers', officers])
    info.append(['Total Members', memb])
    info.append(['Total', len(members)])

    await bot.say(tabulate(info))


bot.run(token)
