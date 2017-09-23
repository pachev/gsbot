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

    @commands.command(pass_context=True)
    async def lookup(self, ctx, name=""):
        """Looks up a guild member by family name or character name"""
        try:
            members = Member.objects(Q(fam_name__icontains = name) | Q(char_name__icontains = name))
            rows = get_row(members, False)
            data = tabulate(rows,
                            headers,
                            'simple',)

            if members.count() == 1:
                await self.bot.say(codify(data) +"\n" + members.first().gear_pic)
            else:
                for page in paginate(data):
                    await self.bot.say(page)

        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")

    @commands.command(pass_context=True)
    async def class_search(self, ctx, char_class=""):
        """Looks up guild members by class"""
        try:

            if char_class.lower() == "dk":
                all_members = Member.objects(Q(char_class__iexact = char_class)
                                         | Q(char_class__iexact = "dark")
                                         | Q(char_class__iexact = "darkknight")
                                         | Q(char_class__iexact = "dark knight"))
            elif char_class.lower() == "sorc":
                all_members = Member.objects(Q(char_class__iexact = char_class)
                                         | Q(char_class__iexact = "sorceress"))
            else:
                all_members = Member.objects(char_class__iexact = char_class)

            members = all_members(server=ctx.message.server.id)
            count = members.count()
            rows = get_row(members, False)

            data = tabulate(rows,
                            headers,
                            'simple',)
            for page in paginate("Total Number of " + char_class + "on this server: " + str(count) + "\n\n" + data):
                await self.bot.say(page)

        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")



def setup(bot):
    bot.add_cog(Search(bot))
