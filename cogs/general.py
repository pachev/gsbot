import discord
import csv
from discord.ext import commands
from tabulate import tabulate

from models.character import Character
from models.server_settings import ServerSettings
from utils import *


class General:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def info(self, ctx):
        """List important gear score info. Lowest, highest_gs, average, newest(not yet), oldest,
        total users, total officers, total members"""

        try:
            info = []
            members = Character.primary_chars(server=ctx.message.server.id)
            if members:
                officers = members(rank='Officer')
                average_gs = members.average('gear_score')
                lowest_gs = members.order_by('+gear_score').first()
                highest_gs = members.first()
                count = members.count()
                officer_count = officers.count()
                member_count = count - officer_count
                info.append([' Gear Score '])
                info.append(['-------------------------'])
                info.append(['Average', round(average_gs,2)])
                info.append(['Lowest', lowest_gs.gear_score, lowest_gs.fam_name.title(), lowest_gs.char_name.title()])
                info.append(['Highest', highest_gs.gear_score, highest_gs.fam_name.title(), highest_gs.char_name.title()])
                info.append([''])
                info.append(['-------------------------'])
                info.append(['Counts '])
                info.append(['-------------------------'])
                info.append(['Total Officers', officer_count])
                info.append(['Total Members', member_count])
                info.append(['Guild Total', count])
                data = tabulate(info)
            else:
                data = "No members yet to display info. Try adding some members :D"

            await self.bot.say(codify(data))
        except Exception as e:
            print(e)
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

            if is_officer_mode(ctx.message.server.id):
                if is_user_officer(ctx.message.author.roles):
                    await self.bot.send_file(ctx.message.author, 'members.csv', content=codify('Member info attached'))
                    await self.bot.say(codify('File sent. Please check your private messages'))
                    return
                else:
                    await self.bot.say(codify(OFFICER_MODE_MESSAGE))
                    return
            await self.bot.upload('./members.csv')
        except Exception as e:
            print_error(e)
            await self.bot.say(codify('Could not export data'))

    @commands.command(pass_context=True)
    async def officer_mode(self, ctx, status: str):
        """Turns officer mode on or off: Officer mode limits list and lookup to officers only"""

        if status.lower() not in ['on', 'off']:
            await self.bot.say(codify('Command only accepts on or off'))
            return

        server = ctx.message.server.id
        roles = [r.name for r in ctx.message.author.roles]
        officer_mode = True if status.lower() == 'on' else False
        if ADMIN_USER not in roles:
            await self.bot.say(codify('Only officers can perform this action'))
            return

        try:
            server_setting = ServerSettings.objects(server=server).first()
            if not server_setting:
                setting = ServerSettings(server=server, officer_mode=officer_mode)
                setting.save()
            else:
                server_setting.update(officer_mode=officer_mode)
                server_setting.save()

            logActivity('Server settings updated on {}'.format(ctx.message.server.name), ctx.message.author.name)
            await self.bot.say(codify('Officer Mode successfuly changed to {}'.format(status)))
        except Exception as e:
            print_error(e)
            await self.bot.say("Could not change officer mode to {}".format(status))


def setup(bot):
    bot.add_cog(General(bot))
