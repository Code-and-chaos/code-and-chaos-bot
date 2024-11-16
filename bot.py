import discord
from discord.ext import commands

# Bot setup
TOKEN = [REDACTED FOR GITHUB]
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} and ready to go!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong')

bot.run(TOKEN)
