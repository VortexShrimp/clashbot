import coc
import os
import aiohttp
import discord

# INFO: This file contains event listeners for the Clash of Clans events.
#
# TODO: Split this up into multiple files. For example, one for clan events, one for war events, etc.
# 
#       Right now, each function searches for the webhook URL in the environment variables, everytime it is called.
#       This is not efficient, so we should probably load it once and pass it to the functions.
#
#       Also, currently the member donations event only sends a message if the member has donated troops or received troops.
#       There is no info about who sent/received the troops in the events, so we cannot send that information.
#       In terms of a solution, I think a global queue could be used to store the donations and then send them in batch.

# Helper function to send a webhook.
async def send_embed_via_webhook(webhook_url: str, embed: discord.Embed) -> None:
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)
        await webhook.send(embed=embed)

@coc.ClanEvents.member_join()
async def on_clan_member_join(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    print('[debug] on_clan_member_join called')

    webhook_url: str | None = os.getenv('DISCORD_CLAN_WEBHOOK')
    if webhook_url is None:
        return
    
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
    
    await send_embed_via_webhook(webhook_url, embed)

@coc.ClanEvents.member_leave()
async def on_clan_member_leave(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    print('[debug] on_clan_member_leave called')

    webhook_url: str | None = os.getenv('DISCORD_CLAN_WEBHOOK')
    if webhook_url is None:
        return
    
    embed = discord.Embed(colour=discord.Colour.red(),
                          title='Player Left',
                          description=f'Player `{new_member.name} ({new_member.tag})` has left the clan.')

    # Need to get the old member's clan badge because they just left.
    clan_badge: coc.Badge | None = old_member.clan.badge if old_member.clan else None
    if clan_badge is not None and hasattr(clan_badge, "url"):
        embed.set_thumbnail(url=clan_badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.ClanEvents.level()
async def on_clan_level_changed(old_clan: coc.Clan, new_clan: coc.Clan) -> None:
    print('[debug] on_clan_level_changed called')

    webhook_url: str | None= os.getenv('DISCORD_CLAN_WEBHOOK')
    if webhook_url is None:
        return
    
    if old_clan.level == new_clan.level:
        return
    
    embed = discord.Embed(colour=discord.Colour.yellow(),
                          title='Level Up',
                          description=f'The clan has leveled up from {old_clan.level} to {new_clan.level}.')
    
    if new_clan.badge is not None and hasattr(new_clan.badge, "url"):
        embed.set_thumbnail(url=new_clan.badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.ClanEvents.description()
async def on_clan_description_changed(old_clan: coc.Clan, new_clan: coc.Clan) -> None:
    print('[debug] on_clan_description_changed called')

    webhook_url: str | None = os.getenv('DISCORD_CLAN_WEBHOOK')
    if webhook_url is None:
        return
    
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
    
    await send_embed_via_webhook(webhook_url, embed)

@coc.ClanEvents.badge()
async def on_clan_badge_changed(old_clan: coc.Clan, new_clan: coc.Clan) -> None:
    # Spammed by the API for some reason.
    # print('[debug] on_clan_badge_changed called')

    webhook_url: str | None = os.getenv('DISCORD_CLAN_WEBHOOK')
    if webhook_url is None:
        return
    
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

    await send_embed_via_webhook(webhook_url, embed)

@coc.ClanEvents.member_donations()
async def on_member_donations_sent(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    print('[debug] on_member_donations_sent called')

    webhook_url: str | None = os.getenv('DISCORD_DONATIONS_WEBHOOK')
    if webhook_url is None:
        return

    donation_count: int = new_member.donations - old_member.donations
    if donation_count == 0:
        return
    
    embed = discord.Embed(colour=discord.Colour.green(),
                          title='Donations Sent',
                          description=f'{new_member.name} `{new_member.tag}` has donated: {donation_count} troops.')
    
    # clan_badge: coc.Badge | None = new_member.clan.badge if new_member.clan else None
    # if clan_badge is not None and hasattr(clan_badge, "url"):
    #     embed.set_thumbnail(url=clan_badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.ClanEvents.member_received()
async def on_member_donations_received(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    print('[debug] on_member_donations_received called')

    webhook_url: str | None = os.getenv('DISCORD_DONATIONS_WEBHOOK')
    if webhook_url is None:
        return

    received_count: int = new_member.received - old_member.received
    if received_count == 0:
        return

    embed = discord.Embed(colour=discord.Colour.red(),
                          title='Donations Received',
                          description=f'{new_member.name} `{new_member.tag}` has received: {received_count} troops.')

    # Too much spam.
    # clan_badge: coc.Badge | None = new_member.clan.badge if new_member.clan else None
    # if clan_badge is not None and hasattr(clan_badge, "url"):
    #     embed.set_thumbnail(url=clan_badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.WarEvents.new_war()
async def on_new_war(new_war: coc.ClanWar) -> None:
    print('[debug] on_new_war called')

    webhook_url: str | None = os.getenv('DISCORD_WAR_WEBHOOK')
    if webhook_url is None:
        return
    
    embed = discord.Embed(colour=discord.Colour.yellow(),
                          title='New War',
                          # TODO: Neaten this up...
                          description=f'A new `{new_war.team_size}vs{new_war.team_size}` war has started against `{new_war.opponent.name} ({new_war.opponent.tag}) level {new_war.opponent.level}`.')

    clan_badge: coc.Badge | None = new_war.clan.badge if new_war.clan else None
    if clan_badge is not None and hasattr(clan_badge, "url"):
        embed.set_thumbnail(url=clan_badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.WarEvents.war_attack()
async def on_war_attack(attack: coc.WarAttack, current_war: coc.ClanWar) -> None:
    print('[debug] on_war_attack called')

    webhook_url: str | None = os.getenv('DISCORD_WAR_WEBHOOK')
    if webhook_url is None:
        return

    home_clan_tag: str | None = os.getenv('COC_CLAN_TAG')
    if home_clan_tag is None:
        return
    
    # If the attacker is in our clan make the color green.
    colour : discord.Colour = discord.Colour.green() if attack.attacker.clan.tag == home_clan_tag else discord.Colour.red()
    description: str = f'New attack from {attack.attacker.clan.name}'

    embed = discord.Embed(colour=colour,
                          title='War Attack',
                          description=description)
    
    embed.add_field(name='Attacker',
                    value=f'{attack.attacker.name} ({attack.attacker.tag})\n'
                          f'`{"Town Hall:":<15}` `{attack.attacker.town_hall:<3}`\n'
                          f'`{"Number:":<15}` `{attack.attacker.map_position:<3}`',
                    inline=False)
    
    embed.add_field(name='Defender',
                    value=f'{attack.defender.name} ({attack.defender.tag})\n'
                          f'`{"Town Hall:":<15}` `{attack.defender.town_hall:<3}`\n'
                          f'`{"Number:":<15}` `{attack.defender.map_position:<3}`',
                    inline=False)

    embed.add_field(name='Stats',
                    value=f'`{"Stars:":<15}` `{attack.stars:<3}`\n'
                          f'`{"Destruction:":<15}` `{attack.destruction:<3}%`',
                    inline=False)

    clan_badge: coc.Badge | None = attack.attacker.clan.badge if attack.attacker.clan else None
    if clan_badge is not None and hasattr(clan_badge, "url"):
        embed.set_thumbnail(url=clan_badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.WarEvents.state()
async def on_war_state_changed(old_war: coc.ClanWar, new_war: coc.ClanWar) -> None:
    print('[debug] on_war_state_changed called')

    webhook_url: str | None = os.getenv('DISCORD_WAR_WEBHOOK')
    if webhook_url is None:
        return

    new_war_state: coc.wars.WarState = new_war.state
    old_war_state: coc.wars.WarState = old_war.state
    
    embed = discord.Embed(colour=discord.Colour.dark_grey(),
                          title='War State Update',
                          description=f'Clan war state has changed from {old_war_state.in_game_name} to {new_war_state.in_game_name}')

    clan_badge: coc.Badge | None = new_war.clan.badge if new_war.clan else None
    if clan_badge is not None and hasattr(clan_badge, "url"):
        embed.set_thumbnail(url=clan_badge.url)

    await send_embed_via_webhook(webhook_url, embed)
