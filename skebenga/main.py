import discord
from discord.ext import commands

import coc
import os
import dotenv
import asyncio

class SkebengaBot(commands.Bot):
    def __init__(self, coc_client : coc.EventsClient):
        self.coc_client : coc.EventsClient = coc_client
        super().__init__(command_prefix='!', intents=discord.Intents.all())

    # Load all the cogs used in the bot here.
    async def setup_hook(self):
        # Try load all the bot's cogs.
        for file in os.listdir(f'.\skebenga\cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')
                    print(f'Loaded {file} extension')
                except Exception as error:
                    print(f'Failed to load extension {file}')
                    print(f'[error] {error}')

        self.tree.sync()

        # Example discord bot to follow.
        # https://github.com/mathsman5133/coc.py/blob/master/examples/discord_bot_with_cogs.py

    async def on_ready(self):
        print(f'Logged in as {self.user}.')

        activity = discord.Activity(type=discord.ActivityType.watching, name='Clash of Clans')
        await self.change_presence(activity=activity)
        print(f'Presence updated.')

async def main():
    # Get our tokens from the .env file.
    discord_token : str = os.getenv('DISCORD_TOKEN')
    coc_email : str = os.getenv('COC_EMAIL')
    coc_password : str = os.getenv('COC_PASSWORD')

    async with coc.EventsClient() as coc_client:
        # Attempt to log into the CoC API.
        try:
            await coc_client.login(coc_email, coc_password)
        except coc.InvalidCredentials as error:
            print(f'[error] Failed to login to CoC API.')
            exit(error)

        # Run the discord bot.
        bot = SkebengaBot(coc_client=coc_client)
        await bot.start(token=discord_token)

if __name__ == '__main__':
    if dotenv.load_dotenv() == True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            ...
    else:
        print('[error] Failed to load ".env" file.')
