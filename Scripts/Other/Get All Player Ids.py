import requests
import json
import time

def load_teams():
    with open('resources/all_teams.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_team_players(team_id):
    url = f"https://www.sofascore.com/api/v1/team/{team_id}/players"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch players for team {team_id}: {response.status_code}")
        return None

def extract_player_info(player_data):
    return {
        "id": player_data['player']['id'],
        "name": player_data['player']['name']
    }

def get_all_players():
    teams = load_teams()
    all_players = {}

    for team_name, team_info in teams.items():
        print(f"Fetching players for {team_name}...")
        team_id = team_info['id']
        players_data = get_team_players(team_id)
        
        if players_data:
            team_players = [extract_player_info(player) for player in players_data['players']]
            all_players[team_name] = team_players
        
        time.sleep(1)  # To avoid hitting rate limits

    return all_players

def save_players_to_json(players):
    with open('resources/all_players.json', 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    all_players = get_all_players()
    save_players_to_json(all_players)
    print("All players have been saved to 'resources/all_players.json'")

