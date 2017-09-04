import csv
from mongoengine import *
import sys

from configparser import ConfigParser  
from tabulate import tabulate
from datetime import datetime

import asyncio
import discord
from discord.ext import commands

from utils import *
from member import Member


#Main connection function offered by mongoengine defaults are localhost:27017
connect(db_name)

bot = commands.Bot(command_prefix='gsbot ', description=description)

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
    # Here we load our extensions listed above in [initial_extensions].
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
                print('loaded {}'.format(extension))
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

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
async def update_me(ctx, level: int, ap: int, dp: int):
    """Updates a users gear score Each user is linked to a gear score in the database
    and can only update their scores(excluding officers)."""
    date = datetime.now()

    try:
        author = ctx.message.author
        member = Member.objects(discord = author.id).first()
        member.level = level
        member.ap = ap
        member.dp = dp
        member.gear_score = ap + dp
        member.updated = date.strftime("%D")
        member.save()

        info = [["Success updating User"], ["Character", member.char_name], ["gear_score", ap+dp], ["Discord", author.id]]

        await bot.say(codify(tabulate(info)))
        
    except Error:
        print(Error)
        await bot.say("Error updating user")

@bot.command(pass_context=True)
async def update(ctx, level: int, ap: int, dp: int, user: discord.Member):
    """ **Officers Only** Updates a users gear score Each user is linked to a gear score in the database
    and can only update their scores(excluding officers)."""


    roles = [u.name for u in author.roles]
    if admin_user not in roles:
        await bot.say("Only officers may perform this action")
    else:
        date = datetime.now()

        try:
            author = ctx.message.author
            member = Member.objects(discord = author.id).first()
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
            info = [["Success Deleting User"], ["Character", member.char_name], ["Family", member.fam_name]]
            member.delete()
            await bot.say(codify(tabulate(info)))
        except Exception as e:
            print(e)
            await bot.say(codify("Error deleting user, Make sure the spelling is correct"))

@bot.command(pass_context=True)
async def delete_me(ctx):
    """Deletes your added character"""

    try:
        member = Member.objects(discord = ctx.message.author.id).first()
        info = [["Success Deleting User"], ["Character", member.char_name], ["Discord", ctx.message.author.id]]
        member.delete()
        await bot.say(codify(tabulate(info)))
    except Exception as e:
        print(e)
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

    author = ctx.message.author
    user = Member.objects(discord = author).first()
    date = datetime.now()
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
