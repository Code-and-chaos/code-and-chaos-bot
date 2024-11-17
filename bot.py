import logging
import time
import os
import discord
from discord.ext import commands
start_time = time.strftime('%m-%d-%YdT%H%M%S', time.localtime())
calculation_start_time = time.time()

# Config
log_level = logging.INFO

# Filepaths
token_file = './token.txt'
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

    try:
        await bot.tree.sync()
        logging.info("Slash commands synced successfully!")
    except Exception as e:
        logging.error(f"Error syncing commands: {e}")

@bot.tree.command(name="ping", description="Pings the bot.")
async def ping(interaction: discord.Interaction):
    logging.info(f'{interaction.user} ran command /ping in {interaction.guild.name}-{interaction.channel.name}')
    await interaction.response.send_message("Pong")

@bot.tree.command(name="help", description="Display a list of all available commands.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Help - Available Commands",
        description="Here is a list of all commands you can use:",
        color=discord.Color.blue()
    )

    for command in bot.tree.get_commands():
        embed.add_field(
            name=f"/{command.name}",
            value=command.description if command.description else "No description available.",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="info", description="Displays information about the bot.")
async def info_command(interaction: discord.Interaction):
    current_time = time.time()
    uptime = int(current_time - calculation_start_time)

    embed = discord.Embed(
        title="Bot Information",
        description="Here is some information about the bot:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Bot Name:",
        value=bot.user.name,
        inline=False
    )
    embed.add_field(
        name="Uptime:",
        value=f"{uptime // 3600} hours { (uptime % 3600) // 60} minutes",
        inline=False
    )
    embed.add_field(
        name="Developer:",
        value="@QuietTerminalInteractive (https://github.com/QuietTerminalInteractive), @Minecrafter8001 (https://github.com/Minecrafter8001)",
        inline=False
    )

    embed.add_field(
        name="Total Users:",
        value=str(sum(guild.member_count for guild in bot.guilds)),
        inline=True
    )
    embed.add_field(
        name="Tip:",
        value="Use `/help` to see a list of all available commands.",
        inline=False
    )

    await interaction.response.send_message(embed=embed)

# Login
bot.run(TOKEN)
