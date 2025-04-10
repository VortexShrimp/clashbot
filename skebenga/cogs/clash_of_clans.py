import discord
from discord.ext import commands

import coc

# So that we can access the CoC fields.
from main import SkebengaBot

class ClashOfClansCog(commands.Cog):
    def __init__(self, bot : SkebengaBot):
        self.bot : SkebengaBot = bot

    @commands.command(name='player_info')
    async def player_info(self, ctx : commands.Context, player_tag : str):
        # Make sure the player's tag is valid.
        if not coc.utils.is_valid_tag(player_tag):
            await ctx.send('Invalid player tag format provided.')
            return
        
        # Attempt to get the player.
        try:
            player : coc.Player = await self.bot.coc_client.get_player(player_tag)
        except coc.NotFound:
            await ctx("This player does not exist.")
            return
        
        frame = ""

        if player.town_hall > 11:
            frame += f'`{'TH Weapon Level:':<20}` `{player.town_hall_weapon:<20}`\n'

        role = player.role if player.role else 'None'
        clan = player.clan.name if player.clan else 'None'

        frame += (
            f'`{'Name:':<20}` `{player.name:<20}`\n'
            f'`{'Role:':<20}` `{role:<20}`\n'
            f'`{'Player Tag:':<20}` `{player.tag:<20}`\n'
            f'`{'Current Clan:':<20}` `{clan:<20.20}`\n'
            f'`{'League:':<20}` `{player.league.name:<20.20}`\n'
            f'`{'Trophies:':<20}` `{player.trophies:<20}`\n'
            f'`{'Best Trophies:':<20}` `{player.best_trophies:<20}`\n'
            f'`{'War Stars:':<20}` `{player.war_stars:<20}`\n'
            f'`{'Attack Wins:':<20}` `{player.attack_wins:<20}`\n'
            f'`{'Defense Wins:':<20}` `{player.defense_wins:<20}`\n'
            f'`{'Capital Contribution':<20}` `{player.clan_capital_contributions:<20}`\n'
        )

        embed = discord.Embed(colour=discord.Colour.yellow(), description=frame, title=f'Player Info')
        embed.set_thumbnail(url=player.clan.badge.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ClashOfClansCog(bot))
