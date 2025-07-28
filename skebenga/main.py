import discord
from discord.ext import commands

import coc
import os
import dotenv
import asyncio

import globals
import listeners_clan
import listeners_client
import listeners_war

class ClashBot(commands.Bot):
    def __init__(self, coc_client: coc.EventsClient, coc_clantag: str) -> None:
        self.coc_client: coc.EventsClient = coc_client
        self.coc_clantag: str = coc_clantag

        super().__init__(command_prefix='!', intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await self.setup_cogs()
        await self.setup_coc_api()

    async def on_ready(self) -> None:
        print(f'[info] Logged in as {self.user}.')
        activity: discord.Activity = discord.Activity(type=discord.ActivityType.watching, name='Clash of Clans')
        await self.change_presence(activity=activity)

    # Load any cogs found in the cogs directory.
    async def setup_cogs(self) -> None:
        for file in os.listdir(f'./skebenga/cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')
                    print(f'[info] Loaded {file} extension.')
                except Exception as error:
                    print(f'[error] Failed to load extension {file}. Error {error}.')

    async def setup_coc_api(self) -> None:
        self.coc_client.add_clan_updates(self.coc_clantag)
        self.coc_client.add_war_updates(self.coc_clantag)

        try:
            clan: coc.Clan = await self.coc_client.get_clan(self.coc_clantag)
            print(f'[info] Tracking {clan.name}{clan.tag} clan.')
            
            # Start tracking all members of the clan.
            self.coc_client.add_player_updates(*[member.tag for member in clan.members])
        except coc.ClashOfClansException:
            print(f'[error] Failed to start tracking {self.coc_clantag}')

        # Register our custom event listeners.
        self.coc_client.add_events(
            # Clan Events
            listeners_clan.on_member_join,
            listeners_clan.on_member_leave,
            listeners_clan.on_level,
            listeners_clan.on_description,
            listeners_clan.on_badge,
            listeners_clan.on_member_role,
            listeners_clan.on_member_donations_sent,
            listeners_clan.on_member_donations_received,

            # Client Events
            listeners_client.on_maintenance_start,
            listeners_client.on_maintenance_completion,
            listeners_client.on_clan_games_start,
            listeners_client.on_clan_games_end,
            listeners_client.on_raid_weekend_start,
            listeners_client.on_raid_weekend_end,

            # War Events
            listeners_war.on_attack,
            listeners_war.on_state,
            listeners_war.on_new_war,
        )

async def main() -> None:
    discord_token: str | None = os.getenv('DISCORD_TOKEN')
    if discord_token is None:
        raise ValueError('[error] DISCORD_TOKEN not found in .env file.')

    coc_email: str | None = os.getenv('COC_EMAIL')
    if coc_email is None:
        raise ValueError('[error] COC_EMAIL not found in .env file.')

    coc_password: str | None = os.getenv('COC_PASSWORD')
    if coc_password is None:
        raise ValueError('[error] COC_PASSWORD not found in .env file.')

    # Make sure the clan tag is provided and valid.
    globals.COC_CLANTAG = os.getenv('COC_CLAN_TAG')
    if globals.COC_CLANTAG is None:
        raise ValueError('[error] COC_CLAN_TAG not found in .env file.')

    if not coc.utils.is_valid_tag(globals.COC_CLANTAG):
        raise ValueError(f'[error] Invalid clan tag format provided: {globals.COC_CLANTAG}')

    globals.DISCORD_CLAN_WEBHOOK = os.getenv('DISCORD_CLAN_WEBHOOK')
    if globals.DISCORD_CLAN_WEBHOOK is None:
        raise ValueError('[error] DISCORD_CLAN_WEBHOOK not found in .env file. Clan events will not be sent to Discord.')

    globals.DISCORD_WAR_WEBHOOK = os.getenv('DISCORD_WAR_WEBHOOK')
    if globals.DISCORD_WAR_WEBHOOK is None:
        raise ValueError('[error] DISCORD_WAR_WEBHOOK not found in .env file. War events will not be sent to Discord.')

    globals.DISCORD_DONATIONS_WEBHOOK = os.getenv('DISCORD_DONATIONS_WEBHOOK')
    if globals.DISCORD_DONATIONS_WEBHOOK is None:
        raise ValueError('[error] DISCORD_DONATIONS_WEBHOOK not found in .env file. Donations will not be sent to Discord.')

    globals.DISCORD_GENERAL_WEBHOOK = os.getenv('DISCORD_GENERAL_WEBHOOK')
    if globals.DISCORD_GENERAL_WEBHOOK is None:
        raise ValueError('[error] DISCORD_GENERAL_WEBHOOK not found in .env file. General events will not be sent to Discord.')

    async with coc.EventsClient() as coc_client:
        # Attempt to log into the CoC API.
        try:
            await coc_client.login(coc_email, coc_password)
        except coc.InvalidCredentials as error:
            print(f'[error] Failed to login to CoC API. Error: {error}')
            return

        bot = ClashBot(coc_client, globals.COC_CLANTAG)

        # Run the bot.
        await bot.start(discord_token)

if __name__ == '__main__':
    # Search for a .env file in the current directory.
    if dotenv.load_dotenv() == True:
        loop = asyncio.new_event_loop()

        try:
            loop.run_until_complete(main())
            loop.run_forever()
        except (KeyboardInterrupt, ValueError) as error:
            print(error)
    # If the .env file does not exist, create one.
    else:
        print('[error] Failed to load ".env" file. Creating one for you. Please fill it out before running the bot again.')

        # Create a new .env file with the required fields.
        with open('.env', 'w') as env_file:
            env_file.write(
                'DISCORD_TOKEN=\n'

                'DISCORD_CLAN_WEBHOOK=\n'
                'DISCORD_WAR_WEBHOOK=\n'
                'DISCORD_DONATIONS_WEBHOOK=\n'
                'DISCORD_GENERAL_WEBHOOK=\n'

                'COC_EMAIL=\n'
                'COC_PASSWORD=\n'

                'COC_CLAN_TAG=\n'
            )
