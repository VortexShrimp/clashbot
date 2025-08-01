import discord
import aiohttp

async def send_embed_via_webhook(webhook_url: str, embed: discord.Embed) -> None:
    """
    Send an embed message via a Discord webhook.

    Args:
        webhook_url (str): The URL of the Discord webhook.
        embed (discord.Embed): The embed message to send.
    """

    async with aiohttp.ClientSession() as session:
        webhook: discord.Webhook = discord.Webhook.from_url(webhook_url, session=session)
        await webhook.send(embed=embed)
