import coc

@coc.ClanEvents.member_join()
async def on_clan_member_join(old_member : coc.ClanMember, new_member : coc.ClanMember):
    print(f'Player {old_member.name}{old_member.tag} just joined {new_member.clan.name}')

@coc.ClanEvents.member_leave()
async def on_clan_member_leave(old_member : coc.ClanMember, new_member : coc.ClanMember):
    print(f'Player {new_member.name}{new_member.tag} just left {old_member.clan.name}')

@coc.ClanEvents.member_donations()
async def on_clan_member_sent_donation(old_member : coc.ClanMember, new_member : coc.ClanMember):
    sent_troop_count : int = new_member.donations - old_member.donations
    print(f'Player {new_member.name}{new_member.tag} just sent {sent_troop_count} troops.')

@coc.ClanEvents.member_received()
async def on_clan_member_recieved_donation(old_member : coc.ClanMember, new_member : coc.ClanMember):
    recieved_troop_count : int = new_member.received - old_member.received
    print(f'Player {new_member.name}{new_member.tag} just received {recieved_troop_count} troops.')