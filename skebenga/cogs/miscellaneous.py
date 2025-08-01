import discord
from discord.ext import commands

class MiscellaneousCog(commands.Cog):
    """
    A cog for miscellaneous commands.
    
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

        latency_milliseconds: int = round(self.bot.latency * 1000)

        await ctx.reply(content=f'Pong! `{latency_milliseconds}ms`')

    @commands.command(name='say')
    @commands.has_permissions(administrator=True)
    async def say(self, ctx: commands.Context, *, message: str):
        """
        Make the bot say a message.

        This command requires the user to have administrator permissions.

        Args:
            message (str): The message to send.
        """

        # Delete the command message.
        await ctx.message.delete()

        # Send the message.
        await ctx.send(message)

    @commands.command(name='reply')
    @commands.has_permissions(administrator=True)
    async def reply(self, ctx: commands.Context, *, message: str):
        """
        Make the bot reply to a message.

        Args:
            message (str): The message to reply with.
        """

        await ctx.reply(content=message)

    @commands.command(name='avatar')
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        """
        Get the avatar URL of a member.

        If no member is specified, it defaults to the command invoker.

        Args:
            member (discord.Member, optional): The member whose avatar URL to retrieve. Defaults to None.
        """

        if member is None:
            member = ctx.author

        avatar: discord.Asset = member.avatar or member.default_avatar

        await ctx.send(avatar.url)

    @say.error
    @reply.error
    @avatar.error
    async def handle_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('You do not have permission to use this command.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f'Missing required argument: {error.param.name}.')
        else:
            await ctx.reply('An error occurred while processing your command.')

async def setup(bot: commands.Bot):
    await bot.add_cog(MiscellaneousCog(bot))
