from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import csv

from configparser import ConfigParser  
from tabulate import tabulate
import numpy as np
from datetime import datetime



import asyncio
import discord
from discord.ext import commands
import random


#Connecting to the sqlite database that holds the user information
#Note: The database table has already been populated
engine = create_engine('sqlite:///gsbot.db', echo=False)
Base = declarative_base()

table_name='gs_bot'
admin_user='Officers'


Session = sessionmaker(bind=engine)
session = Session()

config = ConfigParser()  
config.read('config.ini')  
token = config.get('auth', 'token2') 



#this is where I declare the class for the ORM based on the original spreadsheet
class Member(Base):
    __tablename__ = table_name
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, nullable=False)
    fam_name = Column(String)
    char_name = Column(String)
    discord = Column(String)
    notes = Column(String)
    updated = Column(String)
    char_class = Column(String)
    rank = Column(String)
    level = Column(Integer)
    ap = Column(Integer)
    dp = Column(Integer)
    gear_score = Column(Integer)

if not engine.dialect.has_table(engine, table_name):  # If table don't exist, Create.
    Base.metadata.create_all(engine)


description = '''
This the official Gear Score bot of the Legendary Guild Sazerac.
Made by drawven(drawven@gmail.com)
'''

bot = commands.Bot(command_prefix='gsbot ', description=description)

headers = ['Fam', 'Char', 'Class', 'Lvl', 'AP', 'DP','GS', 'Updated']

#utility method to wrap string in codeblocks
def codify(s):
    return '```\n' + s + '\n```'


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def add_me(ctx, fam_name, char_name, level: int, ap : int, dp: int, char_class):
    """Adds yourself as a member to the database. This member is linked with your discord id
    and can only be updated by either that member or an officer.
    example regular member: gsbot add drawven drawven 56 83 83 Musa 
    Note: Total gear score and rank is auto calculated."""
    date = datetime.now()

    author = ctx.message.author
    count = session.query(Member).filter(Member.discord == ctx.message.author.id).count()

    roles = [u.name for u in author.roles]

    if admin_user in roles:
        rank = 'Officer'
    else:
        rank = 'Member'

    if count >= 1:
        await bot.say("Cannot add more than one character to this discord id")
    else:
        try:
            member = Member(fam_name=fam_name, 
                            char_name=char_name, 
                            level= level,
                            ap = ap,
                            dp = dp,
                            char_class= char_class,
                            rank = rank,
                            gear_score = ap + dp,
                            discord = ctx.message.author.id,
                            notes = "",
                            updated =  date.strftime("%D"))
            session.add(member)
            session.commit()
            info = [["Success Adding User"], ["Character", char_name], ["gear_score", ap+dp], ["Discord", ctx.message.author.id]]

            await bot.say(codify(tabulate(info)))
            
        except:
            await bot.say("Something went horribly wrong")

@bot.command(pass_context=True)
async def add(ctx, 
              fam_name,
              char_name,
              level: int,
              ap : int,
              dp: int,
              char_class,
              user: discord.Member,):
    """Officers only Adds a member to the database. 
    example : gsbot add drawven drawven 56 83 83 Musa @drawven#9405
    Note: Total gear score and rank is auto calculated"""
    date = datetime.now()

    author = ctx.message.author
    count = session.query(Member).filter(Member.discord == user.id).count()

    roles = [u.name for u in author.roles]
    if admin_user not in roles:
        await bot.say("Only officers may perorm this action")
    else:
        if count >= 1:
            await bot.say("Cannot add more than one character to this discord id")
        else:
            try:

                user_roles = [u.name for u in user.roles]
                if admin_user in user_roles:
                    rank = 'Officer'
                else:
                    rank = 'Member'
                member = Member(fam_name=fam_name, 
                                char_name=char_name, 
                                level= level,
                                ap = ap,
                                dp = dp,
                                char_class= char_class,
                                rank = rank,
                                gear_score = ap + dp,
                                discord = user.id,
                                notes = "",
                                updated =  date.strftime("%D"))
                session.add(member)
                session.commit()
                info = [["Success Adding User"], ["Character", char_name], ["gear_score", ap+dp], ["Discord", user.id]]

                await bot.say(codify(tabulate(info)))
                
            except:
                await bot.say("Something went horribly wrong")


@bot.command(pass_context=True)
async def update_me(ctx, level: int, ap: int, dp: int):
    """Updates a users gear score Each user is linked to a gear score in the database
    and can only update their scores(excluding officers)."""
    date = datetime.now()

    try:
        member = session.query(Member).filter(Member.discord == ctx.message.author.id).one()
        member.level = level
        member.ap = ap
        member.dp = dp
        member.gear_score = ap + dp
        member.updated = date.strftime("%D")

        session.add(member)
        info = [["Success updating User"], ["Character", member.char_name], ["gear_score", ap+dp], ["Discord", ctx.message.author.id]]

        session.commit()

        await bot.say(codify(tabulate(info)))
        
    except Error:
        print(Error)
        await bot.say("Error updating user")

@bot.command(pass_context=True)
async def update(ctx, level: int, ap: int, dp: int, user: discord.Member):
    """ Officers Only Updates a users gear score Each user is linked to a gear score in the database
    and can only update their scores(excluding officers)."""

    author = ctx.message.author

    roles = [u.name for u in author.roles]
    print([i.name for i in author.roles])
    if admin_user not in roles:
        await bot.say("Only officers may perorm this action")
    else:
        date = datetime.now()

        try:
            member = session.query(Member).filter(Member.discord == user.id).one()
            member.level = level
            member.ap = ap
            member.dp = dp
            member.gear_score = ap + dp
            member.updated = date.strftime("%D")

            session.add(member)
            info = [["Success updating User"], ["Character", member.char_name], ["gear_score", ap+dp], ["Discord", ctx.message.author.id]]

            session.commit()

            await bot.say(codify(tabulate(info)))
            
        except Error:
            print(Error)
            await bot.say("Error updating user")

@bot.command(pass_context=True)
async def delete(ctx, user: discord.Member):
    """Officers only Deletes an added character"""

    author = ctx.message.author
    count = session.query(Member).filter(Member.discord == user.id).count()

    roles = [u.name for u in author.roles]
    print([i.name for i in author.roles])
    if admin_user not in roles:
        await bot.say("Only officers may perorm this action")
    else:
        try:
            member = session.query(Member).filter(Member.discord == user.id).one()
            session.delete(member)
            info = [["Success Deleting User"], ["Character", member.char_name], ["Discord", user.id]]
            session.commit()

            await bot.say(codify(tabulate(info)))
            
        except:
            await bot.say("Error deleting user")

@bot.command(pass_context=True)
async def delete_me(ctx):
    """Deletes your added character"""

    try:
        member = session.query(Member).filter(Member.discord == ctx.message.author.id).one()
        session.delete(member)
        info = [["Success Deleting User"], ["Character", member.char_name], ["Discord", ctx.message.author.id]]
        session.commit()

        await bot.say(codify(tabulate(info)))
        
    except:
        await bot.say("Error deleting user")


@bot.command()
async def list(num=10):
    """List all the members and their gear score with optional limit. 
    eg. ?list returns first 10 by default  and ?list 5 first 5 sorted by
    gear score"""
    try:
        members = session.query(Member).order_by(Member.gear_score.desc()).all()
        rows = [[u.fam_name, u.char_name, u.char_class, u.level, u.ap, u.dp, u.gear_score, u.updated] for u in members[:num]] 

        data = tabulate(rows,
                        headers,
                       'simple',)
        await bot.say(codify(data))
    except:
        await bot.say("Something went horribly wrong")


@bot.command()
async def over(num=350):
    """List all the members over a certain gear score"""
    try:
        members = session.query(Member).order_by(Member.gear_score.desc()).all()
        rows =[[u.fam_name, u.char_name, u.char_class, u.level, u.ap, u.dp, u.gear_score, u.updated] for u in members if u.gear_score >= num]

        data = tabulate(rows,
                        headers,
                       'simple',)
        await bot.say(codify(data))
    except:
        await bot.say("Something went horribly wrong")


@bot.command()
async def under(num=350):
    """List all the members under a certain gear score"""
    try:
        members = session.query(Member).order_by(Member.gear_score.desc()).all()
        rows =[[u.fam_name, u.char_name,  u.char_class, u.level, u.ap, u.dp, u.gear_score, u.updated] for u in members if u.gear_score <= num]
        data = tabulate(rows,
                        headers,
                       'simple',)
        await bot.say(codify(data))
    except:
        await bot.say("Something went horribly wrong")


@bot.command()
async def lookup(name=""):
    """Looks up a guild member by score"""
    try:
        members = session.query(Member).filter(or_(Member.fam_name.ilike('%'+name+'%'),
                                                  Member.char_name.ilike('%'+name+'%'))).all()
        rows =[[u.fam_name, u.char_name, u.char_class, u.level, u.ap, u.dp, u.gear_score, u.updated] for u in members]

        data = tabulate(rows,
                        headers,
                       'simple',)

        await bot.say(codify(data))
    except:
        await bot.say("Something went horribly wrong")


@bot.command()
async def average():
    """Gives the current guild score average"""

    members = session.query(Member).order_by(Member.gear_score.desc()).all()
    gear_scores = [u.gear_score for u in members]
    average = np.average(gear_scores)
    print(average)
    await bot.say(average)

@bot.command()
async def info():
    """List important gear score info. Lowest, highest, average, newest(not yet), oldest, total users, total officers, total members"""

    try:
        info = []
        members = session.query(Member).order_by(Member.gear_score.desc()).all()
        officers = session.query(Member).filter(Member.rank == 'Officer').count()
        gear_scores = [u.gear_score for u in members]
        average = np.average(gear_scores)
        lowest = members[-1]
        highest = members[0]
        info.append(['Average', round(average,2)])
        info.append(['Lowest', lowest.gear_score, lowest.fam_name, lowest.char_name])
        info.append(['Higest', highest.gear_score, highest.fam_name, highest.char_name])
        info.append(['Total Officers', officers])
        info.append(['Total Members', len(members) - officers])
        info.append(['Total', len(members)])
        data = tabulate(info)

        await bot.say(codify(data))
    except:
        await bot.say("Could not retrieve info")

@bot.command()
async def export():
    """Exports current guild data"""

    out = open('./members.csv', 'w')
    out_csv = csv.writer(out)
    members = session.query(Member).order_by(Member.gear_score.desc()).all()
    [out_csv.writerow([getattr(curr, column.name) for column in Member.__mapper__.columns]) for curr in members]
    out.close()
    await bot.upload('./members.csv')
        

bot.run(token)
