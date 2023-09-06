"""Script that gets matches data and returns a well formatted response of each current match

Get next tournament
Get current match score
"""
from bs4 import BeautifulSoup
from dataclasses import dataclass

with open("result.html", "r") as f:
    soup = BeautifulSoup(f.read(), 'lxml')

@dataclass
class TeamScore:
    team: str
    game: str
    first_set: str
    second_set: str
    third_set: str

    def __str__(self):
        return (
            f'{self.team}\n{self.game} {self.first_set} {self.second_set} {self.third_set}'
        )


def get_team_score(team_row):
    data = team_row.find_all('td')
    team = data[0].text.strip().replace('\n', ' ').replace(' ' * 8, ' ')  # Improve style and (rank)
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




live = soup.find("div", id='live-scores-container')
matches_table = live.find("div", class_='row')
matches = matches_table.find_all('div', recursive=False) # Only find first level divs
for m in matches:
    try:
        scoring_table = m.find('table')
        if not scoring_table:
            continue
        table_sections = scoring_table.find_all('tr')
        header = table_sections[0].text.strip().replace('\n', ' | ')
        summary = table_sections[3].text.strip().replace('\n' * 4, ' ')
        team1 = table_sections[1]
        team2 = table_sections[2]
        score1 = get_team_score(team1)
        score2 = get_team_score(team2)
        print("MATCH")
        print(score1)
        print(score2)
        print("------")
    except Exception as e:
        breakpoint()
        assert 1
        assert 2

