"""Script that gets matches data and returns a well formatted response of each current match

Get next tournament
Get current match score
"""
import re

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Match:
    header: str
    summary: str
    score1: 'TeamScore'
    score2: 'TeamScore'


@dataclass
class TeamScore:
    team: str
    game: str
    first_set: str
    second_set: str
    third_set: str

    def __str__(self):
        return (
            f'👥 {self.team}\n'
            f'{self.game or "-"} | {self.first_set} {self.second_set} {self.third_set}'
        )


def _get_player_names(element):
    player_names_div = element.find('div', class_='player-names')
    player_names_spans = player_names_div.select('td.team span')
    # Remove name initial and empty spans
    spans = [span for span in player_names_spans if span.text and '.' not in span.text]
    # Surname 1 [Surname 2] / Surname A
    players = " / ".join((spans[0].text, spans[1].text))
    return players


def _get_team_score(team_row):
    data = team_row.find_all('td')
    team = _get_player_names(data[0])
    points_this_game = data[1].text.strip().replace('\n', ' ')
    first_set_games = data[2].text.strip().replace('\n', ' ')
    second_set_games = data[3].text.strip().replace('\n', ' ')
    third_set_games = data[4].text.strip().replace('\n', ' ')

    return TeamScore(
        team=team,
        game=points_this_game,
        first_set=first_set_games,
        second_set=second_set_games,
        third_set=third_set_games,
    )


def _get_matches_html():
    paris_major_url = 'https://widget.matchscorerlive.com/screen/tournamentlive/FIP-2023-3603?t=tol'
    r = requests.get(paris_major_url, timeout=10)
    return BeautifulSoup(r.text, 'lxml')


def _parse_matches(matches):
    result = []
    for m in matches:
        try:
            scoring_table = m.find('table')
            table_sections = scoring_table.find_all('tr')

            header_raw = table_sections[0].text.strip()
            header = re.sub(r'\s+', ' ', header_raw)
            summary_raw = table_sections[3].text.strip()
            summary = re.sub(r'\s+', ' ', summary_raw).replace('MATCH STATS', '').strip()
            team1 = table_sections[1]
            team2 = table_sections[2]
            score1 = _get_team_score(team1)
            score2 = _get_team_score(team2)
            result.append(Match(header, summary, score1, score2))
        except Exception as e:
            print(f"An error occurred {e!r}")

    return result


def get_current_matches():
    soup = _get_matches_html()
    live = soup.find("div", id='live-scores-container')
    matches_table = live.find("div", class_='row')
    matches = matches_table.find_all('div', recursive=False)  # Only find first level divs
    matches = _parse_matches(matches)
    return matches


def format_matches(matches: list[Match]) -> str:
    return '\n'.join(
        f"⛳ {match.header} {match.summary}\n{match.score1}\n{match.score2}\n"
        for match in matches
    ) or 'No hay partidos en curso'


def get_current_matches_as_string():
    return format_matches(get_current_matches())

if __name__ == "__main__":
    print(get_current_matches_as_string())