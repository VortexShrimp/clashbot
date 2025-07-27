"""
Module that holds all the WarEvent listeners for the bot.
"""

import coc
import discord
import globals

@coc.WarEvents.new_war()
async def on_new_war(new_war: coc.ClanWar) -> None:
    print('[debug] on_new_war called')
    
    embed = discord.Embed(colour=discord.Colour.yellow(),
                          title='New War',
                          # TODO: Neaten this up...
                          description=f'A new `{new_war.team_size}vs{new_war.team_size}` war has started against `{new_war.opponent.name} ({new_war.opponent.tag}) level {new_war.opponent.level}`.')

    clan_badge: coc.Badge | None = new_war.clan.badge if new_war.clan else None
    if clan_badge is not None and hasattr(clan_badge, "url"):
        embed.set_thumbnail(url=clan_badge.url)

    await globals.send_embed_via_webhook(globals.DISCORD_WAR_WEBHOOK, embed)

@coc.WarEvents.war_attack()
async def on_attack(attack: coc.WarAttack, current_war: coc.ClanWar) -> None:
    print('[debug] on_war_attack called')
    
    # If the attacker is in our clan make the color green.
    colour : discord.Colour = discord.Colour.green() if attack.attacker.clan.tag == globals.COC_CLANTAG else discord.Colour.red()
    description: str = f'New attack from {attack.attacker.clan.name}'

    embed = discord.Embed(colour=colour,
                          title='War Attack',
                          description=description)
    
    embed.add_field(name='Attacker',
                    value=f'{attack.attacker.name} ({attack.attacker.tag})\n'
                          f'`{"Town Hall:":<15}` `{attack.attacker.town_hall:<4}`\n'
                          f'`{"Number:":<15}` `{attack.attacker.map_position:<4}`',
                    inline=False)
    
    embed.add_field(name='Defender',
                    value=f'{attack.defender.name} ({attack.defender.tag})\n'
                          f'`{"Town Hall:":<15}` `{attack.defender.town_hall:<4}`\n'
                          f'`{"Number:":<15}` `{attack.defender.map_position:<4}`',
                    inline=False)

    embed.add_field(name='Results',
                    value=f'`{"Stars:":<15}` `{attack.stars:<4}`\n'
                          f'`{"Destruction:":<15}` `{attack.destruction:<4}%`',
                    inline=False)
    
    # TODO: Add updated war stats, like current stars, destruction and time until war ends.

    clan_badge: coc.Badge | None = attack.attacker.clan.badge if attack.attacker.clan else None
    if clan_badge is not None and hasattr(clan_badge, "url"):
        embed.set_thumbnail(url=clan_badge.url)

    await globals.send_embed_via_webhook(globals.DISCORD_WAR_WEBHOOK, embed)

@coc.WarEvents.state()
async def on_state(old_war: coc.ClanWar, new_war: coc.ClanWar) -> None:
    print('[debug] on_war_state_changed called')

    new_war_state: coc.wars.WarState = new_war.state
    old_war_state: coc.wars.WarState = old_war.state
    
    embed = discord.Embed(colour=discord.Colour.dark_grey(),
                          title='War State Update',
                          description=f'Clan war state has changed from {old_war_state.in_game_name} to {new_war_state.in_game_name}')

    clan_badge: coc.Badge | None = new_war.clan.badge if new_war.clan else None
    if clan_badge is not None and hasattr(clan_badge, "url"):
        embed.set_thumbnail(url=clan_badge.url)

    await globals.send_embed_via_webhook(globals.DISCORD_WAR_WEBHOOK, embed)