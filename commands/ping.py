import discord
def setup(bot, logging):
    @bot.tree.command(name="ping", description="Pings the bot.")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong")
