import discord
import re

def setup(bot, logging, audit_log_channel_id):
    @bot.tree.command(name="delete", description="Deletes the message with the provided message ID.")
    async def delete(interaction: discord.Interaction, message_id: str, *, hide: bool = False):
        await interaction.response.defer(ephemeral=hide)
        message_id_regex = re.compile(r'^\d{19}$')
        channel_and_message_id_regex = re.compile(r'^\d{19}-\d{19}$')

        if channel_and_message_id_regex.match(message_id):
            await delete_message_with_channel_id(interaction, message_id, hide)
        elif message_id_regex.match(message_id):
            await delete_message(interaction, message_id, hide)
        else:
            await send_error_embed(interaction, message_id, "Invalid message ID.", hide)

    async def delete_message(interaction, message_id, hide):
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            content = message.clean_content
            await message.delete()
            await send_success_embed(interaction, message, message_id, hide, content=content)
        except discord.NotFound:
            await send_error_embed(interaction, message_id, "Message not found.", hide)
        except discord.Forbidden:
            await send_error_embed(interaction, message_id, "Bot has insufficient permissions.", hide)
        except Exception as e:
            logging.error(f"Failed to delete message: {e}")
            await send_error_embed(interaction, message_id, "An unexpected error occurred.", hide)

    async def delete_message_with_channel_id(interaction, message_id, hide):
        channel_id, message_id = message_id.split('-')
        try:
            message = await bot.get_channel(int(channel_id)).fetch_message(int(message_id))
            content = message.clean_content
            await message.delete()
            await send_success_embed(interaction, message, message_id, hide, content, channel_id )
        except discord.NotFound:
            await send_error_embed(interaction, message_id, "Message not found.", hide)
        except discord.Forbidden:
            await send_error_embed(interaction, message_id, "Bot has insufficient permissions.", hide)
        except Exception as e:
            logging.error(f"Failed to delete message: {e}")
            await send_error_embed(interaction, message_id, "An unexpected error occurred.", hide)

    async def send_success_embed(interaction, message, message_id, hide, content, channel_id=None, ):
        embed = discord.Embed(
            title="Message Deleted",
            description=f"{interaction.user.mention} successfully deleted a message.",
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed)

        embed = discord.Embed(
            title="Command Executed: /delete",
            description=f"{interaction.user.mention} ran /delete command at {interaction.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Content", value=content, inline=False)
        embed.add_field(name="User", value=message.author.mention, inline=True)
        embed.add_field(name="Invoker", value=interaction.user.mention, inline=True)
        embed.add_field(name="Executed in", value=f"<#{interaction.channel.id}>", inline=True)
        embed.add_field(name="hidden", value=hide, inline=True)
        await bot.get_channel(audit_log_channel_id).send(embed=embed)

    async def send_error_embed(interaction, message_id, error_message, hide):
        embed = discord.Embed(
            title="Error",
            description=error_message,
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)

        embed = discord.Embed(
            title="Command Failed: /delete",
            description=f"{interaction.user.mention} ran /delete command at {interaction.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            color=discord.Color.red()
        )
        embed.add_field(name="Error", value=error_message, inline=False)
        embed.add_field(name="Message ID", value=message_id, inline=False)
        embed.add_field(name="Executed in", value=f"<#{interaction.channel.id}>", inline=True)
        embed.add_field(name="Invoker", value=interaction.user.mention, inline=True)
        embed.add_field(name="hidden", value=hide, inline=True)
        await bot.get_channel(audit_log_channel_id).send(embed=embed)



