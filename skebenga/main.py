import discord
from discord.ext import commands

import coc
import os
import dotenv
import asyncio

class SkebengaBot(commands.Bot):
    def __init__(self, coc_client : coc.EventsClient, coc_clantag : str):
        self.coc_client : coc.EventsClient = coc_client
        self.coc_clantag : str = coc_clantag

        super().__init__(command_prefix='!', intents=discord.Intents.all())

    # Load all the cogs used in the bot here.
    async def setup_hook(self):
        # Try load all the bot's cogs.
        for file in os.listdir(f'./skebenga/cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')
                    print(f'Loaded {file} extension')
                except Exception as error:
                    print(f'Failed to load extension {file}')
                    print(f'[error] {error}')

        # Example discord bot to follow.
        # https://github.com/mathsman5133/coc.py/blob/master/examples/discord_bot_with_cogs.py

        # Start tracking your clan.
        self.coc_client.add_clan_updates(self.coc_clantag)

        try:
            clan : coc.Clan = await self.coc_client.get_clan(self.coc_clantag)
            print(f'Tracking {clan.name} with tag {clan.tag}')
        except:
            print(f'[error] Failed to start tracking {self.coc_clantag}')

        self.coc_client.add_player_updates(*[member.tag for member in clan.members])

        # Add our custom event listeners.
        self.coc_client.add_events(
            on_clan_member_join,
            on_clan_member_leave,
            on_member_sent_donation,
            on_member_recieved_donation
        )

    async def on_ready(self):
        print(f'Logged in as {self.user}.')

        activity = discord.Activity(type=discord.ActivityType.watching, name='Clash of Clans')
        await self.change_presence(activity=activity)
        print(f'Presence updated.')

@coc.ClanEvents.member_join()
async def on_clan_member_join(old_member : coc.ClanMember, new_member : coc.ClanMember):
    print(f'Player {old_member.name}{old_member.tag} just joined {new_member.clan.name}')

@coc.ClanEvents.member_leave()
async def on_clan_member_leave(old_member : coc.ClanMember, new_member : coc.ClanMember):
    print(f'Player {new_member.name}{new_member.tag} just left {old_member.clan.name}')

@coc.ClanEvents.member_donations()
async def on_member_sent_donation(old_member : coc.ClanMember, new_member : coc.ClanMember):
    sent_troop_count : int = new_member.donations - old_member.donations
    print(f'Player {new_member.name}{new_member.tag} just sent {sent_troop_count} troops.')

@coc.ClanEvents.member_received()
async def on_member_recieved_donation(old_member : coc.ClanMember, new_member : coc.ClanMember):
    recieved_troop_count : int = new_member.received - old_member.received
    print(f'Player {new_member.name}{new_member.tag} just received {recieved_troop_count} troops.')

async def main():
    # Get our tokens from the .env file.
    discord_token : str = os.getenv('DISCORD_TOKEN')

    coc_email : str = os.getenv('COC_EMAIL')
    coc_password : str = os.getenv('COC_PASSWORD')
    coc_clantag : str = os.getenv('COC_CLANTAG')

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
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            ...
    else:
        print('[error] Failed to load ".env" file.')
