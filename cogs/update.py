import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime

from models.character import Character
from models.historical import Historical
from utils import *

class Update:
    """Update commands."""

    def __init__(self, bot):
        self.bot = bot

    async def __get_member(self, author, fam_name, server_id):
        if not fam_name:
            character = Character.primary_chars(member = author.id).first()
        else:
            character = Character.primary_chars(fam_name = fam_name, server = server_id).first()
            roles = [u.name for u in author.roles]
            if ADMIN_USER not in roles:
                await self.bot.say("Only officers may perform this action")
                return
        
        return character

    @commands.command(pass_context=True)
    async def update(self, ctx, level: int, ap: int, dp: int, level_percent: float, fam_name=''):
        """Updates user's main character's gear score. **Officers can add an additional family name at
        the end of this command to update another user"""
        date = datetime.now()

        try:
            author = ctx.message.author
            
            character = await self.__get_member(author, fam_name, ctx.message.server.id)
            if character is None:
                return

            # Adds historical data to database
            update = Historical.create({
                'type': "update",
                'char_class':character.char_class.upper(),
                'timestamp': date,
                'level': float(str(character.level) + '.' + str(round(character.progress))) ,
                'ap': character.ap,
                'dp': character.dp,
                'gear_score': character.gear_score
            })

            historical_data = character.hist_data
            historical_data.append(update)

            character.update_attributes({
                'ap': ap, 
                'dp': dp,
                'level': level,
                'gear_score': ap + dp,
                'progress': level_percent,
                'updated': date,
                'hist_data': historical_data
            })

            row = get_row([character], False)
            data = tabulate(row, HEADERS, 'simple')

            await self.bot.say(codify(data))

        except Exception as e:
            print(e)
            await self.bot.say("Error updating user")


def setup(bot):
    bot.add_cog(Update(bot))
