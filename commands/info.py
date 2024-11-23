import discord
import time
calculation_start_time = time.time()

def setup(bot, logging, audit_log_channel_id):
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
            name="Developers:",
            value="<@520872721060462592> [Github](https://github.com/QuietTerminalInteractive)\n<@512988669561274400> [Github](https://github.com/Minecrafter8001)",
            inline=False
        )

        embed.add_field(
            name="Source code:",
            value="https://github.com/Code-and-chaos/code-and-chaos-bot",
            inline=False
        )

        embed.add_field(
            name="Total users:",
            value=str(sum(guild.member_count for guild in bot.guilds)),
            inline=True
        )
        embed.set_footer(
            text='Use "/help" to see a list of all available commands.',
        )

        await interaction.response.send_message(embed=embed)

