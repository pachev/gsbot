import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime

from member import Member
from historical import Historical
from utils import *


class Update:
    """Update commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def update(self, ctx, level: int, ap: int, dp: int, level_percent: float, fam_name=''):
        """Updates a user's gear score. Each user is linked to a gear score in the database
        and can only update their scores. **Officers can add an additional family name at 
        the end of this command to update another user"""
        date = datetime.now()

        try:
            author = ctx.message.author
            if not fam_name:
                member = Member.objects(discord = author.id).first()
            else:
                member = Member.objects(fam_name = fam_name, server = ctx.message.server.id).first()
                roles = [u.name for u in author.roles]
                if ADMIN_USER not in roles:
                    await self.bot.say("Only officers may perform this action")
                    return

            # Adds historical data to database
            update = Historical.create({
                'type': "update",
                'char_class': member.char_class,
                'timestamp': date,
                'level': member.level + (round(member.progress, 2) * .01),
                'ap': member.ap,
                'dp': member.dp,
                'gear_score': member.gear_score
            })

            member.update({
                'char_name': new_char_name,
                'ap': ap, 
                'dp': dp,
                'level': level,
                'gear_score': ap + dp,
                'char_class': new_char_class,
                'updated': date,
                'hist_data': historical_data
            })

            row = get_row([member], False)
            data = tabulate(row,
                            HEADERS,
                            'simple',)

            await self.bot.say(codify(data))

        except Exception as e:
            print(e)
            await self.bot.say("Error updating user")


def setup(bot):
    bot.add_cog(Update(bot))
