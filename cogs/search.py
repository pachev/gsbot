import discord
from discord.ext import commands
from tabulate import tabulate
from mongoengine import *

from member import Member
from utils import *


class Search:
    """Update commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lookup(self, name=""):
        """Looks up a guild member by score"""
        try:
            members = Member.objects(Q(fam_name__icontains = name) | Q(char_name__icontains = name))
            rows = get_row(members, False)

            data = tabulate(rows,
                            headers,
                           'simple',)
            for page in paginate(data):
                await self.bot.say(page)

        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")



def setup(bot):
    bot.add_cog(Search(bot))
