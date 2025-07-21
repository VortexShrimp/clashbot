import coc
import os
import aiohttp
import discord

# Helper function to send a webhook.
async def send_embed_via_webhook(webhook_url: str, embed: discord.Embed) -> None:
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)
        await webhook.send(embed=embed)

@coc.ClanEvents.member_join()
async def on_clan_member_join(old_member: coc.ClanMember, new_member: coc.ClanMember) -> None:
    webhook_url: str | None = os.getenv('DISCORD_CLAN_WEBHOOK')
    if webhook_url is None:
        return

    embed = discord.Embed(colour=discord.Colour.green(),
                          title='Player Joined',
                          description=f'Player `{new_member.name} ({new_member.tag})` has joined the clan.')
    if new_member.clan is not None and new_member.clan.badge is not None and hasattr(new_member.clan.badge, "url"):
        embed.set_thumbnail(url=new_member.clan.badge.url)

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
    webhook_url: str | None = os.getenv('DISCORD_CLAN_WEBHOOK')
    if webhook_url is None:
        return
    
    embed = discord.Embed(colour=discord.Colour.red(),
                          title='Player Left',
                          description=f'Player `{new_member.name} ({new_member.tag})` has left the clan.')
    if old_member.clan is not None and old_member.clan.badge is not None and hasattr(old_member.clan.badge, "url"):
        embed.set_thumbnail(url=old_member.clan.badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.ClanEvents.level()
async def on_clan_level_changed(old_clan: coc.Clan, new_clan: coc.Clan) -> None:
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
    webhook_url: str | None = os.getenv('DISCORD_CLAN_WEBHOOK')
    if webhook_url is None:
        return
    
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
    webhook_url: str | None = os.getenv('DISCORD_CLAN_WEBHOOK')
    if webhook_url is None:
        return
    
    # Don't send the event if nothing has changed.
    if old_clan.badge is not None and new_clan.badge is not None and old_clan.badge.url == new_clan.badge.url:
        return

    embed = discord.Embed(colour=discord.Colour.yellow(),
                          title='Badge Update',
                          description='The clan\'s badge has been updated.')
    if new_clan.badge is not None and hasattr(new_clan.badge, "url"):
        embed.set_thumbnail(url=new_clan.badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.WarEvents.new_war()
async def on_new_war(new_war: coc.ClanWar) -> None:
    webhook_url: str | None = os.getenv('DISCORD_WAR_WEBHOOK')
    if webhook_url is None:
        return
    
    embed = discord.Embed(colour=discord.Colour.yellow(),
                          title='New War',
                          # TODO: Neaten this up...
                          description=f'A new `{new_war.team_size}vs{new_war.team_size}` war has started against `{new_war.opponent.name} ({new_war.opponent.tag}) level {new_war.opponent.level}`.')
    if new_war.clan is not None and new_war.clan.badge is not None and hasattr(new_war.clan.badge, "url"):
        embed.set_thumbnail(url=new_war.clan.badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.WarEvents.war_attack()
async def on_war_attack(attack: coc.WarAttack, current_war: coc.ClanWar) -> None:
    webhook_url: str | None = os.getenv('DISCORD_WAR_WEBHOOK')
    if webhook_url is None:
        return

    home_clan_tag: str | None = os.getenv('COC_CLAN_TAG')
    if home_clan_tag is None:
        return
    
    # If the attacker is in our clan make the color green.
    colour = discord.Colour.green() if attack.attacker.clan.tag == home_clan_tag else discord.Colour.red()
    
    frame: str = f'`{attack.attacker.name}` attacked `{attack.defender.name}` and got {attack.stars} stars with {attack.destruction}%.'

    embed = discord.Embed(colour=colour,
                          title='War Attack',
                          description=frame)
    if attack.attacker.clan is not None and attack.attacker.clan.badge is not None and hasattr(attack.attacker.clan.badge, "url"):
        embed.set_thumbnail(url=attack.attacker.clan.badge.url)

    await send_embed_via_webhook(webhook_url, embed)

@coc.WarEvents.state()
async def on_war_state_changed(old_war: coc.ClanWar, new_war: coc.ClanWar) -> None:
    webhook_url: str | None = os.getenv('DISCORD_WAR_WEBHOOK')
    if webhook_url is None:
        return
    
    embed = discord.Embed(colour=discord.Colour.dark_grey(),
                          title='War State Update',
                          description=f'Clan war state has changed from {old_war.state} to {new_war.state}')
    if new_war.clan is not None and new_war.clan.badge is not None and hasattr(new_war.clan.badge, "url"):
        embed.set_thumbnail(url=new_war.clan.badge.url)

    await send_embed_via_webhook(webhook_url, embed)
