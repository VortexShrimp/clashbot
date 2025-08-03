import discord
from discord.ext import commands

import utilities
from main import ClashBot

class HelpCog(commands.Cog):
    def __init__(self, bot: ClashBot) -> None:
        self.bot: ClashBot = bot

    @commands.command(name='help')
    async def help(self, ctx: commands.Context, *, category_name: str | None = None) -> None:
        """
        Display a list of all available commands and their descriptions.

        If a category name is provided, it will show commands in that category.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
            category_name (str, optional): The name of the category to show commands for.
        """

        # If category_name is not provided, show all categories.
        if category_name is None:
            embed: discord.Embed = discord.Embed(
                title='Help',
                description=f'Use `{self.bot.command_prefix}help <category>` to see category commands.',
                color=utilities.get_bot_guild_role_colour(ctx)
            )

            for cog_name, cog in self.bot.cogs.items():
                # Skip the help cog itself.
                if cog_name == self.__cog_name__:
                    continue

                embed.add_field(
                    name=cog_name[:-3],  # Remove 'Cog' suffix.
                    value=cog.__doc__ or 'No description provided.',
                    inline=False
                )

            await ctx.send(embed=embed)
        else:
            category: commands.Cog | None = None
            cog_full_name: str | None = None

            # Find the cog that matches the category name.
            for cog_name, cog in self.bot.cogs.items():
                if cog_name.lower() == category_name.lower() + 'cog':
                    category = cog
                    cog_full_name = cog_name
                    break
            
            # If the category is not found, send an error message.
            if category is None:
                await ctx.send("Category not found.")
                return

            embed = discord.Embed(
                title=f'Help - {cog_full_name[:-3]}',
                description=f'List of commands in the {category_name} category',
                color=utilities.get_bot_guild_role_colour(ctx)
            )

            for command in category.get_commands():
                embed.add_field(
                    name=command.name,
                    # TODO: Figure out how to get the command description only.
                    value=command.help or 'No description provided.',
                    inline=False
                )

            await ctx.send(embed=embed)

    @help.error
    async def handle_error(ctx: commands.Context, error: commands.CommandError) -> None:
        """
        Handle errors for the help command.
        """

        if isinstance(error, commands.CommandInvokeError):
            print(f'[error] CommandInvokeError in help command: {error}')
            await ctx.send('An error occurred while processing your request. Please try again later.')
        else:
            print(f'[error] Unexpected error in help command: {error}')
            await ctx.send('An unexpected error occurred. Please try again later.')

async def setup(bot: ClashBot):
    await bot.add_cog(HelpCog(bot))
