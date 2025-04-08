import discord
from discord.ext import commands, tasks

import coc
import os
import dotenv

class SkebengaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.load_extension('cog_moderator')

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        activity = discord.Activity(type=discord.ActivityType.watching, name='Clash of Clans')
        await self.change_presence(activity=activity)

    #TODO: Move this into some sort of misc cog?
    #@commands.command()
    #async def ping(self, ctx : commands.Context):
        #latency : int = round(self.latency * 1000)
        #await ctx.send(content=f'Pong! Latency: {latency}ms')

if __name__ == '__main__':
    if dotenv.load_dotenv() == True:
        # Get our tokens from the .env file.
        discord_token : str = os.getenv('TOKEN_DISCORD')
        coc_token : str = os.getenv('TOKEN_COC')

        bot = SkebengaBot()
        bot.run(discord_token)
