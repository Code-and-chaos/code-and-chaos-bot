import logging
import time
import os
import json
import discord
import importlib.util
from discord.ext import commands
start_time = time.strftime('%m-%d-%YdT%H%M%S', time.localtime())
calculation_start_time = time.time()

# Config
log_level = logging.INFO
LOG_CHANNEL_ID = 1091009808901099583

# Paths
commands_directory = './commands'
config_file = './config.json'
logfilepath = './logs'
logfile = 'Bot-' + start_time + '.log'


# Logging setup
if not os.path.exists(logfilepath):
    os.makedirs(logfilepath)
logging.basicConfig(filename= logfilepath + '/' + logfile, level=log_level)
console = logging.StreamHandler()
console.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


# Bot setup
with open(config_file) as f:
    token_data = json.load(f)
    TOKEN = token_data.get('token')
    if not TOKEN:
        logging.error('Token not found in ' + config_file)
        raise ValueError('Token not found in ' + config_file)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)


async def load_commands():
    for filename in os.listdir(commands_directory):
        if filename.endswith(".py") and filename != "__init__.py":
            file_path = os.path.join(commands_directory, filename)
            module_name = filename[:-3]

            logging.info(f"Loading command module: {module_name}")

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'setup'):
                module.setup(bot, logging, LOG_CHANNEL_ID)
                logging.info(f"Successfully set up module: {module_name}")
            else:
                logging.warning(f"No setup function found in module: {module_name}")




@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} and ready to go!')
    try:
        await load_commands()
        await bot.tree.sync()
        logging.info("Slash commands synced successfully!")
    except Exception as e:
        logging.error(f"Error syncing commands: {e}")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        logging.info(f'{interaction.user} ran command /{interaction.command.name} in {interaction.guild.name} #{interaction.channel.name}')


# Login
bot.run(TOKEN)
