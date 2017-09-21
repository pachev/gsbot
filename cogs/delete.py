import discord
from discord.ext import commands
from tabulate import tabulate

from member import Member
from utils import *


class Delete:
    """Delete commands."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def delete(self, ctx, fam_name):
        """**Officers only** Deletes an added user by family name"""

        author = ctx.message.author
        roles = [u.name for u in author.roles]
        print('starting')
        try:
            print(roles)
        except Exception as e:
            print(e)
        if admin_user not in roles:
            await self.bot.say("Only officers may perform this action")
        else:
            try:
                member = Member.objects(fam_name = fam_name).first()
                info = [["Success Deleting User"], ["Character", member.char_name], ["Family", member.fam_name]]
                member.delete()
                await self.bot.say(codify(tabulate(info)))
            except Exception as e:
                print(e)
                await self.bot.say(codify("Error deleting user, Make sure the spelling is correct"))

    @commands.command(pass_context=True)
    async def delete_me(self, ctx):
        """Deletes your added character"""

        try:
            member = Member.objects(discord = ctx.message.author.id).first()
            info = [["Success Deleting User"], ["Character", member.char_name], ["Discord", member.discord]]
            member.delete()
            await self.bot.say(codify(tabulate(info)))
        except Exception as e:
            print(e)
            await self.bot.say("Error deleting user")


def setup(bot):
    bot.add_cog(Delete(bot))
