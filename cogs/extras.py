import discord
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime
from cloudinary.uploader import upload

from models.character import Character
from utils import *


class Extras:
    """Extra commands for fun"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def attach_pic(self, ctx, url: str = None):
        """ Command to attach a picture to your character. When someone looks you up the attached picture is displayed"""
        try:
            author = ctx.message.author
            attachments = ctx.message.attachments
            character = Character.primary_chars(member = author.id).first()
            if not character:
                await self.bot.say('Could not find a main character for user {}'.format(author.name))
                return

            if url:
                response = upload(url, tags=PIC_TAG)
            else:
                if not attachments:
                    await self.bot.say('You must either attach a picture or provide a url')
                    return
                response = upload(attachments[0]['url'], tags=PIC_TAG)

            character.gear_pic = response['url']
            character.save()
            logActivity('{} has updated picture for {}'.format(character.fam_name.title(), character.char_name), ctx.message.author.name)
            await self.bot.say(codify("Picture added successfully"))
        except Exception as e:
            print(e)
            await self.bot.say("Picture could not be added")

    @commands.command(pass_context=True)
    async def my_list(self,ctx):
        """***Experimental***List all the characters that you have added to the database for this server"""
        try:
            print('server,', ctx.message.server.id)
            members = Character.objects(member=ctx.message.author.id, server = ctx.message.server.id)
            rows = get_row(members, False)

            data = tabulate(rows,
                            HEADERS,
                            'simple',)

            for page in paginate(data):
                await self.bot.say(page)
        except Exception as e:
            await self.bot.say("Something went horribly wrong")
            print_error(e)

    @commands.command(pass_context=True)
    async def set_main(self,ctx,num:int=0):
        """***Experimental*** Changes primary character on server"""
        if not int(num):
            await self.bot.say(codify('Invalid Selection'))
            return
        try:
            print('server,', ctx.message.server.id)
            characters = Character.objects(member=ctx.message.author.id, server = ctx.message.server.id)
            if num < 1 or num > len(characters):
                await self.bot.say(codify('Invalid Selection'))
                return

            num -= 1
            for char in characters:
                char.primary = False
                char.save()
            main = characters[num]
            main.primary = True
            main.save()
            logActivity('{} has changed their main character'.format(main.char_name), ctx.message.author.name)
            await self.bot.say(codify('Main Character Switched Succesfuly to {}'.format(main.char_name)))
        except Exception as e:
            await self.bot.say("Something went horribly wrong")
            print_error(e)


def setup(bot):
    bot.add_cog(Extras(bot))
