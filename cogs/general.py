import discord
import csv
from discord.ext import commands
from tabulate import tabulate

from member import Member
from utils import *


class General:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self):
        """List important gear score info. Lowest, highest, average, newest(not yet), oldest, total users, total officers, total members"""

        try:
            info = []
            members = Member.objects()
            officers = Member.objects(rank='Officer')
            average = Member.objects.average('gear_score')
            lowest = Member.objects.order_by('+gear_score').first()
            highest = members[0]
            info.append(['Average', round(average,2)])
            info.append(['Lowest', lowest.gear_score, lowest.fam_name, lowest.char_name])
            info.append(['Highest', highest.gear_score, highest.fam_name, highest.char_name])
            info.append(['Total Officers', len(officers)])
            info.append(['Total Members', len(members) - len(officers)])
            info.append(['Guild Total', len(members)])
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
