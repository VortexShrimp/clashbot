import discord
from discord.ext import commands

class ModeratorCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(name='kick')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        if reason is None:
            await ctx.send(f'User {member} has been kicked.')
        else:
            await ctx.send(f'User {member} has been kicked for {reason}.')

    @commands.command(name='ban')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        if reason is None:
            await ctx.send(f'User {member} has been banned.')
        else:
            await ctx.send(f'User {member} has been banned for {reason}.')

    @commands.command(name='say')
    @commands.has_permissions(administrator=True)
    async def say(self, ctx: commands.Context, *, message: str):
        await ctx.send(message)

    @commands.command(name='purge')
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx: commands.Context, amount: int):
        if amount < 1:
            response: discord.Message = await ctx.reply("Please specify a number greater than 0.")
            await response.delete(delay=3)
            return
        
        if isinstance(ctx.channel, discord.TextChannel):
            await ctx.channel.purge(limit=amount)
            # Send a confirmation and delete it after a small delay.
            confirmation: discord.Message = await ctx.send(f"Deleted {amount} messages.")
            await confirmation.delete(delay=3)
        else:
            response: discord.Message = await ctx.reply("This command can only be used in server text channels.")
            await response.delete(delay=3)

    @kick.error
    @ban.error
    @say.error
    @purge.error
    async def handle_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            message = 'You do not have the required permissions to use this command.'
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f'Missing required argument for this command.\n`{error.param}`'
        else:
            message = f'{error}'

        embed = discord.Embed(colour=discord.Colour.red(),
                              title='Error',
                              description=message)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ModeratorCog(bot))
