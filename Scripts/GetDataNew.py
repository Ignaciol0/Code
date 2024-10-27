import requests
import json
import pandas as pd
import unidecode
import time
import random
from requests.exceptions import RequestException

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Host': 'api.sofascore.com',
    'Origin': 'https://www.sofascore.com',
    'Referer': 'https://www.sofascore.com/'
}

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

def load_next_players():
    with open('resources/Next_players.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_all_teams():
    with open('resources/all_teams.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_all_players():
    with open('resources/all_players.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_player_id(player_name, all_players):
    for team in all_players.values():
        for player in team:
            if unidecode.unidecode(player['name'].lower()) == unidecode.unidecode(player_name.lower()):
                return player['id']
    return None

def get_player_stats(player_id, tournament_id, season_id, max_retries=3):
    url = f"https://api.sofascore.com/api/v1/player/{player_id}/unique-tournament/{tournament_id}/season/{season_id}/statistics/overall"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            
            if response.status_code == 200:
                data = response.json()
                print(f"Successfully fetched stats for player {player_id}")
                return data
            
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text[:200]}...")  # Print first 200 characters of response
            
            if attempt < max_retries - 1:
                wait_time = random.uniform(1, 3)  # Random wait between 1 and 3 seconds
                print(f"Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed to fetch stats after {max_retries} attempts")
    
    return None

def get_player_matches(player_id):
    url = f"https://www.sofascore.com/api/v1/player/{player_id}/last-year-summary"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch matches: {response.status_code}")
        return None

def parse_player_stats(stats_data):
    if not stats_data or 'statistics' not in stats_data:
        return {}
    stats = stats_data['statistics']
    parsed_stats = {
        'rating': stats.get('rating'),
        'Total played': stats.get('appearances', 0),
        'Started': stats.get('lineups', 0),
        'Minutes per game': stats.get('minutesPlayed', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Goals': stats.get('goals', 0),
        'Assists': stats.get('assists', 0),
        'Yellow cards': stats.get('yellowCards', 0),
        'Red cards': stats.get('redCards', 0),
        'Shots per game': stats.get('shotsTotal', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Pass accuracy': f"{stats.get('passesAccuracy', 0)}%",
        'Key passes': stats.get('keyPasses', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Dribbles': stats.get('dribbleSuccessful', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Tackles': stats.get('tackles', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Interceptions': stats.get('interceptions', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
    }
    return parsed_stats

def parse_player_matches(matches_data):
    if not matches_data or 'events' not in matches_data:
        return []

    parsed_matches = []
    for event in matches_data['events'][:5]:  # Get last 5 matches
        parsed_matches.append({
            'opponent': event['opponent']['name'],
            'goals': event['goals'],
            'assists': event['assists'],
            'rating': event['rating']
        })
    return parsed_matches

def scrape_player(player_info, all_teams, all_players):
    player_name = player_info['name']
    team_name = player_info['team']
    player_id = get_player_id(player_name, all_players)
    if not player_id:
        print(f"Player {player_name} not found")
        return None

    team_data = all_teams.get(team_name)
    if not team_data:
        print(f"Team {team_name} not found")
        return None

    info = {
        'name': player_name,
        'team': team_name,
        'league': player_info['league'],
        'category': player_info['category'],
        'position': player_info['position']
    }
    
    # Get league stats
    league_id = team_data['league_id']
    league_season_id = team_data['league_season_id']
    if league_id and league_season_id:
        stats_data = get_player_stats(player_id, league_id, league_season_id)
        if stats_data:
            info['league_stats'] = parse_player_stats(stats_data)

    # Get European competition stats if available
    euro_id = team_data['international_id']
    euro_season_id = team_data['international_season_id']
    if euro_id and euro_season_id:
        stats_data = get_player_stats(player_id, euro_id, euro_season_id)
        if stats_data:
            info['euro_stats'] = parse_player_stats(stats_data)

    # Get match data
    matches_data = get_player_matches(player_id)
    if matches_data:
        info['matches'] = parse_player_matches(matches_data)

    return info

def save_player_data(player_name, data):
    filename = f"players/{unidecode.unidecode(player_name)}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_all_players():
    next_players = load_next_players()
    all_teams = load_all_teams()
    all_players = load_all_players()
    next_players = [next_players[0]]
    for player_info in next_players:
        print(f"Processing {player_info['name']}...")
        player_data = scrape_player(player_info, all_teams, all_players)
        if player_data:
            save_player_data(player_info['name'], player_data)
            print(f"Data for {player_info['name']} has been saved.")
        else:
            print(f"Failed to retrieve data for {player_info['name']}")

if __name__ == "__main__":
    process_all_players()
