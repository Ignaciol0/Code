import requests
import json

SEASON_IDS = {
    'premier_league': 61627,
    'la_liga': 61643,
    'bundesliga': 63516,
    'serie_a': 63515,
    'ligue_1': 61736,
    'champions_league': 61644,
    'europa_league': 61645,
    'europa_conference_league': 61648
}

TOP_5_LEAGUES = {
    'premier_league': {'id': 17, 'name': 'Premier League', 'season_id': SEASON_IDS['premier_league']},
    'la_liga': {'id': 8, 'name': 'La Liga', 'season_id': SEASON_IDS['la_liga']},
    'bundesliga': {'id': 35, 'name': 'Bundesliga', 'season_id': SEASON_IDS['bundesliga']},
    'serie_a': {'id': 23, 'name': 'Serie A', 'season_id': SEASON_IDS['serie_a']},
    'ligue_1': {'id': 34, 'name': 'Ligue 1', 'season_id': SEASON_IDS['ligue_1']},
    'champions_league': {'id': 7, 'name': 'Champions League', 'season_id': SEASON_IDS['champions_league']},
    'europa_league': {'id': 679, 'name': 'Europa League', 'season_id': SEASON_IDS['europa_league']},
    'europa_conference_league': {'id': 17015, 'name': 'Europa Conference League', 'season_id': SEASON_IDS['europa_conference_league']}
}

def get_league_teams(league_key, leagues_dict):
    league = leagues_dict[league_key]
    url = f"https://api.sofascore.com/api/v1/unique-tournament/{league['id']}/season/{league['season_id']}/standings/total"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        standings = data['standings'][0]['rows']
        return [
            {
                'name': team['team']['name'],
                'id': team['team']['id'],
                'league_id': league['id'],
                'league_season_id': league['season_id'],
                'international_id': None,
                'international_season_id': None
            }
            for team in standings
        ]
    else:
        print(f"Failed to fetch teams for {league['name']}: {response.status_code}")
        return []

def get_all_teams():
    all_teams = {}
    for league_key, league_info in TOP_5_LEAGUES.items():
        teams = get_league_teams(league_key, TOP_5_LEAGUES)
        for team in teams:
            if team['name'] not in all_teams:
                all_teams[team['name']] = {
                    'id': team['id'],
                    'league_id': team['league_id'],
                    'league_season_id': team['league_season_id'],
                    'international_id': None,
                    'international_season_id': None
                }
            else:
                # If the team is already in the dict, it might be an international team
                if all_teams[team['name']]['league_id'] is not None:
                    all_teams[team['name']]['international_id'] = team['league_id']
                    all_teams[team['name']]['international_season_id'] = team['league_season_id']
                else:
                    all_teams[team['name']]['league_id'] = team['league_id']
                    all_teams[team['name']]['league_season_id'] = team['league_season_id']
    
    return all_teams

def save_teams_to_json(teams):
    with open('resources/all_teams.json', 'w', encoding='utf-8') as f:
        json.dump(teams, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    all_teams = get_all_teams()
    save_teams_to_json(all_teams)
    print("All teams have been saved to 'resources/all_teams.json'")
