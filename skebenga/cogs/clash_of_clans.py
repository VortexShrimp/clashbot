import coc
import discord
from discord.ext import commands

from main import ClashBot

class ClashOfClansCog(commands.Cog):
    """
    Clash of Clans related commands.
    """

    def __init__(self, bot: ClashBot) -> None:
        self.bot: ClashBot = bot

    @commands.command(name='player')
    async def player(self, ctx: commands.Context, player_tag: str) -> None:
        # Make sure the player's tag is valid.
        if not coc.utils.is_valid_tag(player_tag):
            embed: discord.Embed = discord.Embed(colour=discord.Colour.red(), title=f'Error', description='The tag that you provided has an invalid format.')
            await ctx.reply(embed=embed)
            return
        
        # Attempt to get the player.
        try:
            player: coc.Player = await self.bot.coc_client.get_player(player_tag)
        except coc.NotFound:
            embed: discord.Embed = discord.Embed(colour=discord.Colour.red(), title=f'Error', description=f'Unable to find the player with the provided tag ({player_tag}).')
            await ctx.reply(embed=embed)
            return
        except coc.Maintenance:
            embed: discord.Embed = discord.Embed(colour=discord.Colour.red(), title=f'Error', description='The Clash of Clans API is currently under maintenance.')
            await ctx.reply(embed=embed)
            return
        
        # Create the embed with player information.
        embed: discord.Embed = discord.Embed(colour=discord.Colour.yellow(), title=f'Player Info', description=f'Information for player `{player.name} ({player.tag})`')

        player_clan: coc.Clan | None = player.clan
        if player_clan is not None and hasattr(player_clan, "badge") and player_clan.badge is not None:
            # If the player has a clan, set the thumbnail to the clan's badge.
            embed.set_thumbnail(url=player_clan.badge.url)

            # Add clan information to the embed.
            embed.add_field(name='Clan',
                            value=f'{player_clan.name} ({player_clan.tag})\n'
                            f'Role: {player.role.in_game_name}\n'
                            f'Capital Contribution: {player.clan_capital_contributions}\n'
                            f'[Open in game]({player_clan.share_link})',
                            inline=False)
            
        embed.add_field(name='Home Base',
                        value=f'Town Hall Level: {player.town_hall}\n'
                        f'{'' if player.town_hall > 11 else 'Town Hall Weapon Level: ' + str(player.town_hall_weapon) + '\n'}'
                        f'Trophies: {player.trophies}\n'
                        f'Best Trophies: {player.best_trophies}\n'
                        f'League: {player.league.name}\n',
                        inline=False)
        
            
        embed.add_field(name='Builder Base',
                        value = f'Builder Hall Level: {player.builder_hall}\n'
                                f'Builder Base Trophies: {player.builder_base_trophies}\n'
                                f'Builder Base League: {player.builder_base_league.name}\n',
                        inline=False)
        
        embed.add_field(name='Stats',
                        value=f'Attack Wins: {player.attack_wins}\n'
                              f'Defense Wins: {player.defense_wins}\n'
                              f'War Stars: {player.war_stars}\n',
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='members')
    async def members(self, ctx: commands.Context, clan_tag: str = "default") -> None:
        # If no clan tag is provided, use the tag found in the .env file.
        desired_clan_tag: str = self.bot.coc_clantag if clan_tag == "default" else clan_tag

        # Make sure the clan's tag is valid.
        if not coc.utils.is_valid_tag(desired_clan_tag):
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Invalid clan tag format provided. `{desired_clan_tag}`')
            await ctx.reply(embed=embed)
            return

        # Attempt to get the clan.
        try:
            clan: coc.Clan = await self.bot.coc_client.get_clan(desired_clan_tag)
        except coc.NotFound:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Unable to get the desired clan with tag `{desired_clan_tag}`.')
            await ctx.reply(embed=embed)
            return
        except coc.Maintenance:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description='The Clash of Clans API is currently under maintenance.')
            await ctx.reply(embed=embed)
            return
        except coc.GatewayError:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Unexpected gateway error.')
            await ctx.reply(embed=embed)
            return

        embed: discord.Embed = discord.Embed(colour=discord.Colour.yellow(),
                                             title='Clan Members',
                                        description=f'{clan.name} ({clan.tag})\n'
                                             f'[Open in game]({clan.share_link})')

        frame: str = ''
        number: int = 1

        for member in clan.members:
            frame += (f'`{f'{number}. {member.name}':<20}` 'f'`{member.tag:<15}`\n')
            number = number + 1

        embed.add_field(name='Members',
                        value=frame,
                        inline=False)

        embed.set_footer(text=f'Total Members: {clan.member_count}/50')

        if clan.badge is not None and hasattr(clan.badge, "url"):
            embed.set_thumbnail(url=clan.badge.url)

        await ctx.send(embed=embed)

    @commands.command(name='clan')
    async def clan(self, ctx: commands.Context, clan_tag: str = "default") -> None:
        # If no clan tag is provided, use the tag found in the .env file.
        desired_clan_tag : str = self.bot.coc_clantag if clan_tag == "default" else clan_tag

        # Make sure the clan's tag is valid.
        if not coc.utils.is_valid_tag(desired_clan_tag):
            embed: discord.Embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Invalid clan tag format provided `({desired_clan_tag}).`')
            await ctx.reply(embed=embed)
            return

        # Attempt to get the clan.
        try:
            clan: coc.Clan = await self.bot.coc_client.get_clan(desired_clan_tag)
        except coc.NotFound:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description=f'Unable to get the desired clan with tag `({desired_clan_tag})`.')
            await ctx.reply(embed=embed)
            return
        except coc.Maintenance:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  title=f'Error',
                                  description='The Clash of Clans API is currently under maintenance.')
            await ctx.reply(embed=embed)
            return

        embed: discord.Embed = discord.Embed(colour=discord.Colour.yellow(), title='Clan Info', 
                                             description=f'Information about {clan.name} ({clan.tag})\n[Open in game]({clan.share_link})')

        # Set the thumbnail to the clan's badge if it exists.
        if clan.badge is not None and hasattr(clan.badge, "url"):
            embed.set_thumbnail(url=clan.badge.url)

        embed.add_field(name='Description',
                    value=clan.description,
                    inline=False)
        
        embed.add_field(name='Members',
                    value=f'{clan.member_count}/50',
                    inline=False)
        
        embed.add_field(name='Clan Type',
                    value=clan.type,
                    inline=True)

        embed.add_field(name='Location',
                    value=clan.location,
                    inline=True)
        
        leader: coc.ClanMember | None = clan.get_member_by(role=coc.Role.leader)
        if leader is not None:
            embed.add_field(name='Leader',
                            value=f'{leader.name} ({leader.tag})',
                            inline=False)
        
        embed.add_field(name='Clan Labels',
                    value='\n'.join(label.name for label in clan.labels),
                    inline=True)
        
        embed.add_field(name='War Record',
                        value=f'Won - {clan.war_wins}\nLost - {clan.war_losses}\n'
                        f'Draw - {clan.war_ties}',
                        inline=True)
        
        embed.add_field(name='Wars',
                    value=f'War Frequency: {clan.war_frequency}\n'
                          f'War Win Streak: {clan.war_win_streak}\n'
                          f'War League: {'' if clan.war_league is None else clan.war_league.name}\n'
                          f'War Log: {"Public" if clan.public_war_log else "Private"}',
                    inline=False)

        embed.add_field(name='Trophies',
                        value=f'Clan Trophies: {clan.points}\n'
                        f'Required Trophies: {clan.required_trophies}\n'
                        f'Builder Base Trophies: {clan.builder_base_points}\n'
                        f'Required Builder Base Trophies: {clan.required_builder_base_trophies}',
                        inline=False)

        # If the the clan has districts info, add it to the embed.
        if clan.capital_districts:
            frame: str = ''

            for district in clan.capital_districts:
                frame += (f'`{f'{district.name}:':<20}` 'f'`{district.hall_level:<15}`\n')

            embed.add_field(name='Capital District',
                            value=frame,
                            inline=False)

        await ctx.send(embed=embed)

    @player.error
    @clan.error
    @members.error
    async def handle_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            message = f'Missing required argument for this command.\n`{error.param}`'
        else:
            message = f'{error}'

        embed: discord.Embed = discord.Embed(colour=discord.Colour.red(),
                              title='Error',
                              description=message)

        await ctx.send(embed=embed)

async def setup(bot: ClashBot):
    await bot.add_cog(ClashOfClansCog(bot))
