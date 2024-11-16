import discord
from discord.ext import commands

# Bot setup
with open('token.txt') as f:
    TOKEN = f.read().strip()
    if not TOKEN:
        raise ValueError('Token not found in token.txt')
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
