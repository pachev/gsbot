import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime

from models import Member, Historical
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
                  user: discord.User = None):
        """Adds yourself as a member to the database. This member is linked with your
        discord id and can only be updated by either that member or an officer.
        **Officers can add a user by tagging them at the end. eg @drawven#8888**
        Note: Total gear score and rank is auto calculated."""


        try:
            author = ctx.message.author
            roles = [u.name for u in author.roles]
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
                count = Member.objects(discord = author.id).count()
                if count >= 1:
                    await self.bot.say("Cannot add more than one character to this discord id. Try rerolling with gsbot reroll")
            else:
                try:
                    user_roles = [u.name for u in user.roles]
                    member.rank = 'Officer' if admin_user in user_roles else 'Member'
                except Exception as e:
                    member.rank = 'Member'
                    print(e)
                member.discord = user.id
                if admin_user not in roles:
                    await self.bot.say("Only officers may perform this action")


            member.server = ctx.message.server.id
            member.save()
            info = [["Success Adding User"], ["Character", char_name], ["gear_score", ap+dp], ["Discord", ctx.message.author.id]]
            await self.bot.say(codify(tabulate(info)))

        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")

    @commands.command(pass_context=True)
    async def reroll(self, ctx, new_char_name, level: int, ap : int, dp: int, new_char_class):
        """Just for someone special: Allows you to reroll """

        author = ctx.message.author.id
        member = Member.objects(discord = author).first()
        date = datetime.now()
        if not member:
            await self.bot.say("Can't reroll if you're not in the database :(, try adding yoursell first")

        else:
            try:
                ## Adds historical data to todabase
                update = Historical(
                    type = "reroll",
                    char_class = member.char_class,
                    timestamp = date,
                    level = member.level + (round(member.progress, 2) * .01),
                    ap = member.ap,
                    dp = member.dp,
                    gear_score = member.gear_score
                )
                update.save()

                member.char_name = new_char_name
                member.ap = ap
                member.dp = dp
                member.gear_score = ap + dp
                member.char_class = new_char_class
                member.updated = date
                member.hist_data.append(update)
                member.save()

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
