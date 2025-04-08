import discord
from discord.ext import commands

import coc
import os
import dotenv

# Load the .env file that holds the tokens.
dotenv.load_dotenv()

# Get our token from the .env file.
TOKEN_DISCORD : str = os.getenv('TOKEN_DISCORD')
TOKEN_COC = os.getenv('TOKEN_COC')

# Create the bot.
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.event
async def on_ready():
    activity = discord.Activity(type = discord.ActivityType.watching, name = "Clash of Clans")
    await bot.change_presence(activity = activity)

@bot.command(name = 'ping')
async def ping(ctx):
    latency : int = round(bot.latency * 1000)  # Convert latency to milliseconds
    await ctx.send(f'Pong! Latency: {latency}ms')

if __name__ == '__main__':
    bot.load_extension('cog_moderator')

    # Run the bot.
    bot.run(token = TOKEN_DISCORD)
