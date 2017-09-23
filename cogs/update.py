import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime

from models import Member, Historical
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
                member = Member.objects(fam_name = fam_name).first()
                roles = [u.name for u in author.roles]
                if admin_user not in roles:
                    await self.bot.say("Only officers may perform this action")

            # Adds historical data to database
            update = Historical(
                type = "update",
                char_class = member.char_class,
                timestamp = date,
                level = member.level + (round(member.progress, 2) * .01),
                ap = member.ap,
                dp = member.dp,
                gear_score = member.gear_score
            )
            update.save()

            member.level = level
            member.ap = ap
            member.dp = dp
            member.gear_score = ap + dp
            member.progress = level_percent
            member.updated = date
            member.hist_data.append(update)
            member.save()

            info = [["Success updating User"], ["Character", member.char_name], ["gear_score", ap+dp], ["Discord", author.id]]

            await self.bot.say(codify(tabulate(info)))
            
        except Exception as e:
            print(e)
            await self.bot.say("Error updating user")


def setup(bot):
    bot.add_cog(Update(bot))
