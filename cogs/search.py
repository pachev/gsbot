import discord
from discord.ext import commands
from tabulate import tabulate
from mongoengine import *
from typing import Any

from models.character import Character
from utils import *


class Search:
    """Update commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def lookup(self, ctx, query):
        """Looks up a guild member by family name or character name or pass in a user like @drawven"""
        try:
            mentions = ctx.message.mentions
            if len(mentions) >= 1:
                members = Character.primary_chars(member=mentions[0].id)
            else:
                members = Character.primary_chars(Q(fam_name__icontains = query) | Q(char_name__icontains = query),
                                         server = ctx.message.server.id)

            rows = get_row(members, False)
            data = tabulate(rows,
                            HEADERS,
                            'simple',)

            if members.count() == 1:
                content = codify(data) +"\n" + members.first().gear_pic
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, content)
            else:
                for page in paginate(data):
                    await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)

        except Exception as e:
            print_error(e)
            await self.bot.say("Something went horribly wrong")

    @commands.command(pass_context=True)
    async def class_search(self, ctx, char_class=""):
        """Looks up main characters by class"""
        try:

            if char_class.lower() == "dk":
                members = Character.primary_chars(Q(char_class__iexact = char_class)
                                            | Q(char_class__iexact = "dark")
                                            | Q(char_class__iexact = "darkknight")
                                            | Q(char_class__iexact = "dark knight"))
            elif char_class.lower() == "sorc":
                members = Character.primary_chars(Q(char_class__iexact = char_class)
                                            | Q(char_class__iexact = "sorceress"))
            else:
                members = Character.primary_chars(char_class__iexact = char_class)

            count = members(server = ctx.message.server.id).count()
            rows = get_row(members(server = ctx.message.server.id), False)

            data = tabulate(rows,
                            HEADERS,
                            'simple',)
            for page in paginate("Total Number of " + char_class + " on this server: " + str(count) + "\n\n" + data):
                await send_or_display(ctx.message.server.id, ctx.message.author, self.bot, page)

        except Exception as e:
            print_error(e)
            await self.bot.say("Something went horribly wrong")



def setup(bot):
    bot.add_cog(Search(bot))
