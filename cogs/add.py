import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime

from models.character import Character
from models.member import Member
from models.historical import Historical
from models.server import Server
from utils import *

class Add:
    """Add commands."""

    def __init__(self, bot):
        self.bot = bot

    async def __get_rank_and_discord_id(self, author, user, roles):
        if not user:
            discord_id = author.id
            discord_username = author.name
            rank = 'Officer' if ADMIN_USER in roles else 'Member'
        else:
            try:
                user_roles = [u.name for u in user.roles]
                rank = 'Officer' if ADMIN_USER in user_roles else 'Member'
            except Exception as e:
                rank = 'Member'
                print(e)
            discord_id = user.id
            discord_username = user.name
            if ADMIN_USER not in roles:
                await self.bot.say(codify("Only officers may perform this action"))
                return (None, None)
        
        return (rank, discord_id, discord_username)

    def __get_server_and_member(self, server_id, discord_id):
        member = Member.objects(discord = discord_id).first()
        server = Server.objects(id=server_id).first()

        if not server:
            server = Server.create({'id': server_id})
        if not member:
            member = Member.create({'discord': discord_id})

        # Checks if member being added is in the server
        server_member = Member.objects(servers=server_id, discord=discord_id).first()
        if not server_member:
            server.members.append(member)
            server.save()
            member.servers.append(server_id)
            member.save()

        return (server, member)

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
        """Adds your primary character to the guild. This character is linked with your
        discord id and can only be updated by either that member or an officer.
        **Officers can add a user by tagging them at the end. eg @drawven**
        Note: Total gear score and rank is auto calculated."""

        # Checks character name to make sure it is correct
        try:

            if not await check_character_name(self.bot, char_class):
                return
            author = ctx.message.author
            server_id= ctx.message.server.id
            roles = [u.name for u in author.roles]
            rank, discord_id, discord_username = await self.__get_rank_and_discord_id(author, user, roles)
            server, member = self.__get_server_and_member(server_id, discord_id)

            if rank is None or discord_id is None:
                return

            character = Character.primary_chars(member=discord_id).first()
            isPrimary = False if character else True


            character = Character.create({
                'rank': rank,
                'fam_name': fam_name.upper(),
                'char_name': char_name.upper(),
                'char_class': char_class.upper(),
                'server': server_id,
                'level': level,
                'ap': ap,
                'dp': dp,
                'gear_score': ap + dp,
                'primary': isPrimary,
                'member': discord_id,
            })
            member.characters.append(character)
            member.save()

            row = get_row([character], False)
            data = tabulate(row, HEADERS, 'simple')

            await self.bot.say(codify("Success Adding Character for member {}\n\n".
                                      format(discord_username.upper()) + data))

        except Exception as e:
            print(e)
            await self.bot.say("Something went horribly wrong")

    @commands.command(pass_context=True)
    async def reroll(self, ctx, new_char_name, level: int, ap : int, dp: int, new_char_class):
        """Just for someone special: Allows you to reroll your main character """

        author = ctx.message.author.id
        character = Character.primary_chars(member = author).first()
        date = datetime.now()
        if not character:
            await self.bot.say("Can't reroll if you're not in the database :(, try adding a character first")
            return

        if not await check_character_name(self.bot, new_char_class):
            return

        else:
            try:
                ## Adds historical data to database
                update = Historical.create({
                    'type': "reroll",
                    'char_class': character.char_class.upper(),
                    'timestamp': date,
                    'level':float(str(character.level) + '.' + str(round(character.progress))) ,
                    'ap': character.ap,
                    'dp': character.dp,
                    'gear_score': character.gear_score
                })

                historical_data = character.hist_data
                historical_data.append(update)

                character.update_attributes({
                    'char_name': new_char_name.upper(),
                    'ap': ap, 
                    'dp': dp,
                    'level': level,
                    'gear_score': ap + dp,
                    'char_class': new_char_class.upper(),
                    'updated': date,
                    'hist_data': historical_data
                })
                
                row = get_row([character], False)
                data = tabulate(row, HEADERS, 'simple')

                await self.bot.say(codify("Success Rerolling\n\n" + data))

            except Exception as e:
                print(e)
                await self.bot.say("Could not reroll")

def setup(bot):
    bot.add_cog(Add(bot))
