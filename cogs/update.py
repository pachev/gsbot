import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime

from member import Member
from utils import *


class Update:
    """Update commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def update_me(self, ctx, level: int, ap: int, dp: int):
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
            member.updated = date
            member.save()

            info = [["Success updating User"], ["Character", member.char_name], ["gear_score", ap+dp], ["Discord", author.id]]

            await self.bot.say(codify(tabulate(info)))
            
        except Error:
            print(Error)
            await self.bot.say("Error updating user")

    @commands.command(pass_context=True)
    async def update(self, ctx, level: int, ap: int, dp: int, fam_name):
        """ **Officers Only** Updates a users gear score Each user is linked to a gear score in the database
        and can only update their scores(excluding officers)."""


        roles = [u.name for u in author.roles]
        if admin_user not in roles:
            await self.bot.say("Only officers may perform this action")
        else:
            date = datetime.now()

            try:
                author = ctx.message.author
                member = Member.objects(fam_name = fam_name).first()
                member.level = level
                member.ap = ap
                member.dp = dp
                member.gear_score = ap + dp
                member.updated = date

                member.save()
                info = [["Success updating User"], ["Character", member.char_name], ["gear_score", ap+dp], ["Discord", ctx.message.author.id]]

                await self.bot.say(codify(tabulate(info)))
                
            except Error:
                print(Error)
                await self.bot.say("Error updating user")

def setup(bot):
    bot.add_cog(Update(bot))
