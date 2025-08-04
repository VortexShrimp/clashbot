import discord
from discord.ext import commands

import utilities

class ModeratorCog(commands.Cog):
    """
    Standard server moderation tools that require administrator permissions.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name='kick', brief='Kick a member from the server.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str | None = None) -> None:
        """
        Kick a member from the server.

        Args:
            member (discord.Member): The member to kick.
            reason (str, optional): The reason for the kick.
        """

        await member.kick(reason=reason)

        if reason is None:
            await ctx.send(f'User {member} has been kicked.')
        else:
            await ctx.send(f'User {member} has been kicked for {reason}.')

    @commands.command(name='ban', brief='Ban a member from the server.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str | None = None) -> None:
        """
        Ban a member from the server.

        Args:
            member (discord.Member): The member to ban.
            reason (str, optional): The reason for the ban.
        """

        await member.ban(reason=reason)

        if reason is None:
            await ctx.send(f'User {member} has been banned.')
        else:
            await ctx.send(f'User {member} has been banned for: {reason}.')

    @commands.command(name='purge', brief='Purge a specified number of messages from the channel.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def purge(self, ctx: commands.Context, amount: int) -> None:
        """
        Purge a specified number of messages from the channel.

        Args:
            amount (int): The number of messages to delete.
        """

        if amount < 1:
            response: discord.Message = await ctx.reply('Please specify a number greater than 0.')
            await response.delete(delay=5)
            return
        
        await ctx.channel.purge(limit=amount)

        # Send a confirmation and delete it after a small delay.
        confirmation: discord.Message = await ctx.send(f'Deleted {amount} messages.')
        await confirmation.delete(delay=5)

    @kick.error
    @ban.error
    @purge.error
    async def handle_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingPermissions):
            message: str = 'You do not have permission to use this command.'
        elif isinstance(error, commands.MissingRequiredArgument):
            message: str = f'Missing required argument: {error.param.name}.'
        else:
            message: str = f'An unknown error occurred while processing your command: {str(error)}.'

        await ctx.reply(embed=utilities.error_embed(message))

async def setup(bot: commands.Bot):
    await bot.add_cog(ModeratorCog(bot))
