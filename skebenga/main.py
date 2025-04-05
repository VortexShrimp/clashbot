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
bot = commands.Bot(command_prefix = '!', intents = discord.Intents.default())

# Run the bot.
if __name__ == '__main__':
    bot.run(token = TOKEN_DISCORD)
