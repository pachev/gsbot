import math
from datetime import datetime

import discord
from tabulate import tabulate

from models.character import Character
from models.historical import Historical
from models.member import Member
from models.server import Server
from utils import *


class Add(commands.Cog):
    """Add commands."""

    def __init__(self, bot):
        self.bot = bot

    async def __get_rank_and_member(self, author, user, roles, ctx):
        if not user:
            discord_user = author
            rank = 'Officer' if ADMIN_USER in roles else 'Member'
        else:
            try:
                user_roles = [u.name for u in user.roles]
                rank = 'Officer' if ADMIN_USER in user_roles else 'Member'
            except Exception as e:
                rank = 'Member'
                print(e)
            discord_user = user
            if ADMIN_USER not in roles:
                await ctx.send(codify("Only officers may perform this action"))
                return (None, None)

        return rank, discord_user

    def __get_server_and_member(self, discord_server, discord_user):
        member = Member.objects(discord=discord_user.id).first()
        server = Server.objects(id=discord_server.id).first()

        if not server:
            server = Server.create({
                'id': discord_server.id,
                'name': discord_server.name,
                'avatar': str(discord_server.icon_url) if discord_server.icon_url is not None else ''
            })

        if not member:
            member = Member.create({
                'discord': discord_user.id,
                'name': discord_user.name,
                'avatar': str(discord_user.avatar_url) if discord_user.avatar_url is not None else ''
            })

        # Checks if member being added is in the server
        server_member = Member.objects(servers=discord_server.id, discord=discord_user.id).first()
        if not server_member:
            server.members.append(member)
            server.save()
            member.servers.append(discord_server.id)
            member.save()

        return (server, member)

    @commands.command(pass_context=True)
    async def add(self,
                  ctx,
                  fam_name,
                  char_name,
                  level: int,
                  ap: int,
                  aap: int,
                  dp: int,
                  char_class,
                  user: discord.User = None):
        """Adds your primary character to the guild. This character is linked with your
        discord id and can only be updated by either that member or an officer.
        **Officers can add a user by tagging them at the end. eg @drawven**
        Note: Total gear score, renown score, and rank are auto calculated."""

        # Checks character name to make sure it is correct
        try:

            if not await check_character_name(ctx, char_class):
                return
            author = ctx.message.author
            discord_server = ctx.message.guild
            roles = [u.name for u in author.roles]
            rank, discord_user = await self.__get_rank_and_member(author, user, roles, ctx)
            server, member = self.__get_server_and_member(discord_server, discord_user)

            if rank is None or discord_user.id is None:
                return

            character = Character.primary_chars(member=discord_user.id).first()
            is_primary = False if character else True

            character = Character.create({
                'rank': rank,
                'fam_name': fam_name.upper(),
                'char_name': char_name.upper(),
                'char_class': char_class.upper(),
                'server': discord_server.id,
                'level': level,
                'ap': ap,
                'aap': aap,
                'dp': dp,
                'gear_score': max(aap, ap) + dp,
                'renown_score': math.trunc((ap + aap) / 2 + dp),
                'primary': is_primary,
                'member': discord_user.id,
            })
            member.characters.append(character)
            member.save()

            row = get_row([character], False)
            data = tabulate(row, HEADERS, 'simple')
            logActivity('{} has added a character'.format(character.fam_name), user.name if user else author.name)
            await ctx.send(codify("Success Adding Character for member {} :D\n\n".
                                  format(discord_user.name.upper()) + data))

        except Exception as e:
            print_error(e)
            await ctx.send("Something went horribly wrong")

    @commands.command(pass_context=True)
    async def reroll(self, ctx, new_char_name, level: int, ap: int, aap: int, dp: int, new_char_class):
        """Just for someone special: Allows you to reroll your main character """

        author = ctx.message.author.id
        character = Character.primary_chars(member=author).first()
        date = datetime.now()
        if not character:
            await ctx.send("Can't reroll if you're not in the database :(, try adding a character first")
            return

        if not await check_character_name(ctx, new_char_class):
            return

        else:
            try:
                # Adds historical data to database
                update = Historical.create({
                    'type': "reroll",
                    'char_class': character.char_class.upper(),
                    'timestamp': date,
                    'level': float(str(character.level) + '.' + str(round(character.progress))),
                    'ap': character.ap,
                    'aap': character.aap,
                    'dp': character.dp,
                    'gear_score': character.gear_score,
                    'renown_score': character.renown_score,
                })

                historical_data = character.hist_data
                fame = character.fame or 0
                historical_data.append(update)

                character.update_attributes({
                    'char_name': new_char_name.upper(),
                    'ap': ap,
                    'aap': aap,
                    'dp': dp,
                    'level': level,
                    'gear_score': max(aap, ap) + dp,
                    'renown_score': math.trunc((ap + aap) / 2 + dp),
                    'char_class': new_char_class.upper(),
                    'updated': date,
                    'hist_data': historical_data
                })

                row = get_row([character], False)
                data = tabulate(row, HEADERS, 'simple')

                logActivity('{} has rerolled a character'.format(character.fam_name), ctx.message.author.name)
                reminder = '\n\nRemember to add a new pic with gsbot attach_pic!'
                await ctx.send(codify("Success Rerolling\n\n" + data + reminder))

            except Exception as e:
                print_error(e)
                await ctx.send("Could not reroll")


def setup(bot):
    bot.add_cog(Add(bot))
