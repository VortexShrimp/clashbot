"""
Global configuration variables for Discord webhooks and Clash of Clans clan tag.

These variables are intended to be set at runtime and used throughout the application.
- DISCORD_CLAN_WEBHOOK: Webhook URL for clan notifications.
- DISCORD_WAR_WEBHOOK: Webhook URL for war notifications.
- DISCORD_DONATIONS_WEBHOOK: Webhook URL for donation notifications.
- COC_CLANTAG: Clash of Clans clan tag.
"""

DISCORD_CLAN_WEBHOOK: str | None = None
DISCORD_WAR_WEBHOOK: str | None = None
DISCORD_DONATIONS_WEBHOOK: str | None = None

COC_CLANTAG: str | None = None
