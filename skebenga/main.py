import discord
from discord.ext import commands

import coc
import os
import dotenv

class SkebengaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        intents.guild_reactions = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup(self):
        await self.wait_until_ready()
        await self.tree.sync()

    # Load all the cogs used in the bot here.
    async def setup_hook(self):
        for file in os.listdir(f'.\skebenga\cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')
                    print(f'Loaded {file} extension')
                except Exception as error:
                    print(f'Failed to load extension {file}')
                    print(f'[Error] {error}')

        # Run the setup task.          
        self.loop.create_task(self.setup())

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        activity = discord.Activity(type=discord.ActivityType.watching, name='Clash of Clans')
        await self.change_presence(activity=activity)

if __name__ == '__main__':
    if dotenv.load_dotenv() == True:
        # Get our tokens from the .env file.
        discord_token : str = os.getenv('TOKEN_DISCORD')
        coc_token : str = os.getenv('TOKEN_COC')

        bot = SkebengaBot()
        bot.run(discord_token)
