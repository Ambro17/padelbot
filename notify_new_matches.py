"""Notify if a specific pair is playing"""
from api import get_current_matches

pairs = {
    'Belasteguin/Yanguas': ['belasteguin', 'yanguas'],
    'Chingotto/Navarro': ['chingotto', 'navarro'],
    'Coello/Tapia': ['coello', 'tapia'],
    'Gutierrez/Gonzalez': ['gutierrez', 'gonzalez'],
    'Lebron/Galan': ['lebron', 'galan'],
    'Sanz/Nieto': ['sanz', 'nieto'],
    'Stupaczuk/Di Nenno': ['stupaczuk', 'di nenno'],
    'Tello/Ruiz': ['tello', 'ruiz']
}


def is_pair_present(live_match_pair, selected_pair):
    team_members = pairs.get(selected_pair, [])
    return any(member.lower() in live_match_pair.lower() for member in team_members)


def update_suscribers():
    matches = get_current_matches()
    suscribers = {'Tapia/Coello': [], 'Nieto/Sanz': []}
    for match in matches:
        team1 = match.score1.team
        team2 = match.score2.team
        notify_of_match(match, suscribers)


    pass


def notify_of_match(match, suscribers: dict):
    match_status = get_match()
    if match_status == 'NOTIFIED':
        return

    for s in suscribers:
        # Api call to their stored user id
        pass

    mark_match_as_notified()
    pass


def mark_match_as_notified():
    # Mark Tournament-Team1-Team2 match as completed
    pass


def get_match():
    return ''
