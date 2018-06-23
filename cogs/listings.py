import discord
from discord.ext import commands
from tabulate import tabulate

from models.character import Character
from utils import *


class Listing:
    """All the listing commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def list(self,ctx,num=100):
        """List all the main characters and their gear score with optional limit.
        Example. gsbot list returns first 100 by default  and gsbot list 5 first 5 sorted by
        gear score"""
        try:
            members = Character.primary_chars(server=ctx.message.server.id)
            rows = get_row(members, True, num)

            data = tabulate(rows,
                            HEADERS,
                           'simple',)
            
            for page in paginate(data):
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)
        except Exception as e:
            await self.bot.say(codify('Could not list members'))
            print_error(e)

    @commands.command(pass_context=True)
    async def over(self, ctx, num=400):
        """List all the main characters over a certain gear score"""
        try:
            members = Character.primary_chars(gear_score__gte = num, server = ctx.message.server.id)
            rows = get_row(members,False)

            data = tabulate(rows,
                            HEADERS,
                           'simple',)

            for page in paginate(data):
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)

        except Exception as e:
            print_error(e)
            await self.bot.say("Something went horribly wrong")

    @commands.command(pass_context=True)
    async def under(self, ctx, num=400):
        """List all the main characters under a certain gear score"""
        try:
            members = Character.primary_chars(gear_score__lte = num, server = ctx.message.server.id)
            rows = get_row(members, False)
            data = tabulate(rows,
                            HEADERS,
                           'simple',)

            for page in paginate(data):
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)
        except Exception as e:
            print_error(e)
            await self.bot.say("Something went horribly wrong")

    @commands.group(pass_context=True)
    async def sort_by(self, ctx):
        """Group of sorting commands"""

        # Checks if no sub-commands are invoked
        if ctx.invoked_subcommand is None:
            await self.bot.say(codify("Sort by any category available(lvl, ap, aap, dp). Try gsbot help sort_by"))

    @sort_by.command(pass_context=True)
    async def lvl(self, ctx, num=100):
        """ - Sorts list by level and progress with optional limiter"""
        try:
            members = Character.primary_chars(server = ctx.message.server.id).order_by('-level', '-progress')
            rows = get_row(members, True, num)

            data = tabulate(rows,
                            HEADERS,
                            'simple',)

            for page in paginate(data):
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)
        except Exception as e:
            await self.bot.say("Could not retrieve list")
            print_error(e)

    @sort_by.command(pass_context=True)
    async def ap(self, ctx, num=100):
        """ - Sorts list by AP with optional limit"""
        try:
            members = Character.primary_chars(server=ctx.message.server.id).order_by('-ap')
            rows = get_row(members, True, num)

            data = tabulate(rows,
                            HEADERS,
                            'simple',)

            for page in paginate(data):
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)
        except Exception as e:
            await self.bot.say("Could not retrieve list")
            print_error(e)

    @sort_by.command(pass_context=True)
    async def aap(self, ctx, num=100):
        """ - Sorts list by awakened AP with optional limit"""
        try:
            members = Character.primary_chars(server=ctx.message.server.id).order_by('-aap')
            rows = get_row(members, True, num)

            data = tabulate(rows,
                            HEADERS,
                            'simple',)

            for page in paginate(data):
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)
        except Exception as e:
            await self.bot.say("Could not retrieve list")
            print_error(e)

    @sort_by.command(pass_context=True)
    async def dp(self, ctx, num=100):
        """ - Sorts list by DP with optional limit"""
        try:
            members = Character.primary_chars(server=ctx.message.server.id).order_by('-dp')
            rows = get_row(members, True, num)

            data = tabulate(rows,
                            HEADERS,
                            'simple',)

            for page in paginate(data):
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)
        except Exception as e:
            await self.bot.say("Could not retrieve list")
            print_error(e)

    @sort_by.command(pass_context=True)
    async def rs(self, ctx, num=100):
        """ - Sorts list by RS (renown score) with optional limit"""
        try:
            members = Character.primary_chars(server=ctx.message.server.id).order_by('-renown_score')
            rows = get_row(members, True, num)

            data = tabulate(rows,
                            HEADERS,
                            'simple',)

            for page in paginate(data):
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)
        except Exception as e:
            await self.bot.say("Could not retrieve list")
            print_error(e)


def setup(bot):
    bot.add_cog(Listing(bot))
