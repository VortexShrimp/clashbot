"""
Module that holds all the general client listeners for the bot.
"""

import coc
import discord
import globals
import datetime

@coc.ClientEvents.maintenance_start()
async def on_maintenance_start() -> None:
    print('[debug] on_maintenance_start called')

@coc.ClientEvents.maintenance_end()
async def on_maintenance_completion(start_time: datetime.datetime) -> None:
    print('[debug] on_maintenance_end called')

@coc.ClientEvents.clan_games_start()
async def on_clan_games_start() -> None:
    print('[debug] on_clan_games_start called')

@coc.ClientEvents.clan_games_end()
async def on_clan_games_end() -> None:
    print('[debug] on_clan_games_end called')

@coc.ClientEvents.raid_weekend_start()
async def on_raid_weekend_start() -> None:
    print('[debug] on_raid_weekend_start called')

@coc.ClientEvents.raid_weekend_end()
async def on_raid_weekend_end() -> None:
    print('[debug] on_raid_weekend_end called')
