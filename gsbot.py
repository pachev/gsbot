import traceback
from mongoengine import *
import sys
import discord
from discord.ext import commands
from cloudinary import config

from utils import *
from models.character import Character

# Main connection function offered by mongoengine defaults are localhost:27017
connect(DB_NAME,
        host=DB_HOST,
        username=DB_USER,
        password=DB_PASS,
        authentication_source=DB_NAME)

if HAS_CLOUD_STORAGE:
    config(
        cloud_name = CLOUD_NAME,
        api_key = CLOUDINARY_API,
        api_secret = CLOUDINARY_SECRET
    )


bot = commands.Bot(command_prefix='gsbot ', description=DESCRIPTION)


# Here we load our extensions listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in INITIAL_EXTENSIONS:
        try:
            bot.load_extension(extension)
            print('loaded {}'.format(extension))
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Discord Version: ', discord.__version__)
    await bot.change_presence(
        activity=discord.Game(name='GSBOT For BDO!!!!!', type=1, url='https://gsbot.pachevjoseph.com'),
        status=discord.Status.online
    )
    print('------')


@bot.event
async def on_command_error(ctx, error):
    """
    Retrieved from : https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
    The event triggered when an error is raised while invoking a command.
     Parameters
     ------------
     ctx: commands.Context
         The context used for command invocation.
     error: commands.CommandError
         The Exception raised.
     """

    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    # This prevents any cogs with an overwritten cog_command_error being handled here.
    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return


    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That is not a command. Try "gsbot help"')

    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except discord.HTTPException:
            pass

    # For this error example we check to see where it came from...
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('This command is missing a required argument. Try gsbot help ' + ctx.command)

    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send('Could not understand the arguments given. Try gsbot help ' + ctx.command)

    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        await ctx.send('Something went horribly wrong with the command' + ctx.command)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

bot.run(TOKEN, bot=True, reconnect=True)
