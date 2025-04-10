import discord
from discord.ext import commands

class ModeratorCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot

    @commands.command(name='kick')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason = reason)
        await ctx.send(f'User {member} has been kicked for {reason}')

    @commands.command(name='ban')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned for {reason}')

    @commands.command(name='say')
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message):
        await ctx.send(message)

    @kick.error
    @ban.error
    @say.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the required permissions to use this command.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You have not provided a required argument for this command.')
        else:
            await ctx.send('An error occurred while processing the command.')

async def setup(bot):
    await bot.add_cog(ModeratorCog(bot))
