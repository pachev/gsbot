from pymongo import MongoClient
from mongoengine import *
import csv

from configparser import ConfigParser  
from tabulate import tabulate
import numpy as np
from datetime import datetime



import asyncio
import discord
from discord.ext import commands
import random


db_name = 'gsbot'


config = ConfigParser()  
config.read('config.ini')  
token = config.get('auth', 'token2') 


collection ='sazerac'
admin_user ='Admin'


connect(db_name)


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
    progress = IntField()
    updated = DateTimeField(default=datetime.now)
    gear_pic = URLField()
    server = IntField()

    meta = {'collection' : collection}

    @queryset_manager
    def objects(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.order_by('-gear_score')


description = '''
This the official Gear Score bot of the Legendary Guild Sazerac.
Made by drawven(drawven@gmail.com)
'''

bot = commands.Bot(command_prefix='gsbot ', description=description)

headers = ['Rank', 'Fam', 'Char', 'Class', 'Lvl', 'AP', 'DP','GS', 'Updated']

#utility method to wrap string in codeblocks
def codify(s):
    return '```\n' + s + '\n```'

def get_row(members, filter, num=-1):
    if filter:
        return [[u.rank, u.fam_name, u.char_name, u.char_class, u.level, u.ap, u.dp, u.gear_score, u.updated] for u in members[:num]] 

    return [[u.rank, u.fam_name, u.char_name, u.char_class, u.level, u.ap, u.dp, u.gear_score, u.updated] for u in members] 

def paginate(data):
    paginator = commands.Paginator()
    for i in data.splitlines():
        paginator.add_line(i)
    return paginator.pages

#Here check for server configs and add a new collection for each server name
def check_server_config():
    pass


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    check_server_config()

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, codify("Does not compute: try gsbot help or gsbot help <specific command>"))
    elif isinstance(error, commands.CommandNotFound):
        await bot.send_message(ctx.message.channel, codify("I don't know that command: try gsbot help"))

@bot.command(pass_context=True)
async def add_me(ctx, fam_name, char_name, level: int, ap : int, dp: int, char_class):
    """Adds yourself as a member to the database. This member is linked with your discord id
    and can only be updated by either that member or an officer.
    Example regular member: gsbot add drawven drawven 56 83 83 Musa 
    Note: Total gear score and rank is auto calculated."""

    author = ctx.message.author

    roles = [u.name for u in author.roles]

    if admin_user in roles:
        rank = 'Officer'
    else:
        rank = 'Member'

    count = len(Member.objects(discord = author.id))
    if count >= 1:
        await bot.say("Cannot add more than one character to this discord id. Try rerolling with gsbot reroll")
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
                            discord = ctx.message.author.id)
            member.save()
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
    """**Officers only** Adds a member to the database. 
    example : gsbot add drawven drawven 56 83 83 Musa @drawven#9405
    Note: Total gear score and rank is auto calculated"""
    date = datetime.now()

    author = ctx.message.author
    count = len(Member.objects(discord = author.id))

    roles = [u.name for u in author.roles]
    if admin_user not in roles:
        await bot.say("Only officers may perform this action")
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
                                discord = user.id)
                member.save()
                info = [["Success Adding User"], ["Character", member.char_name], ["Gear Score", ap+dp], ["Discord", user.id]]

                await bot.say(codify(tabulate(info)))
                
            except:
                await bot.say("Something went horribly wrong")


@bot.command(pass_context=True)
async def update_me(ctx, level: int, ap: int, dp: int):
    """Updates a users gear score Each user is linked to a gear score in the database
    and can only update their scores(excluding officers)."""
    date = datetime.now()

    try:
        member = Member.objects(discord = ctx.author.id).first()
        member.level = level
        member.ap = ap
        member.dp = dp
        member.gear_score = ap + dp
        member.updated = date.strftime("%D")
        member.save()

        info = [["Success updating User"], ["Character", member.char_name], ["gear_score", ap+dp], ["Discord", ctx.message.author.id]]

        await bot.say(codify(tabulate(info)))
        
    except Error:
        print(Error)
        await bot.say("Error updating user")

@bot.command(pass_context=True)
async def update(ctx, level: int, ap: int, dp: int, user: discord.Member):
    """ **Officers Only** Updates a users gear score Each user is linked to a gear score in the database
    and can only update their scores(excluding officers)."""

    author = ctx.message.author

    roles = [u.name for u in author.roles]
    if admin_user not in roles:
        await bot.say("Only officers may perform this action")
    else:
        date = datetime.now()

        try:
            member = Member.objects(discord = ctx.author.id).first()
            member.level = level
            member.ap = ap
            member.dp = dp
            member.gear_score = ap + dp
            member.updated = date.strftime("%D")

            member.save()
            info = [["Success updating User"], ["Character", member.char_name], ["gear_score", ap+dp], ["Discord", ctx.message.author.id]]

            await bot.say(codify(tabulate(info)))
            
        except Error:
            print(Error)
            await bot.say("Error updating user")

@bot.command(pass_context=True)
async def delete(ctx, fam_name):
    """**Officers only** Deletes an added user by family name"""

    author = ctx.message.author
    roles = [u.name for u in author.roles]
    if admin_user not in roles:
        await bot.say("Only officers may perform this action")
    else:
        try:
            member = Member.objects(fam_name = fam_name).first()
            member.delete()

            info = [["Success Deleting User"], ["Character", member.char_name], ["Family", member.fam_name]]

            await bot.say(codify(tabulate(info)))
            
        except Exception as e:
            print(e)
            await bot.say(codify("Error deleting user, Make sure the spelling is correct"))

@bot.command(pass_context=True)
async def delete_me(ctx):
    """Deletes your added character"""

    try:
        member = Member.objects(discord = ctx.author.id).first()
        member.delete()
        info = [["Success Deleting User"], ["Character", member.char_name], ["Discord", ctx.message.author.id]]

        await bot.say(codify(tabulate(info)))
        
    except:
        await bot.say("Error deleting user")


@bot.command()
async def list(num=100):
    """List all the members and their gear score with optional limit. 
    Example. gsbot list returns first 100 by default  and gsbot list 5 first 5 sorted by
    gear score"""
    try:
        members = Member.objects()
        rows = get_row(members, True, num)

        data = tabulate(rows,
                        headers,
                       'simple',)
        
        for page in paginate(data):
            await bot.say(page)
    except:
        await bot.say("Something went horribly wrong")


@bot.command()
async def over(num=400):
    """List all the members over a certain gear score"""
    try:
        members = Member.objects(gear_score__gte = num)
        rows = get_row(members,False)

        data = tabulate(rows,
                        headers,
                       'simple',)

        for page in paginate(data):
            await bot.say(page)

    except Exception as e:
        print(e)
        await bot.say("Something went horribly wrong")


@bot.command()
async def under(num=400):
    """List all the members under a certain gear score"""
    try:
        members = Member.objects(gear_score__lte = num)
        rows = get_row(members, False)
        data = tabulate(rows,
                        headers,
                       'simple',)

        for page in paginate(data):
            await bot.say(page)
    except:
        await bot.say("Something went horribly wrong")


@bot.command()
async def lookup(name=""):
    """Looks up a guild member by score"""
    try:
        members = Member.objects(Q(fam_name__icontains = name) | Q(char_name__icontains = name))
        rows = get_row(members, False)

        data = tabulate(rows,
                        headers,
                       'simple',)
        for page in paginate(data):
            await bot.say(page)

    except Exception as e:
        print(e)
        await bot.say("Something went horribly wrong")

@bot.command()
async def info():
    """List important gear score info. Lowest, highest, average, newest(not yet), oldest, total users, total officers, total members"""

    try:
        info = []
        members = Member.objects()
        officers = Member.objects(rank=admin_user)
        average = Member.objects.average('gear_score')
        lowest = Member.objects.order_by('+gear_score').first()
        highest = members[0]
        info.append(['Average', round(average,2)])
        info.append(['Lowest', lowest.gear_score, lowest.fam_name, lowest.char_name])
        info.append(['Highest', highest.gear_score, highest.fam_name, highest.char_name])
        info.append(['Total Officers', len(officers)])
        info.append(['Total Members', len(members) - len(officers)])
        info.append(['Guild Total', len(members)])
        data = tabulate(info)

        await bot.say(codify(data))
    except Exception as e:
        print(e)
        await bot.say("Could not retrieve info")

@bot.command()
async def export():
    """Exports current guild data"""

    members = Member.objects()
    rows = get_row(members, False)
    rows.insert(0, headers)
    try:
        with open('./members.csv', 'w') as myfile:
            wr = csv.writer(myfile)
            wr.writerows(rows)
        await bot.upload('./members.csv')
    except Exception as e:
        print(e)
        await bot.say("Something went horribly wrong")

@bot.command(pass_context=True)
async def reroll(ctx, new_char_name, level: int, ap : int, dp: int, new_char_class):
    """Just for scatter: Allows you to reroll """

    user = Member.objects(discord = ctx.author.id).first()

    date = datetime.now()

    author = ctx.message.author
    if not user:
        await bot.say("Can't reroll if you're not in the database :(, try adding yoursell first")


    else:
        try:
            user.char_name = new_char_name
            user.ap = ap
            user.dp = dp
            user.gear_score = ap + dp
            user.char_class = new_char_class
            user.save()

            info = [["Success Re-Rolling"], 
                    ["New Char", new_char_name], 
                    ["New GS", ap+dp], 
                    ["New Class", new_char_class]]

            await bot.say(codify(tabulate(info)))
            
        except Exception as e:
            print(e)
            await bot.say("Something went horribly wrong")

bot.run(token)
