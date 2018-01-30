import discord
import csv
from discord.ext import commands
from tabulate import tabulate

from models.character import Character
from utils import *


class General:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def info(self, ctx):
        """List important gear score info. Lowest, highest, average, newest(not yet), oldest,
        total users, total officers, total members"""

        try:
            info = []
            members = Character.primary_chars(server=ctx.message.server.id)
            if members:
                officers = members(rank='Officer')
                average = members.average('gear_score')
                lowest = members.order_by('+gear_score').first()
                highest = members[0]
                count = members.count()
                officer_count = officers.count()
                member_count = count - officer_count
                info.append(['Average', round(average,2)])
                info.append(['Lowest', lowest.gear_score, lowest.fam_name.title(), lowest.char_name.title()])
                info.append(['Highest', highest.gear_score, highest.fam_name.title(), highest.char_name.title()])
                info.append(['Total Officers', officer_count])
                info.append(['Total Members', member_count])
                info.append(['Guild Total', count])
                data = tabulate(info)
            else:
                data = "No members yet to display info. Try adding some members :D"

            await self.bot.say(codify(data))
        except Exception as e:
            print_error('Could not retrieve info' + e)
            await self.bot.say("Could not retrieve info")

    @commands.command(pass_context=True)
    async def export(self, ctx):
        """Exports current guild data"""

        members = Character.primary_chars(server=ctx.message.server.id)
        rows = get_row(members, False)
        rows.insert(0, HEADERS)
        try:
            with open('./members.csv', 'w') as myfile:
                wr = csv.writer(myfile)
                wr.writerows(rows)
            await self.bot.upload('./members.csv')
        except Exception as e:
            print_error('Could not export data\n\n' + e)
            await self.bot.say("Something went horribly wrong")


def setup(bot):
    bot.add_cog(General(bot))
