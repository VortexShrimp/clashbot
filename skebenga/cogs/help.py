import discord
from discord.ext import commands

import utilities
from main import ClashBot

class HelpCog(commands.Cog):
    def __init__(self, bot: ClashBot):
        self.bot: ClashBot = bot

    @commands.command(name='help')
    async def help(self, ctx: commands.Context):
        """
        Display a list of all available commands and their descriptions.
        """

        print(f"[info] Help command invoked by {ctx.author} in guild {ctx.guild.name if ctx.guild else 'DM'}")

        # TODO: Implement a more structured help command.
        # This is a simple implementation that lists all commands in all cogs for later reference.

        colour: discord.Color = utilities.get_bot_guild_role_colour(ctx)

        embed: discord.Embed = discord.Embed(
            title='Help',
            description='List of available commands',
            color=colour
        )

        # help_text = "Here are the available commands:\n\n"

        # for cog in self.bot.cogs.values():
            # help_text += f"**{cog.__class__.__name__}**\n"
            # if hasattr(cog, 'get_commands'):
                # for command in cog.get_commands():
                    # help_text += f"{command.name}: {command.help}\n"

            # help_text += "\n"

        await ctx.send(embed=embed)

    @help.error
    async def handle_error(ctx: commands.Context, error: commands.CommandError):
        """
        Handle errors for the help command.
        """

        if isinstance(error, commands.CommandInvokeError):
            print(f"[error] CommandInvokeError in help command: {error}")
            await ctx.send("An error occurred while processing your request. Please try again later.")
        else:
            print(f"[error] Unexpected error in help command: {error}")
            await ctx.send("An unexpected error occurred. Please try again later.")

async def setup(bot: ClashBot):
    await bot.add_cog(HelpCog(bot))
