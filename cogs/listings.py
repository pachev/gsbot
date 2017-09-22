import discord
from discord.ext import commands
from tabulate import tabulate

from models import Member
from utils import *

class Listing:
    """All the listing commands."""
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def list(self,num=100):
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
                await self.bot.say(page)
        except Exception as e:
            await self.bot.say("Something went horribly wrong")
            print(e)


    @commands.command()
    async def over(self, num=400):
        """List all the members over a certain gear score"""
        try:
            members = Member.objects(gear_score__gte = num)
            rows = get_row(members,False)

            data = tabulate(rows,
                            headers,
                           'simple',)

            for page in paginate(data):
                await self.bot.say(page)

        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")


    @commands.command()
    async def under(self, num=400):
        """List all the members under a certain gear score"""
        try:
            members = Member.objects(gear_score__lte = num)
            rows = get_row(members, False)
            data = tabulate(rows,
                            headers,
                           'simple',)

            for page in paginate(data):
                await self.bot.say(page)
        except:
            await self.bot.say("Something went horribly wrong")

def setup(bot):
    bot.add_cog(Listing(bot))
