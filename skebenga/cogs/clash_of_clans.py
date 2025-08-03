import datetime
import coc
import discord
from discord.ext import commands

from main import ClashBot
import utilities

class ClashOfClansCog(commands.Cog):
    """
    Clash of Clans related commands.
    """

    def __init__(self, bot: ClashBot) -> None:
        self.bot: ClashBot = bot

    @commands.command(name='player')
    async def player(self, ctx: commands.Context, player_tag: str) -> None:
        """
        Get information about a Clash of Clans player by their tag.

        Args:
            player_tag (str): The tag of the player to get information about.
        """

        # Make sure the player's tag is valid.
        if not coc.utils.is_valid_tag(player_tag):
            await ctx.reply(embed=utilities.default_error_embed('The tag that you provided has an invalid format.'))
            return
        
        # Attempt to get the player.
        try:
            player: coc.Player = await self.bot.coc_client.get_player(player_tag)
        except coc.NotFound:
            await ctx.reply(embed=utilities.default_error_embed(f'Unable to find the player with the provided tag ({player_tag}).'))
            return
        except coc.Maintenance:
            await ctx.reply(embed=utilities.default_error_embed('The Clash of Clans API is currently under maintenance.'))
            return
        
        # Create the embed with player information.
        embed: discord.Embed = discord.Embed(colour=utilities.get_bot_guild_role_colour(ctx), title=f'Player Info', description=f'Information for player `{player.name} ({player.tag})`')

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
    async def members(self, ctx: commands.Context, clan_tag: str | None = None) -> None:
        """
        Get a list of members in a Clash of Clans clan.
        Args:
            clan_tag (str): The tag of the clan to get members from.
        """

        # If no clan tag is provided, use the tag found in the .env file.
        desired_clan_tag: str = self.bot.coc_clantag if clan_tag is None else clan_tag

        # Make sure the clan's tag is valid.
        if not coc.utils.is_valid_tag(desired_clan_tag):
            await ctx.reply(embed=utilities.default_error_embed(f'Invalid clan tag format provided `{desired_clan_tag}`.'))
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
            await ctx.reply(embed=utilities.default_error_embed('The Clash of Clans API is currently under maintenance.'))
            return
        except coc.GatewayError:
            await ctx.reply(embed=utilities.default_error_embed('Unexpected gateway error.'))
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
    async def clan(self, ctx: commands.Context, clan_tag: str | None = None) -> None:
        """
        Get information about a Clash of Clans clan by its tag.

        Args:
            clan_tag (str): The tag of the clan to get information about
        """

        # If no clan tag is provided, use the tag found in the .env file.
        desired_clan_tag: str = self.bot.coc_clantag if clan_tag is None else clan_tag

        # Make sure the clan's tag is valid.
        if not coc.utils.is_valid_tag(desired_clan_tag):
            await ctx.reply(embed=utilities.default_error_embed(f'Invalid clan tag format provided `({desired_clan_tag})`.'))
            return

        # Attempt to get the clan.
        try:
            clan: coc.Clan = await self.bot.coc_client.get_clan(desired_clan_tag)
        except coc.NotFound:
            await ctx.reply(embed=utilities.default_error_embed(f'Unable to get the desired clan with tag `({desired_clan_tag})`.'))
            return
        except coc.Maintenance:
            await ctx.reply(embed=utilities.default_error_embed('The Clash of Clans API is currently under maintenance.'))
            return

        embed: discord.Embed = discord.Embed(colour=utilities.get_bot_guild_role_colour(ctx),
                                             title='Clan Info',
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

    @commands.command(name='war')
    async def war(self, ctx: commands.Context, clan_tag: str | None = None) -> None:
        """
        Get information about the current war of a Clash of Clans clan.

        Args:
            clan_tag (str): The tag of the clan to get war information about.
        """

        # If no clan tag is provided, use the default tag.
        desired_clan_tag: str = self.bot.coc_clantag if clan_tag is None else clan_tag

        # Make sure the clan's tag is valid.
        if not coc.utils.is_valid_tag(desired_clan_tag):
            await ctx.reply(embed=utilities.default_error_embed(f'Invalid clan tag format provided `({desired_clan_tag})`.'))
            return
        
        # Attempt to get the current war for the clan.
        try:
            current_war: coc.ClanWar | None = await self.bot.coc_client.get_current_war(desired_clan_tag)
        except coc.NotFound:
            await ctx.reply(embed=utilities.default_error_embed(f'Unable to find the clan with tag `({desired_clan_tag})` or it is not currently in a war.'))
            return
        except coc.PrivateWarLog:
            await ctx.reply(embed=utilities.default_error_embed(f'The clan with tag `({desired_clan_tag})` has a private war log.'))
            return
        except coc.Maintenance:
            await ctx.reply(embed=utilities.default_error_embed('The Clash of Clans API is currently under maintenance.'))
            return
        
        war_state: coc.wars.WarState = current_war.state
        if war_state == coc.wars.WarState.not_in_war:
            await ctx.reply(embed=utilities.default_error_embed(f'The clan with tag `({desired_clan_tag})` is not currently in a war.'))
            return
        
        home_clan: coc.WarClan | None = current_war.clan
        opponent_clan: coc.WarClan | None = current_war.opponent

        is_cwl: bool = current_war.is_cwl

        embed: discord.Embed = discord.Embed(colour=utilities.get_bot_guild_role_colour(ctx),
                                             title='War Info',
                                             description=f'Information about the current war for {home_clan.name} ({home_clan.tag})')
        
        # Set the thumbnail to the clan's badge if it exists.
        if home_clan.badge is not None and hasattr(home_clan.badge, "url"):
            embed.set_thumbnail(url=home_clan.badge.url)

        embed.add_field(name='Opponent',
                        value=f'{opponent_clan.name} ({opponent_clan.tag})\n'
                              f'Level: {opponent_clan.level}',
                        inline=True)
        
        war_type: str = 'Clan War League\n' if is_cwl else 'Regular War\n'
        war_type += f'{current_war.state.in_game_name}'
        embed.add_field(name='War Type',
                        value=war_type,
                        inline=True)
        
        end_time_seconds: coc.Timestamp = current_war.end_time.seconds_until
        time_left: str = str(datetime.timedelta(seconds=end_time_seconds))

        war_stats: str = f'War Size: {current_war.team_size}vs{current_war.team_size}\n'
        war_stats += f'War Ends In: {time_left}\n'
        embed.add_field(name='War Stats',
                        value=war_stats,
                        inline=False)
        
        embed.add_field(name='Home Clan',
                        value=f'Stars: {home_clan.stars}/{home_clan.max_stars}\n'
                              f'Destruction: {round(home_clan.destruction, 2)}%\n'
                              f'Attacks: {home_clan.attacks_used}/{home_clan.total_attacks}\n',
                        inline=True)
        
        embed.add_field(name='Opponent Clan',
                        value=f'Stars: {opponent_clan.stars}/{opponent_clan.max_stars}\n'
                              f'Destruction: {round(opponent_clan.destruction, 2)}%\n'
                              f'Attacks: {opponent_clan.attacks_used}/{opponent_clan.total_attacks}\n',
                        inline=True)

        await ctx.send(embed=embed)

    @player.error
    @clan.error
    @members.error
    @war.error
    async def handle_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        message: str = ''

        if isinstance(error, commands.MissingRequiredArgument):
            message = f'Missing required argument for this command.\n`{error.param}`'
        else:
            message = f'{error}'

        await ctx.send(embed=utilities.default_error_embed(message))

async def setup(bot: ClashBot):
    await bot.add_cog(ClashOfClansCog(bot))
