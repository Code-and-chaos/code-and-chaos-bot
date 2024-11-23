import discord
def setup(bot, logging, audit_log_channel_id):
    @bot.tree.command(name="ping", description="Pings the bot.")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong")
