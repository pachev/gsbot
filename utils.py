from discord.ext import commands
from configparser import ConfigParser
from models.activity import Activity
import sys

# The inital config.ini must be supplied in order to retrieve
# basic information
from models.server_settings import ServerSettings

# TODO: User Environmental Variables instead of ini file
CONFIG = ConfigParser(allow_no_value=True)
CONFIG.read('config.ini')

CHARACTER_COLLECTION = CONFIG.get('db', 'character_collection')
SERVER_COLLECTION = CONFIG.get('db', 'server_collection')
MEMBER_COLLECTION = CONFIG.get('db', 'member_collection')
HIST_COLLECTION = CONFIG.get('db', 'historical_collection')
DB_NAME = CONFIG.get('db', 'name')
DB_HOST = CONFIG.get('db', 'host')
DB_USER = CONFIG.get('auth', 'user')
DB_PASS = CONFIG.get('auth', 'pwd')
TOKEN = CONFIG.get('auth', 'token')
PIC_TAG = 'GEAR_PICS'
HAS_CLOUD_STORAGE = CONFIG.getboolean('cloudinary', 'has_cloud_storage')
CLOUD_NAME = CONFIG.get('cloudinary', 'cloud_name')
CLOUDINARY_API = CONFIG.get('cloudinary', 'api_key')
CLOUDINARY_SECRET = CONFIG.get('cloudinary', 'api_secret')

# User role that officer commands are checked against
ADMIN_USER = 'Officers'

INITIAL_EXTENSIONS = ('cogs.add',
                      'cogs.delete',
                      'cogs.general',
                      'cogs.listings',
                      'cogs.search',
                      'cogs.update',
                      'cogs.extras')

HEADERS = ['Rank', 'Fam', 'Char', 'Class', 'Lvl', ' % ', 'AP', 'AAP', 'DP', 'GS', 'PlayStyle', 'Updated']

CHARACTER_CLASSES = [
    "MUSA",
    "DARKKNIGHT",
    "BERSERKER",
    "KUNOICHI",
    "MAEHWA",
    "MYSTIC",
    "NINJA",
    "RANGER",
    "SORCERESS",
    "STRIKER",
    "TAMER",
    "VALKYRIE",
    "WARRIOR",
    "WITCH",
    "WIZARD",
    "LAHN",
    "ARCHER",
    "SHAI",
    "GUARDIAN",
    "HASHASHIN",
    "NOVA"
]

CHARACTER_CLASS_SHORT = {
    "DK": "DARKKNIGHT",
    "ZERKER": "BERSERKER",
    "KUNO": "KUNOICHI",
    "SORC": "SORCERESS",
    "VALK": "VALKYRIE",
    "WIZ": "WIZARD",
}

DESCRIPTION = '''
https://discord.gg/STa7Ebz

This the official Gear Score bot for Black Desert Online. 
For visual data go to: https://gsbot.pachevjoseph.com
For issues/suggestions email me: pachevjoseph@gmail.com. 
'''


# utility method to wrap string in codeblocks
def codify(s):
    return '```\n' + s + '\n```'


def get_row(members, filter, num=-1):
    if filter:
        return [[u.rank.title(),
                 u.fam_name.title(),
                 u.char_name.title(),
                 u.char_class.title(),
                 u.level,
                 u.progress,
                 u.ap,
                 u.aap,
                 u.dp,
                 u.gear_score,
                 u.playstyle,
                 u.updated.strftime('%x')]
                for u in members[:num]]

    return [[u.rank.title(),
             u.fam_name.title(),
             u.char_name.title(),
             u.char_class.title(),
             u.level,
             u.progress,
             u.ap,
             u.aap,
             u.dp,
             u.gear_score,
             u.playstyle,
             u.updated.strftime('%x')]
            for u in members]


def paginate(data):
    paginator = commands.Paginator()
    for i in data.splitlines():
        paginator.add_line(i)
    return paginator.pages


async def check_character_name(ctx, char_class):
    # if char_class is shorthand for a class name (EX. DK = DARKKNIGHT) then set it to the real name
    char_class = CHARACTER_CLASS_SHORT.get(char_class.upper()) if CHARACTER_CLASS_SHORT.get(
        char_class.upper()) else char_class

    # check for invalid class names
    if char_class.upper() not in CHARACTER_CLASSES:
        # find possible class names that user was trying to match
        possible_classes = list(filter(
            lambda class_name: char_class.upper() in class_name,
            CHARACTER_CLASSES,
        ))
        if len(possible_classes) > 1:
            await ctx.send(codify("Character class not recognized.\n"
                                 "Did you mean {}?".format(", ".join(
                possible_classes[:-1]) + " or " + possible_classes[-1])
                                 ))
        elif len(possible_classes) == 1:
            await ctx.send(codify("Character class not recognized.\n"
                                 "Did you mean {}?".format(possible_classes[0])
                                 ))
        else:
            await ctx.send(
                codify("Character class not recognized, here is a list "
                       "of recognized classes\n "
                       + "\n ".join(CHARACTER_CLASSES)))
        return False

    return True


def print_error(error: Exception, message='Error'):
    output = "{}\n\n{}".format(message, error)
    print(output, file=sys.stderr)
    sys.stderr.flush()


def logActivity(message: str, user: str):
    try:
        activity = Activity(message=message, user=user)
        activity.save()
    except Exception as e:
        print_error(e)


OFFICER_MODE_MESSAGE = 'Only officers can request this information in officer mode.'
CONTENT_SENT_MESSAGE = 'Content sent, please check your private messages.'


def is_officer_mode(server: int):
    setting = ServerSettings.objects(server=server).first()
    if setting:
        return setting.officer_mode
    return False


def is_user_officer(roles: list):
    role_names = [r.name for r in roles]
    return ADMIN_USER in role_names


async def send_or_display(server: int, author, ctx, content):
    if is_officer_mode(server):
        if is_user_officer(author.roles):
            await ctx.author.send(content)
            return
        else:
            await ctx.send(OFFICER_MODE_MESSAGE)
            return

    await ctx.send(content)


def is_playstyle_valid(playstyle: str) -> bool:
    val = playstyle if playstyle is not None else ""
    return val.lower() in ["awakening", "succession"]
