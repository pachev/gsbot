import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime

from member import Member
from utils import *


class Add:
    """Add commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def add(self,
                  ctx,
                  fam_name,
                  char_name,
                  level: int,
                  ap : int,
                  dp: int,
                  char_class,
                  user: discord.user = None):
        """Adds yourself as a member to the database. This member is linked with your discord id
        and can only be updated by either that member or an officer.
        Note: Total gear score and rank is auto calculated."""


        try:
            print(ctx.message.author)
            print(user.roles)
        except Exception as e:
            print(e)
        author = ctx.author
        roles = [u.name for u in author.roles]

        try:
            print('inside try')
            member = Member(fam_name=fam_name, 
                            char_name=char_name, 
                            level= level,
                            ap = ap,
                            dp = dp,
                            char_class= char_class,
                            gear_score = ap + dp)

            if not user:
                member.discord = author.id
                member.rank = 'Officer' if admin_user in roles else 'Member'
                count = len(Member.objects(discord = author.id))
                if count >= 1:
                    await self.bot.say("Cannot add more than one character to this discord id. Try rerolling with gsbot reroll")
                    return
            else:
                user_roles = [u.name for u in user.roles]
                member.discord = user.id
                member.rank = 'Officer' if admin_user in user_roles else 'Member'
                if admin_user not in roles:
                    await self.bot.say("Only officers may perform this action")
                    return


            member.save()
            info = [["Success Adding User"], ["Character", char_name], ["gear_score", ap+dp], ["Discord", ctx.message.author.id]]
            await self.bot.say(codify(tabulate(info)))

        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")

    @commands.command(pass_context=True)
    async def reroll(self, ctx, new_char_name, level: int, ap : int, dp: int, new_char_class):
        """Just for someone special: Allows you to reroll """

        author = ctx.message.author
        user = Member.objects(discord = author).first()
        date = datetime.now()
        if not user:
            await self.bot.say("Can't reroll if you're not in the database :(, try adding yoursell first")


        else:
            try:
                user.char_name = new_char_name
                user.ap = ap
                user.dp = dp
                user.gear_score = ap + dp
                user.char_class = new_char_class
                user.updated = date
                user.save()

                info = [["Success Re-Rolling"], 
                        ["New Char", new_char_name], 
                        ["New GS", ap+dp], 
                        ["New Class", new_char_class]]

                await self.bot.say(codify(tabulate(info)))

            except Exception as e:
                print(e)
                await self.bot.say("Something went horribly wrong")


def setup(bot):
    bot.add_cog(Add(bot))
