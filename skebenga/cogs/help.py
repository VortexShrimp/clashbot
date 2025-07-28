import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(name='help')
    async def help(self, ctx: commands.Context):
        """
        Display a list of all available commands and their descriptions.
        """

        # TODO: Implement a more structured help command.
        # This is a simple implementation that lists all commands in all cogs for later reference.

        help_text = "Here are the available commands:\n\n"

        for cog in self.bot.cogs.values():
            help_text += f"**{cog.__class__.__name__}**\n"
            if hasattr(cog, 'get_commands'):
                for command in cog.get_commands():
                    help_text += f"{command.name}: {command.help}\n"

            help_text += "\n"

        await ctx.send(help_text)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))
