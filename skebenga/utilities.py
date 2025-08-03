import discord
from discord.ext import commands

import aiohttp

async def send_embed_via_webhook_url(webhook_url: str, embed: discord.Embed) -> None:
    """
    Send an embed message via a Discord webhook.

    Args:
        webhook_url (str): The URL of the Discord webhook.
        embed (discord.Embed): The embed message to send.
    """

    async with aiohttp.ClientSession() as session:
        webhook: discord.Webhook = discord.Webhook.from_url(webhook_url, session=session)
        
        await webhook.send(embed=embed)

def get_bot_guild_role_colour(ctx: commands.Context) -> discord.Colour:
    """
    Get the bot's role colour in the server.

    Args:
        ctx (discord.Context): The context from which to get the guild.

    Returns:
        discord.Colour: The color of bot in the guild. If the bot is not in a guild, returns the default color.
    """

    guild: discord.Guild | None = ctx.guild
    if guild is None:
        return discord.Color.default()

    bot: discord.Member | None = guild.me
    if bot is None:
        return discord.Color.default()

    return bot.colour

def error_embed(message: str) -> discord.Embed:
    """
    Create a red embed with title 'Error' and a given message.

    Args:
        message (str): The error message to include in the embed.

    Returns:
        discord.Embed: An embed with a default error message.
    """

    return discord.Embed(colour=discord.Colour.red(),
                         title='Error',
                         description=message)
