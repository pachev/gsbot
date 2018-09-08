import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime

from cloudinary.uploader import upload

from models.character import Character
from models.historical import Historical
from utils import *
import math

class Update:
    """Update commands."""

    def __init__(self, bot):
        self.bot = bot

    async def __get_member(self, author, user, server_id):
        author_roles = [u.name for u in author.roles]
        user_roles = [u.name for u in user.roles] if user else []
        if not user:
            character = Character.primary_chars(member = author.id).first()
            rank = 'Officer' if ADMIN_USER in author_roles else 'Member'
        else:
            character = Character.primary_chars(member = user.id, server = server_id).first()
            rank = 'Officer' if ADMIN_USER in user_roles else 'Member'
            if ADMIN_USER not in author_roles:
                await self.bot.say("Only officers may perform this action")
                return
        
        return (rank, character)

    def __create_historical(self, character, date: datetime):
        update = Historical.create({
            'type': "update",
            'char_class':character.char_class.upper(),
            'timestamp': date,
            'level': float(str(character.level) + '.' + str(round(character.progress))) ,
            'ap': character.ap,
            'aap': character.aap,
            'dp': character.dp,
            'gear_score': character.gear_score,
            'renown_score': character.renown_score
        })
        return update


    async def update_attribute(self, ctx, attribute, user: discord.User = None):
        date = datetime.now()
        try:
            author = ctx.message.author
            rank, character = await self.__get_member(author, user, ctx.message.server.id)
            if character is None:
                await self.bot.say(codify('Could not find character to update, Make sure they are in the system.'))
                return

            fame = character.fame
            if attribute['name'] == 'aap':
                character.update_attributes({
                    attribute['name']: attribute['value'],
                    'gear_score':  max(character.ap, attribute['value']) + character.dp,
                    'renown_score': math.trunc((character.ap+attribute['value'])/2 + character.dp) + fame,
                    'updated': date,
                    'rank': rank,
                })

            elif attribute['name'] == 'ap':
                character.update_attributes({
                    attribute['name']: attribute['value'],
                    'gear_score': max(attribute['value'], character.aap) + character.dp,
                    'renown_score': math.trunc((attribute['value']+character.aap)/2 + character.dp) + fame,
                    'updated': date,
                    'rank': rank,
                })

            elif attribute['name']  == 'dp':
                character.update_attributes({
                    attribute['name']: attribute['value'],
                    'gear_score':  attribute['value'] + max(character.aap, character.ap),
                    'renown_score': math.trunc((character.ap+character.aap)/2 + attribute['value']) + fame,
                    'updated': date,
                    'rank': rank,
                })
            elif attribute['name']  == 'fame':
                character.update_attributes({
                    attribute['name']: attribute['value'],
                    'renown_score': math.trunc((character.ap+character.aap)/2 + character.dp) + attribute['value'],
                    'updated': date,
                    'rank': rank,
                })
            else:
                character.update_attributes({
                    attribute['name']: attribute['value'],
                    'updated': date,
                    'rank': rank,
                })

            row = get_row([character], False)
            data = tabulate(row, HEADERS, 'simple')
            logActivity('{} has updated {} on {}'.format(character.fam_name, attribute['name'], character.char_name), author.name)
            await self.bot.say(codify('Updating {} for {} was a great success :D\n\n'.format(attribute['name'], character.char_name) + data))

        except Exception as e:
            print_error(e)
            await self.bot.say(codify("Error updating character"))

    @commands.group(pass_context=True)
    async def update(self, ctx):
        """Group of update commands"""

        # Checks if no sub-commands are invoked
        if ctx.invoked_subcommand is None:
            await self.bot.say(codify("Update main character information by one category or all. use gsbot help update "
                                      "for more info. ex. gsbot update ap 230 or gsbot update all 61 200 230 250 4.5"))

    @update.command(pass_context=True)
    async def all(self, ctx, level: int, ap: int, aap: int, dp: int, level_percent: float, user: discord.User = None):
        """Updates user's main character's information. **Officers can tag another user to update for them """
        date = datetime.now()

        try:
            author = ctx.message.author
            rank, character = await self.__get_member(author, user, ctx.message.server.id)
            if character is None:
                await self.bot.say(codify('Could not find character to update, Make sure they are in the system.'))
                return

            # Adds historical data to database
            update = self.__create_historical(character, date)
            historical_data = character.hist_data
            historical_data.append(update)

            character.update_attributes({
                'ap': ap,
                'aap': aap,
                'dp': dp,
                'level': level,
                'gear_score': max(aap, ap) + dp,
                'renown_score': math.trunc((ap+aap)/2 + dp),
                'progress': level_percent,
                'updated': date,
                'hist_data': historical_data
            })

            row = get_row([character], False)
            data = tabulate(row, HEADERS, 'simple')
            logActivity('{} has updated a character'.format(character.fam_name), author.name)
            await self.bot.say(codify('Updating {} was a great success :D\n\n'.format(character.fam_name) + data))

        except Exception as e:
            print_error(e)
            await self.bot.say("Error updating user")

    @update.command(pass_context=True)
    async def ap(self, ctx, ap: int, user: discord.User = None):
        """Updates user's main character's ap. **Officers can tag another user to update for them """
        await self.update_attribute(ctx, {'name': 'ap', 'value': ap}, user)

    @update.command(pass_context=True)
    async def aap(self, ctx, aap: int, user: discord.User = None):
        """Updates user's main character's aap. **Officers can tag another user to update for them """
        await self.update_attribute(ctx, {'name': 'aap', 'value': aap}, user)

    @update.command(pass_context=True)
    async def dp(self, ctx, dp: int, user: discord.User = None):
        """Updates user's main character's dp. **Officers can tag another user to update for them """
        await self.update_attribute(ctx, {'name': 'dp', 'value': dp}, user)

    @update.command(pass_context=True)
    async def lvl(self, ctx, level: int, user: discord.User = None):
        """Updates user's main character's level. **Officers can tag another user to update for them """
        await self.update_attribute(ctx, {'name': 'level', 'value': level}, user)

    @update.command(pass_context=True)
    async def progress(self, ctx, percent: float, user: discord.User = None):
        """Updates user's main character's level progress. **Officers can tag another user to update for them """
        await self.update_attribute(ctx, {'name': 'progress', 'value': percent}, user)

    @update.command(pass_context=True)
    async def fame(self, ctx, fame: int, user: discord.User = None):
        """Updates user's main character's fame. **Officers can tag another user to update for them """
        await self.update_attribute(ctx, {'name': 'fame', 'value': fame}, user)

    @update.command(pass_context=True)
    async def pic(self, ctx, url: str = None):
        """Updates user's main character's gear pic either attach a pic or type url"""
        attachments = ctx.message.attachments
        # TODO: Add fallback if cloudinary account is not enabled in configuration
        try:
            if url:
                response = upload(url, tags=PIC_TAG)
            else:
                if not attachments:
                    await self.bot.say('You must either attach a picture or provide a url')
                    return
                response = upload(attachments[0]['url'], tags=PIC_TAG)

            await self.update_attribute(ctx, {'name': 'gear_pic', 'value': response['url']})
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(Update(bot))
