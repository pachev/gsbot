import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime

from models import Member
from utils import *


class Extras:
    """Extra commands for fun"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def attach_pic(self, ctx, url):
        """ Command to attach a picture to your character.
            When someone looks you up the attched picture
            is displayed"""

        try:
            author = ctx.message.author
            member = Member.objects(discord = author.id).first()
            member.gear_pic = url
            member.save()
            await self.bot.say(codify("Picture added successfully"))
        except Exception as e:
            print(e)
            await self.bot.say("Picture could not be added")


def setup(bot):
    bot.add_cog(Extras(bot))
