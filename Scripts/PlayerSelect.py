import requests
import json
import random
import unidecode

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
}

EUROPEAN_COMPETITIONS = {
    'champions_league': {'id': 7, 'name': 'Champions League', 'season_id': SEASON_IDS['champions_league']},
    'europa_league': {'id': 679, 'name': 'Europa League', 'season_id': SEASON_IDS['europa_league']},
    'europa_conference_league': {'id': 17015, 'name': 'Europa Conference League', 'season_id': SEASON_IDS['europa_conference_league']}
}


def get_current_season_id(league_id):
    # Keep this function for potential future use
    url = f"https://api.sofascore.com/api/v1/unique-tournament/{league_id}/seasons"
    response = requests.get(url)
    if response.status_code == 200:
        seasons = response.json()['seasons']
        return max(season['id'] for season in seasons)
    else:
        print(f"Failed to fetch seasons for league {league_id}: {response.status_code}")
        return None

def get_league_standings(league_key, leagues_dict):
    league = leagues_dict[league_key]
    url = f"https://api.sofascore.com/api/v1/unique-tournament/{league['id']}/season/{league['season_id']}/standings/total"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        standings = data['standings'][0]['rows']
        return {team['team']['name']: team['position'] for team in standings}
    else:
        print(f"Failed to fetch standings: {response.status_code}")
        return {}

def get_league_top_players(league_key, leagues_dict):
    league = leagues_dict[league_key]
    url = f"https://api.sofascore.com/api/v1/unique-tournament/{league['id']}/season/{league['season_id']}/top-players/overall"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        top_players = []
        categories = ['rating', 'goals', 'assists']
        for category in categories:
            players = data.get('topPlayers', {}).get(category, [])
            for player in players[:5]:  # Get top 5 players from each category
                player_data = {
                    'name': player['player']['name'],
                    'team': player['team']['name'],
                    'league': league['name'],
                    'rating': player.get('rating', 0),
                    'goals': player.get('goals', 0),
                    'assists': player.get('assists', 0),
                    'g+a': player.get('goals', 0) + player.get('assists', 0),
                    'category': category
                }
                top_players.append(player_data)
        
        return top_players
    else:
        print(f"Failed to fetch {league['name']} top players: {response.status_code}")
        return []

def load_past_players():
    try:
        with open('resources/Past_players.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Past_players.json not found. Creating an empty list.")
        return []

def scout_players():
    all_players = []
    past_players = load_past_players()
    past_player_names = set(player['name'] for player in past_players)
    standings = {}
    
    for leagues_dict in [TOP_5_LEAGUES, EUROPEAN_COMPETITIONS]:
        for league_key, league_info in leagues_dict.items():
            standings[league_info['name']] = get_league_standings(league_key, leagues_dict)
            top_players = get_league_top_players(league_key, leagues_dict)
            all_players.extend(top_players)
    
    # Remove duplicates and past players
    unique_players = {}
    for player in all_players:
        if player['name'] not in past_player_names and player['name'] not in unique_players:
            unique_players[player['name']] = player
    
    # Sort players by different criteria
    rating_sorted = sorted(unique_players.values(), key=lambda x: x['rating'], reverse=True)
    goals_sorted = sorted(unique_players.values(), key=lambda x: x['goals'], reverse=True)
    assists_sorted = sorted(unique_players.values(), key=lambda x: x['assists'], reverse=True)
    ga_sorted = sorted(unique_players.values(), key=lambda x: x['g+a'], reverse=True)
    
    # Select top players from each category
    selected_players = []
    for sorted_list in [rating_sorted, goals_sorted, assists_sorted, ga_sorted]:
        for player in sorted_list:
            if len(selected_players) >= 25:
                break
            if player not in selected_players:
                selected_players.append(player)
        if len(selected_players) >= 25:
            break
    
    # Shuffle the list to mix up the order
    random.shuffle(selected_players)
    
    return selected_players[:25], standings

def create_player_file(players, standings):
    player_data = []
    for player in players:
        league_standings = standings.get(player['league'], {})
        team_position = league_standings.get(player['team'], 'Unknown')
        player_data.append({
            "name": unidecode.unidecode(player['name']),
            "team": unidecode.unidecode(player['team']),
            "league": player['league'],
            "category": player['category'],
            "position": team_position
        })
    
    with open('resources/Next_players.json', 'w', encoding='utf-8') as f:
        json.dump(player_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    selected_players, standings = scout_players()
    create_player_file(selected_players, standings)
    print("Selected players have been saved to 'resources/Next_players.json'")
    
