import discord
from discord.ext import commands
from tabulate import tabulate

from models import Member
from utils import *


class Delete:
    """Delete commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def delete(self, ctx, fam_name=''):
        """Deletes character from list. **officers can add an optional family name at the
        end to delete a certain user"""

        try:
            author = ctx.message.author
            if not fam_name:
                member = Member.objects(discord = author.id).first()
            else:
                member = Member.objects(fam_name = fam_name)(server=ctx.message.server.id).first()
                roles = [u.name for u in author.roles]
                if admin_user not in roles:
                    await self.bot.say("Only officers may perform this action")
            info = [["Success Deleting User"], ["Character", member.char_name], ["Family", member.fam_name]]
            member.delete()
            await self.bot.say(codify(tabulate(info)))
        except Exception as e:
            print(e)
            await self.bot.say(codify("Error deleting user"))


def setup(bot):
    bot.add_cog(Delete(bot))
