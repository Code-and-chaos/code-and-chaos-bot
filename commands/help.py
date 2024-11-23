import discord
from discord.ext import commands

def setup(bot, logging, audit_log_channel_id):
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