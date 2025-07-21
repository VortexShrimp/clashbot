import discord
from discord.ext import commands

import coc

from main import ClashBot

class ClashOfClansCog(commands.Cog):
    def __init__(self, bot: ClashBot) -> None:
        self.bot: ClashBot = bot

    @commands.command(name='player_info')
    async def player_info(self, ctx: commands.Context, player_tag: str) -> None:
        # Make sure the player's tag is valid.
        if not coc.utils.is_valid_tag(player_tag):
            embed = discord.Embed(colour=discord.Colour.red(), title=f'Error', description='Invalid player tag format provided.')
            await ctx.send(embed=embed)
            return
        
        # Attempt to get the player.
        try:
            player: coc.Player = await self.bot.coc_client.get_player(player_tag)
        except coc.NotFound:
            embed = discord.Embed(colour=discord.Colour.red(), title=f'Error', description='Unable to get the desired player.')
            await ctx.send(embed=embed)
            return
        
        frame = ''

        frame += f'`{'TH Level:':<20}` `{player.town_hall:<20}`\n'
        if player.town_hall > 11:
            frame += f'`{'TH Weapon Level:':<20}` `{player.town_hall_weapon:<20}`\n'

        role: str = str(player.role) if player.role else 'None'
        clan : str = player.clan.name if player.clan else 'None'
        league : str = player.league.name if player.league else 'None'

        frame += (
            f'`{'Name:':<20}` `{player.name:<20}`\n'
            f'`{'Role:':<20}` `{role:<20}`\n'
            f'`{'Player Tag:':<20}` `{player.tag:<20}`\n'
            f'`{'Current Clan:':<20}` `{clan:<20.20}`\n'
            f'`{'League:':<20}` `{league:<20.20}`\n'
            f'`{'Trophies:':<20}` `{player.trophies:<20}`\n'
            f'`{'Best Trophies:':<20}` `{player.best_trophies:<20}`\n'
            f'`{'War Stars:':<20}` `{player.war_stars:<20}`\n'
            f'`{'Attack Wins:':<20}` `{player.attack_wins:<20}`\n'
            f'`{'Defense Wins:':<20}` `{player.defense_wins:<20}`\n'
            f'`{'Capital Contribution':<20}` `{player.clan_capital_contributions:<20}`\n'
        )

        embed = discord.Embed(colour=discord.Colour.yellow(), title=f'Player Info', description=frame)
        embed.set_thumbnail(url=player.clan.badge.url)

        await ctx.send(embed=embed)

    @commands.command(name='clan_members')
    async def clan_members(self, ctx: commands.Context, clan_tag: str = "default") -> None:
        # If no clan tag is provided, use the tag found in the .env file.
        desired_clan_tag: str = self.bot.coc_clantag if clan_tag == "default" else clan_tag

        # Make sure the clan's tag is valid.
        if coc.utils.is_valid_tag(desired_clan_tag) == False:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Invalid clan tag format provided. `{desired_clan_tag}`')
            await ctx.send(embed=embed)
            return

        # Attempt to get the clan.
        try:
            clan: coc.Clan = await self.bot.coc_client.get_clan(desired_clan_tag)
        except coc.NotFound:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Unable to get the desired clan with tag `{desired_clan_tag}`.')
            await ctx.send(embed=embed)
            return
        except coc.GatewayError:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Unexpected gateway error.')
            await ctx.send(embed=embed)
            return

        frame: str = f'{clan.name} ({clan.tag}) has [{clan.member_count}/50] members.\n\n'
        number: int = 1

        for member in clan.members:
            frame += (f'`{f'{number}. {member.name}':<20}` 'f'`{member.tag:<15}`\n')
            number = number + 1

        embed = discord.Embed(colour=discord.Colour.yellow(), title='Clan Members', description=frame)
        if clan.badge is not None and hasattr(clan.badge, "url"):
            embed.set_thumbnail(url=clan.badge.url)

        await ctx.send(embed=embed)

    @commands.command(name='clan_info')
    async def clan_info(self, ctx: commands.Context, clan_tag: str = "default") -> None:
        # If no clan tag is provided, use the tag found in the .env file.
        desired_clan_tag : str = self.bot.coc_clantag if clan_tag == "default" else clan_tag

        # Make sure the clan's tag is valid.
        if not coc.utils.is_valid_tag(desired_clan_tag):
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Invalid clan tag format provided. `{desired_clan_tag}`')
            await ctx.send(embed=embed)
            return

        # Attempt to get the clan.
        try:
            clan: coc.Clan = await self.bot.coc_client.get_clan(desired_clan_tag)
        except coc.NotFound:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Unable to get the desired clan with tag `{desired_clan_tag}`.')
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(colour=discord.Colour.yellow(), title='Clan Info')
        if clan.badge is not None and hasattr(clan.badge, "url"):
            embed.set_thumbnail(url=clan.badge.url)

        embed.add_field(name='Name',
                    value=f'{clan.name} ({clan.tag})\n[Open in game]({clan.share_link})',
                    inline=False)

        embed.add_field(name='Level',
                    value=clan.level,
                    inline=False)

        embed.add_field(name='Description',
                    value=clan.description,
                    inline=False)

        leader: coc.ClanMember | None = clan.get_member_by(role=coc.Role.leader)
        embed.add_field(name='Leader',
                    value=f'{leader.name} ({leader.tag})' if leader else 'None',
                    inline=False)     

        embed.add_field(name='Clan Type',
                    value=clan.type,
                    inline=False)

        embed.add_field(name='Location',
                    value=clan.location,
                    inline=False)

        embed.add_field(name='Total Clan Trophies',
                    value=clan.points,
                    inline=False)

        embed.add_field(name='Total Clan Builder Base Trophies',
                    value=clan.builder_base_points,
                    inline=False)

        embed.add_field(name='War Log',
                    value='Private' if clan.public_war_log == False else 'Public',
                    inline=False)

        embed.add_field(name='Required Trophies',
                    value=clan.required_trophies,
                    inline=False)
        
        embed.add_field(name='Required Builder Base Trophies',
                    value=clan.required_builder_base_trophies,
                    inline=False)
        
        embed.add_field(name='Required Townhall',
                    value=clan.required_townhall,
                    inline=False)

        embed.add_field(name='War Win Streak',
                    value=clan.war_win_streak,
                    inline=False)

        embed.add_field(name='War Frequency',
                    value=clan.war_frequency,
                    inline=False)

        embed.add_field(name='Clan War League Rank',
                    value=clan.war_league,
                    inline=False)

        embed.add_field(name='Clan Labels',
                    value='\n'.join(label.name for label in clan.labels),
                    inline=False)

        embed.add_field(name='Member Count',
                    value=f'{clan.member_count}/50',
                    inline=False)

        embed.add_field(
            name='Clan Record',
            value=f'Won - {clan.war_wins}\nLost - {clan.war_losses}\n'
                  f'Draw - {clan.war_ties}',
            inline=False
        )

        # If the the clan has districts info, add it to the embed.
        if clan.capital_districts:
            frame: str = ''

            for district in clan.capital_districts:
                frame += (f'`{f'{district.name}:':<20}` 'f'`{district.hall_level:<15}`\n')

            embed.add_field(name='Capital District',
                            value=frame,
                            inline=False)

        await ctx.send(embed=embed)

    @player_info.error
    @clan_info.error
    @clan_members.error
    async def handle_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            message = f'Missing required argument for this command.\n`{error.param}`'
        else:
            message = f'{error}'

        embed = discord.Embed(colour=discord.Colour.red(),
                              title='Error',
                              description=message)
        await ctx.send(embed=embed)

async def setup(bot: ClashBot):
    await bot.add_cog(ClashOfClansCog(bot))
