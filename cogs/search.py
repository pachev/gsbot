import discord
from discord.ext import commands
from tabulate import tabulate
from mongoengine import *

from models import Member
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

            if len(members) == 1:
                await self.bot.say(codify(data) +"\n" + members.first().gear_pic)
            else:
                for page in paginate(data):
                    await self.bot.say(page)

        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")

    @commands.command()
    async def class_search(self, char_class=""):
        """Looks up a guild members by class"""
        try:

            if char_class.lower() == "dk":
                members = Member.objects(Q(char_class__iexact = char_class) | Q(char_class__iexact = "dark") | Q(char_class__iexact = "dark knight") )
            elif char_class.lower() == "sorc":
                members = Member.objects(Q(char_class__iexact = char_class) | Q(char_class__iexact = "sorceress"))
            else:
                members = Member.objects(Q(char_class__iexact = char_class))

            count = len(members)
            rows = get_row(members, False)

            data = tabulate(rows,
                            headers,
                            'simple',)
            for page in paginate("Total Number of " + char_class + ": " + str(count) + "\n\n" + data):
                await self.bot.say(page)

        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")



def setup(bot):
    bot.add_cog(Search(bot))
