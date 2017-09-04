from discord.ext import commands
from configparser import ConfigParser

#Config Parseer that reads basic information. This file must be supplied
#For security reasons, it is not included in the repository, you will need
#your own.
config = ConfigParser()  
config.read('config.ini')  

collection = config.get('db', 'collection')
db_name = config.get('db', 'name')
token = config.get('auth', 'token2') 

#User role that officer commands are checked against
admin_user = 'Admin'

initial_extensions = ('cogs.add',)
headers = ['Rank', 'Fam', 'Char', 'Class', 'Lvl', 'AP', 'DP','GS', 'Updated']

description = '''
This the official Gear Score bot of the Legendary Guild Sazerac.
Made by drawven(drawven@gmail.com)
'''

#utility method to wrap string in codeblocks
def codify(s):
    return '```\n' + s + '\n```'

def get_row(members, filter, num=-1):
    if filter:
        return [[u.rank, u.fam_name, u.char_name, u.char_class, u.level, u.ap, u.dp, u.gear_score, u.updated] for u in members[:num]] 

    return [[u.rank, u.fam_name, u.char_name, u.char_class, u.level, u.ap, u.dp, u.gear_score, u.updated] for u in members] 

def paginate(data):
    paginator = commands.Paginator()
    for i in data.splitlines():
        paginator.add_line(i)
    return paginator.pages


