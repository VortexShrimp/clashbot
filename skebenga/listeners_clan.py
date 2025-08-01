"""
Module that holds all the ClanEvent listeners for the bot.
"""

import coc
import discord
import globals
import utilities

@coc.ClanEvents.member_join()
async def on_member_join(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    print('[debug] on_clan_member_join called')
    
    embed = discord.Embed(colour=discord.Colour.green(),
                          title='Player Joined',
                          description=f'Player `{new_member.name} ({new_member.tag})` has joined the clan.')
    
    clan_badge: coc.Badge | None = new_member.clan.badge if new_member.clan else None
    if clan_badge is not None and hasattr(clan_badge, "url"):
        embed.set_thumbnail(url=clan_badge.url)

    frame += (
        f'`{'League:':<20}` `{new_member.league.name:<20.20}`\n'
        f'`{'Trophies:':<20}` `{new_member.trophies:<20}`\n'
        f'`{'Best Trophies:':<20}` `{new_member.best_trophies:<20}`\n'
        f'`{'War Stars:':<20}` `{new_member.war_stars:<20}`\n'
        f'`{'Attack Wins:':<20}` `{new_member.attack_wins:<20}`\n'
        f'`{'Defense Wins:':<20}` `{new_member.defense_wins:<20}`\n'
        f'`{'Capital Contribution':<20}` `{new_member.clan_capital_contributions:<20}`\n'
        )

    embed.add_field(name='Info',
                    value=frame,
                    inline=False)

    await utilities.send_embed_via_webhook(globals.DISCORD_CLAN_WEBHOOK, embed)

@coc.ClanEvents.member_leave()
async def on_member_leave(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    print('[debug] on_clan_member_leave called')
    
    embed = discord.Embed(colour=discord.Colour.red(),
                          title='Player Left',
                          description=f'Player `{new_member.name} ({new_member.tag})` has left the clan.')

    # Need to get the old member's clan badge because they just left.
    clan_badge: coc.Badge | None = old_member.clan.badge if old_member.clan else None
    if clan_badge is not None and hasattr(clan_badge, "url"):
        embed.set_thumbnail(url=clan_badge.url)

    await utilities.send_embed_via_webhook(globals.DISCORD_CLAN_WEBHOOK, embed)

@coc.ClanEvents.level()
async def on_level(old_clan: coc.Clan, new_clan: coc.Clan) -> None:
    print('[debug] on_clan_level_changed called')
    
    if old_clan.level == new_clan.level:
        return
    
    embed = discord.Embed(colour=discord.Colour.green(),
                          title='Level Up',
                          description=f'{new_clan.name} has leveled up to {new_clan.level}!')
    
    if new_clan.badge is not None and hasattr(new_clan.badge, "url"):
        embed.set_thumbnail(url=new_clan.badge.url)

    await utilities.send_embed_via_webhook(globals.DISCORD_CLAN_WEBHOOK, embed)

@coc.ClanEvents.description()
async def on_description(old_clan: coc.Clan, new_clan: coc.Clan) -> None:
    print('[debug] on_clan_description_changed called')
    
    # Nothing changed.
    if old_clan.description == new_clan.description:
        return
    
    embed = discord.Embed(colour=discord.Colour.yellow(),
                          title='Description Update')
    
    if new_clan.badge is not None and hasattr(new_clan.badge, "url"):
        embed.set_thumbnail(url=new_clan.badge.url)

    embed.add_field(name='Old',
                    value=old_clan.description,
                    inline=False)

    embed.add_field(name='New',
                    value=new_clan.description,
                    inline=False)

    await utilities.send_embed_via_webhook(globals.DISCORD_CLAN_WEBHOOK, embed)

@coc.ClanEvents.badge()
async def on_badge(old_clan: coc.Clan, new_clan: coc.Clan) -> None:
    # Spammed by the API for some reason.
    # print('[debug] on_clan_badge_changed called')

    new_badge: coc.Badge | None = new_clan.badge
    old_badge: coc.Badge | None = old_clan.badge

    if new_badge is None or old_badge is None:
        return
    
    # If the badge URL hasn't changed, don't send the event.
    if new_badge.url == old_badge.url:
        return

    embed = discord.Embed(colour=discord.Colour.yellow(),
                          title='Badge Update',
                          description='The clan\'s badge has been updated.')

    embed.set_thumbnail(url=new_badge.url)
    embed.add_field(name='Old',
                    value=f'[Old Badge]({old_badge.url})',
                    inline=False)

    await utilities.send_embed_via_webhook(globals.DISCORD_CLAN_WEBHOOK, embed)

@coc.ClanEvents.member_role()
async def on_member_role(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    print('[debug] on_member_role_changed called')
    
    old_role: coc.Role = old_member.role if old_member.role else coc.Role.member
    new_role: coc.Role = new_member.role if new_member.role else coc.Role.member

    # Nothing to do if the role hasn't changed.
    if old_role == new_role:
        return

    embed = discord.Embed(colour=discord.Colour.orange(),
                          title='Role Changed')

    embed.add_field(name='Member',
                    value=f'{new_member.name} ({new_member.tag})',
                    inline=False)
    
    embed.add_field(name='Old',
                    value=old_role.in_game_name,
                    inline=True)
    
    embed.add_field(name='New',
                    value=new_role.in_game_name,
                    inline=True)

    await utilities.send_embed_via_webhook(globals.DISCORD_CLAN_WEBHOOK, embed)

@coc.ClanEvents.member_donations()
async def on_member_donations_sent(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    print('[debug] on_member_donations_sent called')

    donation_count: int = new_member.donations - old_member.donations
    if donation_count == 0:
        return
    
    embed = discord.Embed(colour=discord.Colour.green(),
                          title='Donations Sent',
                          description=f'{new_member.name} `{new_member.tag}` has donated: {donation_count} troops.')
    
    await globals.send_embed_via_webhook(globals.DISCORD_DONATIONS_WEBHOOK, embed)

@coc.ClanEvents.member_received()
async def on_member_donations_received(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    print('[debug] on_member_donations_received called')

    received_count: int = new_member.received - old_member.received
    if received_count == 0:
        return

    embed = discord.Embed(colour=discord.Colour.red(),
                          title='Donations Received',
                          description=f'{new_member.name} `{new_member.tag}` has received: {received_count} troops.')

    await utilities.send_embed_via_webhook(globals.DISCORD_DONATIONS_WEBHOOK, embed)
