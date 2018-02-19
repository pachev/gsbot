from discord.ext import commands
from configparser import ConfigParser
from models.activity import Activity
import sys

# The inital config.ini must be supplied in order to retrieve
# basic information
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
TOKEN = CONFIG.get('auth', 'dev_token')
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

HEADERS = ['Rank', 'Fam', 'Char', 'Class', 'Lvl', ' % ', 'AP', 'AAP', 'DP', 'GS']

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
]

CHARACTER_CLASS_SHORT = {
    "DK": "DARKKNIGHT",
    "ZERKER": "BERSERKER",
    "KUNO": "KUNOICHI",
    "SORC": "SORCERESS",
    "VALK": "VALKYRIE",
    }

DESCRIPTION = '''
This the official Gear Score bot.
Made by drawven(drawven@gmail.com)
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
                 u.gear_score]
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
             u.gear_score]
            for u in members]


def paginate(data):
    paginator = commands.Paginator()
    for i in data.splitlines():
        paginator.add_line(i)
    return paginator.pages

async def check_character_name(bot, char_class):
    # if char_class is shorthand for a class name (EX. DK = DARKKNIGHT) then set it to the real name
    char_class = CHARACTER_CLASS_SHORT.get(char_class.upper()) if CHARACTER_CLASS_SHORT.get(char_class.upper()) else char_class

    # check for invalid class names
    if char_class.upper() not in CHARACTER_CLASSES:
        # find possible class names that user was trying to match
        possible_classes = list(filter(
            lambda class_name: char_class.upper() in class_name,
            CHARACTER_CLASSES,
        ))
        if len(possible_classes) > 1:
            await bot.say(codify("Character class not recognized.\n"
                                      "Did you mean {}?".format(", ".join(
                possible_classes[:-1]) + " or " + possible_classes[-1])
                                      ))
        elif len(possible_classes) == 1:
            await bot.say(codify("Character class not recognized.\n"
                                      "Did you mean {}?".format(possible_classes[0])
                                      ))
        else:
            await bot.say(
                codify("Character class not recognized, here is a list "
                       "of recognized classes\n "
                       + "\n ".join(CHARACTER_CLASSES)))
        return False

    return True

def print_error(error: Exception, message = 'Error'):
    output = "{}\n\n{}".format(message, error)
    print(output, file=sys.stderr)
    sys.stderr.flush()


def logActivity(message: str, user: str):
    try:
        activity = Activity(message=message, user=user)
        activity.save()
    except Exception as e:
        print_error(e)

