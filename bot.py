import logging
import time
import os
import discord
from discord.ext import commands
start_time = time.strftime('%m-%d-%YdT%H%M%S', time.localtime())

#config
log_level = logging.INFO

#filepaths
token_file = './token.txt'
logfilepath = './logs'
logfile = 'Bot-' + start_time + '.log'


#logging setup
if not os.path.exists(logfilepath):
    os.makedirs(logfilepath)
logging.basicConfig(filename= logfilepath + '/' + logfile, level=log_level)
console = logging.StreamHandler()
console.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


# Bot setup
with open(token_file) as f:
    TOKEN = f.read().strip()
    if not TOKEN:
        logging.error('Token not found in ' + token_file)
        raise ValueError('Token not found in ' + token_file)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} and ready to go!')

@bot.command(pass_context=True)
async def ping(ctx):
    logging.info(f'{ctx.message.author} ran command .ping in {ctx.guild.name}-{ctx.channel.name}')
    await ctx.send('Pong')


#login
bot.run(TOKEN)
