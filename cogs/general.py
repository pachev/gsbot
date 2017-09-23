import discord
import csv
from discord.ext import commands
from tabulate import tabulate

from models import Member
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
            members = Member.objects(server=ctx.message.server.id)
            officers = members(rank='Officer')
            average = members.average('gear_score')
            lowest = members.order_by('+gear_score').first()
            highest = members[0]
            count = members.count()
            officer_count = officers.count()
            member_count = count - officer_count
            info.append(['Average', round(average,2)])
            info.append(['Lowest', lowest.gear_score, lowest.fam_name, lowest.char_name])
            info.append(['Highest', highest.gear_score, highest.fam_name, highest.char_name])
            info.append(['Total Officers', officer_count])
            info.append(['Total Members', member_count])
            info.append(['Guild Total', count])
            data = tabulate(info)

            await self.bot.say(codify(data))
        except Exception as e:
            print(e)
            await self.bot.say("Could not retrieve info")

    @commands.command()
    async def export(self):
        """Exports current guild data"""

        members = Member.objects()
        rows = get_row(members, False)
        rows.insert(0, headers)
        try:
            with open('./members.csv', 'w') as myfile:
                wr = csv.writer(myfile)
                wr.writerows(rows)
            await self.bot.upload('./members.csv')
        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")


def setup(bot):
    bot.add_cog(General(bot))
