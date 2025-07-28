"""
Global configuration variables for Discord webhooks and Clash of Clans clan tag.

These variables are intended to be set at runtime and used throughout the application.
- DISCORD_CLAN_WEBHOOK: Webhook URL for clan notifications.
- DISCORD_WAR_WEBHOOK: Webhook URL for war notifications.
- DISCORD_DONATIONS_WEBHOOK: Webhook URL for donation notifications.
- COC_CLANTAG: Clash of Clans clan tag.
"""

import discord
import aiohttp

DISCORD_CLAN_WEBHOOK: str | None = None
DISCORD_WAR_WEBHOOK: str | None = None
DISCORD_DONATIONS_WEBHOOK: str | None = None
DISCORD_GENERAL_WEBHOOK: str | None = None

COC_CLANTAG: str | None = None

# TODO: Move this to a separate utility module instead of globals.
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
