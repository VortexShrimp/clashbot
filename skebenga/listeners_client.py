"""
Module that holds all the general client listeners for the bot.
"""

import coc
import discord
import globals
import utilities
import datetime

@coc.ClientEvents.maintenance_start()
async def on_maintenance_start() -> None:
    print('[debug] on_maintenance_start called')

    embed = discord.Embed(colour=discord.Colour.red(),
                          title='Maintenance Started',
                          description='Maintenance is currently underway.')

    await utilities.send_embed_via_webhook(globals.DISCORD_GENERAL_WEBHOOK, embed)

@coc.ClientEvents.maintenance_end()
async def on_maintenance_completion(start_time: datetime.datetime) -> None:
    print('[debug] on_maintenance_end called')

    duration: datetime.timedelta = datetime.datetime.now() - start_time
    embed = discord.Embed(colour=discord.Colour.green(),
                          title='Maintenance Ended',
                          description=f'Maintenance has ended after {duration}.')

    await utilities.send_embed_via_webhook(globals.DISCORD_GENERAL_WEBHOOK, embed)

@coc.ClientEvents.clan_games_start()
async def on_clan_games_start() -> None:
    print('[debug] on_clan_games_start called')

    embed = discord.Embed(colour=discord.Colour.blue(),
                          title='Clan Games Started',
                          description='Participate to earn rewards.')

    await utilities.send_embed_via_webhook(globals.DISCORD_GENERAL_WEBHOOK, embed)

@coc.ClientEvents.clan_games_end()
async def on_clan_games_end() -> None:
    print('[debug] on_clan_games_end called')

    embed = discord.Embed(colour=discord.Colour.blue(),
                          title='Clan Games Ended',
                          description='Check your rewards.')

    await utilities.send_embed_via_webhook(globals.DISCORD_GENERAL_WEBHOOK, embed)

@coc.ClientEvents.raid_weekend_start()
async def on_raid_weekend_start() -> None:
    print('[debug] on_raid_weekend_start called')
    embed = discord.Embed(colour=discord.Colour.purple(),
                          title='Raid Weekend Started',
                          description='Participate to earn loot and glory.')

    await utilities.send_embed_via_webhook(globals.DISCORD_GENERAL_WEBHOOK, embed)

@coc.ClientEvents.raid_weekend_end()
async def on_raid_weekend_end() -> None:
    print('[debug] on_raid_weekend_end called')

    embed = discord.Embed(colour=discord.Colour.purple(),
                          title='Raid Weekend Ended',
                          description='Check your loot and glory earned.')

    await utilities.send_embed_via_webhook(globals.DISCORD_GENERAL_WEBHOOK, embed)
