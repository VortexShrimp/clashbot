import listeners

import discord
from discord.ext import commands

import coc
import os
import dotenv
import asyncio

# The main bot class.
class SkebengaBot(commands.Bot):
    def __init__(self, coc_client: coc.EventsClient, coc_clantag: str) -> None:
        self.coc_client: coc.EventsClient = coc_client
        self.coc_clantag: str = coc_clantag

        super().__init__(command_prefix='!', intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await self.setup_cogs()
        await self.setup_coc_api()

    async def on_ready(self) -> None:
        print(f'Logged in as {self.user}.')
        activity = discord.Activity(type=discord.ActivityType.watching, name='Clash of Clans')
        await self.change_presence(activity=activity)

    # Load any cogs found in the cogs directory.
    async def setup_cogs(self) -> None:
        for file in os.listdir(f'./skebenga/cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')
                    print(f'Loaded {file} extension')
                except Exception as error:
                    print(f'[error] Failed to load extension {file}. Error {error}')

    async def setup_coc_api(self) -> None:
        # Example discord bot to follow.
        # https://github.com/mathsman5133/coc.py/blob/master/examples/discord_bot_with_cogs.py
        # https://peps.python.org/pep-0008/

        self.coc_client.add_clan_updates(self.coc_clantag)
        self.coc_client.add_war_updates(self.coc_clantag)

        try:
            clan: coc.Clan = await self.coc_client.get_clan(self.coc_clantag)
            print(f'Tracking {clan.name} with tag {clan.tag}')
        except coc.ClashOfClansException:
            print(f'[error] Failed to start tracking {self.coc_clantag}')

        self.coc_client.add_player_updates(*[member.tag for member in clan.members])

        # Add our custom event listeners.
        self.coc_client.add_events(
            listeners.on_clan_member_join,
            listeners.on_clan_member_leave,
            listeners.on_clan_level_changed,
            listeners.on_clan_description_changed,
            listeners.on_clan_badge_changed,

            listeners.on_new_war,
            listeners.on_war_attack,
            listeners.on_war_state_changed
        )

async def main() -> None:
    # Get our tokens from the .env file.
    discord_token: str = os.getenv('DISCORD_TOKEN')

    coc_email: str = os.getenv('COC_EMAIL')
    coc_password: str = os.getenv('COC_PASSWORD')
    coc_clantag: str = os.getenv('COC_CLANTAG')

    async with coc.EventsClient() as coc_client:
        # Attempt to log into the CoC API.
        try:
            await coc_client.login(coc_email, coc_password)
        except coc.InvalidCredentials as error:
            print(f'[error] Failed to login to CoC API.')
            exit(error)

        # Run the discord bot.
        bot = SkebengaBot(coc_client, coc_clantag)
        await bot.start(discord_token)

if __name__ == '__main__':
    if dotenv.load_dotenv() == True:
        loop = asyncio.new_event_loop()

        try:
            loop.run_until_complete(main())
            loop.run_forever()
        except KeyboardInterrupt:
            ...
    else:
        print('[error] Failed to load ".env" file.')
