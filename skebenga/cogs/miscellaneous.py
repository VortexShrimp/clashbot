from discord.ext import commands

class MiscellaneousCog(commands.Cog):
    """
    A cog for miscellaneous commands that don't fit into other categories.
    
    This includes commands like ping, say, and other utility commands.
    """
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context):
        """
        Check the bot's latency.

        This command replies with the current latency of the bot in milliseconds.
        """

        latency: int = round(self.bot.latency * 1000)

        await ctx.reply(content=f'Pong! `{latency}ms`')

    @commands.command(name='say')
    @commands.has_permissions(administrator=True)
    async def say(self, ctx: commands.Context, *, message: str):
        """
        Make the bot say a message.

        This command requires the user to have administrator permissions.

        Args:
            message (str): The message to send.
        """
        await ctx.send(message)

    @say.error
    async def handle_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('You do not have permission to use this command.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f'Missing required argument: {error.param.name}.')
        else:
            await ctx.reply('An error occurred while processing your command.')

async def setup(bot: commands.Bot):
    await bot.add_cog(MiscellaneousCog(bot))
