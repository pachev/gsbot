from discord.ext import commands
from configparser import ConfigParser

# The inital config.ini must be supplied in order to retrieve
# basic information
CONFIG = ConfigParser()
CONFIG.read('config.ini')

COLLECTION = CONFIG.get('db', 'collection')
HIST_COLLECTION = CONFIG.get('db', 'historical')
DB_NAME = CONFIG.get('db', 'name')
DB_USER = CONFIG.get('auth', 'user')
DB_PASS = CONFIG.get('auth', 'pwd')
TOKEN = CONFIG.get('auth', 'dev_token')

# User role that officer commands are checked against
ADMIN_USER = 'Officers'

INITIAL_EXTENSIONS = ('cogs.add',
                      'cogs.delete',
                      'cogs.general',
                      'cogs.listings',
                      'cogs.search',
                      'cogs.update',
                      'cogs.extras')

HEADERS = ['Rank', 'Fam', 'Char', 'Class', 'Lvl', ' % ', 'AP', 'DP', 'GS', 'Updated']

DESCRIPTION = '''
This the official Gear Score bot. 
Made by drawven(drawven@gmail.com)
'''


# utility method to wrap string in codeblocks
def codify(s):
    return '```\n' + s + '\n```'


def get_row(members, filter, num=-1):
    if filter:
        return [[u.rank, u.fam_name, u.char_name, u.char_class, u.level, u.progress, u.ap, u.dp,
                 u.gear_score, u.updated.strftime('%D')]
                for u in members[:num]]

    return [[u.rank, u.fam_name, u.char_name, u.char_class, u.level, u.progress, u.ap, u.dp,
             u.gear_score, u.updated.strftime('%D')]
            for u in members]


def paginate(data):
    paginator = commands.Paginator()
    for i in data.splitlines():
        paginator.add_line(i)
    return paginator.pages
