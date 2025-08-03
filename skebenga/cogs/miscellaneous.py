import discord
from discord import app_commands
from discord.ext import commands

import utilities

class MiscellaneousCog(commands.Cog):
    """
    A collection of random commands for users.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name='ping', brief='Check the bot\'s latency in milliseconds.')
    async def ping(self, ctx: commands.Context) -> None:
        """
        Check the bot's latency in milliseconds.
        """

        # Calculate the latency in milliseconds.
        latency_milliseconds: int = round(self.bot.latency * 1000)
        await ctx.reply(content=f'Pong! `{latency_milliseconds}ms`')

    @app_commands.command(name='ping', description='Check the bot\'s latency in milliseconds.')
    async def ping_interaction(self, interaction: discord.Interaction) -> None:
        """
        Check the bot's latency in milliseconds using an interaction.
        """

        # Calculate the latency in milliseconds.
        latency_milliseconds: int = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'Pong! `{latency_milliseconds}ms`')

    @commands.command(name='say', brief='Make the bot say a message.')
    @commands.has_permissions(administrator=True)
    async def say(self, ctx: commands.Context, *, message: str):
        """
        Make the bot say a message in the channel.

        Args:
            message (str): The message to send.
        """

        # Delete the command message.
        await ctx.message.delete()

        # Send the message.
        await ctx.send(message)

    @commands.command(name='avatar', brief='Get a member\'s avatar.')
    @commands.guild_only()
    async def avatar(self, ctx: commands.Context, member: discord.Member = None) -> None:
        """
        Get a member's avatar URL.

        Args:
            member (discord.Member, optional): The member whose avatar to get. Defaults to the command author.
        """

        if member is None:
            member = ctx.author

        avatar: discord.Asset = member.avatar or member.default_avatar

        await ctx.send(avatar.url)

    @ping.error
    @say.error
    @avatar.error
    async def handle_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed=utilities.error_embed('You do not have permission to use this command.'))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(embed=utilities.error_embed(f'Missing required argument: {error.param.name}.'))
        else:
            await ctx.reply(embed=utilities.error_embed('An error occurred while processing your command.'))

async def setup(bot: commands.Bot):
    await bot.add_cog(MiscellaneousCog(bot))
