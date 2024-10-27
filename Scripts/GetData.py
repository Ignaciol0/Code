import json
import time
import random
import unidecode
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pandas as pd
import os
import shutil
from ScriptWriter import make_script
from MakePosts import make_yt_videos
from ImageSearch import ImageSearch

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

def get_player_stats(driver, player_id, tournament_id, season_id, max_retries=3):
    url = f"https://api.sofascore.com/api/v1/player/{player_id}/unique-tournament/{tournament_id}/season/{season_id}/statistics/overall"
    
    for attempt in range(max_retries):
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
            json_content = driver.find_element(By.TAG_NAME, "pre").text
            data = json.loads(json_content)
            return data
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 3))
    
    print(f"Failed to fetch stats after {max_retries} attempts")
    return None

def get_player_matches(driver, player_id, max_retries=3):
    url = f"https://www.sofascore.com/api/v1/player/{player_id}/last-year-summary"
    
    for attempt in range(max_retries):
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
            json_content = driver.find_element(By.TAG_NAME, "pre").text
            data = json.loads(json_content)
            return data
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 3))
    
    print(f"Failed to fetch matches after {max_retries} attempts")
    return None

def parse_player_stats(stats_data):
    if not stats_data or 'statistics' not in stats_data:
        return {}

    stats = stats_data['statistics']
    
    # Helper function to calculate per game stats with rounding
    def per_game_stat(stat, appearances):
        if appearances > 0:
            return round(stat / appearances, 2)
        return 0

    parsed_stats = {
        'rating': round(stats.get('rating', 0), 2),
        'Total played': stats.get('appearances', 0),
        'Started': stats.get('matchesStarted', 0),
        'Minutes per game': per_game_stat(stats.get('minutesPlayed', 0), stats.get('appearances', 1)),
        'Goals': stats.get('goals', 0),
        'Assists': stats.get('assists', 0),
        'Yellow': stats.get('yellowCards', 0),
        'Red cards': stats.get('redCards', 0),
        'Shots per game': per_game_stat(stats.get('totalShots', 0), stats.get('appearances', 1)),
        'Shots on target per game': per_game_stat(stats.get('shotsOnTarget', 0), stats.get('appearances', 1)),
        'Goal conversion': str(round(stats.get('goalConversionPercentage', 0), 2)),
        'Accurate per game': f"{stats.get('accuratePasses', 0)}({round(stats.get('accuratePassesPercentage', 0), 2)}%)",
        'Key passes': per_game_stat(stats.get('keyPasses', 0), stats.get('appearances', 1)),
        'Succ. dribbles': f"{stats.get('successfulDribbles', 0)}({round(stats.get('successfulDribblesPercentage', 0), 2)}%)",
        'Tackles per game': per_game_stat(stats.get('tackles', 0), stats.get('appearances', 1)),
        'Interceptions per game': per_game_stat(stats.get('interceptions', 0), stats.get('appearances', 1)),
        'Big chances created': stats.get('bigChancesCreated', 0),
        'Big chances missed': stats.get('bigChancesMissed', 0),
        'Acc. crosses': f"{stats.get('accurateCrosses', 0)}({round(stats.get('accurateCrossesPercentage', 0), 2)}%)",
        'Clearances per game': per_game_stat(stats.get('clearances', 0), stats.get('appearances', 1)),
        'Balls recovered per game': per_game_stat(stats.get('ballRecovery', 0), stats.get('appearances', 1)),
        'Fouls': per_game_stat(stats.get('fouls', 0), stats.get('appearances', 1)),
        'Offsides': per_game_stat(stats.get('offsides', 0), stats.get('appearances', 1)),
        'Team of the week': stats.get('totwAppearances', 0),
        'Clean sheets': stats.get('cleanSheet', 0),
        'Scoring frequency': f"{round(stats.get('scoringFrequency', 0), 2)} min"
    }
    return parsed_stats

def decode_percentage_value(value):
    """Decode a string value that might contain a percentage into its components."""
    if isinstance(value, str):
        if '(' in value and ')' in value:
            parts = value.split('(')
            cumulative = float(parts[0].strip())
            percentage = float(parts[1].replace('%)', ''))
            return cumulative, percentage
    return value, None

def combine_stats(league_stats, euro_stats):
    combined_stats = {}
    total_appearances = league_stats.get('Total played', 0) + euro_stats.get('Total played', 0)

    for key in league_stats.keys():
        if key in ['rating', 'Pass accuracy', 'Dribbles', 'Accurate crosses', 'Accurate long balls']:
            # Weighted average for percentages and ratings
            league_weight = league_stats['Total played'] / total_appearances if total_appearances > 0 else 0
            euro_weight = euro_stats['Total played'] / total_appearances if total_appearances > 0 else 0
            
            if key == 'rating':
                value = round(league_stats[key] * league_weight + euro_stats[key] * euro_weight, 2)
                combined_stats[key] = 10 if abs(value - 10.0) < 0.0001 else value
            else:
                try:
                    # Decode percentage values
                    league_cumulative, league_percentage = decode_percentage_value(league_stats[key])
                    euro_cumulative, euro_percentage = decode_percentage_value(euro_stats[key])
                    
                    if league_percentage is not None and euro_percentage is not None:
                        # Combine cumulative values and calculate new percentage
                        total_cumulative = league_cumulative + euro_cumulative
                        weighted_percentage = (league_percentage * league_weight + euro_percentage * euro_weight)
                        combined_stats[key] = f"{round(total_cumulative, 2)}({round(weighted_percentage, 2)}%)"
                    else:
                        # Handle simple percentage values
                        league_value = float(league_stats[key].replace('%', ''))
                        euro_value = float(euro_stats[key].replace('%', ''))
                        combined_value = league_value * league_weight + euro_value * euro_weight
                        combined_stats[key] = f"{round(combined_value, 2)}%"
                except (IndexError, ValueError):
                    combined_stats[key] = league_stats[key]
        elif key in ['Minutes per game', 'Shots per game', 'Key passes', 'Tackles', 'Interceptions', 'Clearances', 'Was fouled', 'Fouls', 'Offsides']:
            # Weighted average for per game stats
            value = (league_stats[key] * league_stats['Total played'] + euro_stats[key] * euro_stats['Total played']) / total_appearances if total_appearances > 0 else 0
            combined_stats[key] = round(value, 2)
        else:
            # Sum for cumulative stats
            combined_stats[key] = league_stats[key] + euro_stats[key]

    return combined_stats

def parse_player_matches(matches_data, matches_played):
    # Filter out non-event types and sort by timestamp (most recent first)
    events = [match for match in matches_data if match['type'] == 'event']
    events.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Select matches from the current season
    current_season_matches = events[:matches_played]
    
    # Sort by rating and select the top 7
    best_matches = sorted(current_season_matches, key=lambda x: float(x['value']), reverse=True)[:7]
    
    parsed_matches = []
    for match in best_matches:
        rating = float(match['value'])
        # Convert rating to int if it's 10, otherwise round to 2 decimals
        rating = int(rating) if rating == 10 else round(rating, 2)
        
        parsed_matches.append({
            'date': datetime.fromtimestamp(match['timestamp']).strftime('%Y-%m-%d'),
            'rating': rating
        })
    
    return parsed_matches

def get_player_details(driver, player_id, max_retries=3):
    url = f"https://api.sofascore.com/api/v1/player/{player_id}"
    
    for attempt in range(max_retries):
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
            json_content = driver.find_element(By.TAG_NAME, "pre").text
            data = json.loads(json_content)
            
            player_data = data.get('player', {})
            details = {
                "contract": f"Contract until {time.strftime('%d %b %Y', time.localtime(player_data.get('contractUntilTimestamp', 0)))}",
                "nationality": player_data.get('country', {}).get('alpha3', '').lower(),
                "age": f"{calculate_age(player_data.get('dateOfBirthTimestamp', 0))} yrs",
                "height": f"{player_data.get('height', 0)} cm",
                "preferred foot": player_data.get('preferredFoot', '').lower(),
                "position": player_data.get('position', '').lower(),
                "shirt number": str(player_data.get('shirtNumber', '')),
                "value": str(player_data.get('proposedMarketValue', 0) // 1000000)
            }
            return details
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 3))
    
    print(f"Failed to fetch player details after {max_retries} attempts")
    return None

def calculate_age(birth_timestamp):
    birth_date = datetime.fromtimestamp(birth_timestamp)
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def scrape_player(driver, player_info, all_teams, all_players):
    player_name = player_info['name']
    team_name = player_info['team']
    
    try:
        player_id = get_player_id(player_name, all_players)
        if not player_id:
            print(f"Player {player_name} not found in all_players")
            return None

        team_data = all_teams.get(team_name)
        if not team_data:
            print(f"Team {team_name} not found in all_teams")
            return None

        info = {
            'name': player_name,
            'team': team_name,
            'league': player_info['league'],
            'category': player_info['category'],
            'position': player_info['position']
        }
        
        # Get player details
        try:
            player_details = get_player_details(driver, player_id)
            if player_details:
                info.update(player_details)
        except Exception as e:
            print(f"Error getting player details for {player_name}: {str(e)}")
            traceback.print_exc()

        # Get league and euro stats
        league_stats = None
        euro_stats = None
        
        # Get league stats
        league_id = team_data['league_id']
        league_season_id = team_data['league_season_id']
        if league_id and league_season_id:
            try:
                stats_data = get_player_stats(driver, player_id, league_id, league_season_id)
                if stats_data:
                    league_stats = parse_player_stats(stats_data)
                    print(f"League stats fetched for {player_name}")
            except Exception as e:
                print(f"Error getting league stats for {player_name}: {str(e)}")
                traceback.print_exc()

        # Get European competition stats if available
        euro_id = team_data['international_id']
        euro_season_id = team_data['international_season_id']
        if euro_id and euro_season_id:
            try:
                stats_data = get_player_stats(driver, player_id, euro_id, euro_season_id)
                if stats_data:
                    euro_stats = parse_player_stats(stats_data)
                    print(f"Euro stats fetched for {player_name}")
            except Exception as e:
                print(f"Error getting euro stats for {player_name}: {str(e)}")
                traceback.print_exc()

        # Update info with stats
        if league_stats and euro_stats:
            print(f"Combining stats for {player_name}")
            try:
                combined_stats = combine_stats(league_stats, euro_stats)
                info.update(combined_stats)
                print(f"Stats combined for {player_name}")
            except Exception as e:
                print(f"Error combining stats for {player_name}: {str(e)}")
                traceback.print_exc()
                # If combining fails, use league stats
                info.update(league_stats)
        elif league_stats:
            print(f"Using only league stats for {player_name}")
            info.update(league_stats)
        elif euro_stats:
            print(f"Using only euro stats for {player_name}")
            info.update(euro_stats)

        # Get match data
        try:
            matches_data = get_player_matches(driver, player_id)
            if matches_data and 'summary' in matches_data:
                matches_played = info.get('Total played', 0)
                info['matches'] = parse_player_matches(matches_data['summary'], matches_played)
                print(f"Match data processed for {player_name}")
        except Exception as e:
            print(f"Error getting match data for {player_name}: {str(e)}")
            traceback.print_exc()

        # Add FBRef data
        try:
            info = get_fbref_stats(player_info['name'], info)
            percentiles, attributes_list = get_fbref_percentiles(player_info['name'])
            info['percentiles'] = percentiles
            info['percentile_attributes'] = attributes_list
            matches, positions = get_best_matches_and_positions(info['matches'], player_info['name'], 25)
            info['matches'] = matches
            info['positions'] = positions
            print(f"FBRef data added for {player_name}")
        except Exception as e:
            print(f"Error getting FBRef data for {player_info['name']}: {str(e)}")
            traceback.print_exc()

        # Print final info structure before returning
        print(f"Final stats keys for {player_name}: {list(info.keys())}")
        return info

    except Exception as e:
        print(f"Unexpected error processing {player_name}: {str(e)}")
        traceback.print_exc()
        return None

def round_data_values(data):
    """Round all numerical values in the data dictionary."""
    def round_value(value):
        if isinstance(value, (int, float)):
            # Convert exactly 10.0 to 10 in ratings
            if abs(value - 10.0) < 0.0001:  # Using small epsilon for float comparison
                return 10
            # Round other floats to 2 decimal places
            if isinstance(value, float):
                return round(value, 2)
            return value
        elif isinstance(value, str):
            # Handle percentage strings and other numeric strings
            try:
                if '%' in value:
                    if '(' in value and ')' in value:
                        # Handle combined values like "123(45.67%)"
                        cumulative, percentage = decode_percentage_value(value)
                        return f"{round(cumulative, 2)}({round(percentage, 2)}%)"
                    else:
                        # Handle simple percentages
                        num = float(value.replace('%', ''))
                        return f"{round(num, 2)}%"
                elif 'min' in value:
                    num = float(value.replace(' min', ''))
                    return f"{round(num, 2)} min"
            except ValueError:
                pass
            return value
        return value

    # Process regular entries
    for key, value in data.items():
        if key != 'matches':  # Handle matches separately
            data[key] = round_value(value)
    
    # Process matches specifically
    if 'matches' in data and isinstance(data['matches'], list):
        for i, match in enumerate(data['matches']):
            if isinstance(match, list):
                # For list format matches
                for j, val in enumerate(match):
                    if isinstance(val, (int, float)):
                        match_value = round_value(val)
                        # Special handling for rating of exactly 10.0
                        if isinstance(val, float) and abs(val - 10.0) < 0.0001:
                            match_value = 10
                        data['matches'][i][j] = match_value
            elif isinstance(match, dict):
                # For dict format matches
                for key, val in match.items():
                    if isinstance(val, (int, float)):
                        match_value = round_value(val)
                        # Special handling for rating of exactly 10.0
                        if isinstance(val, float) and abs(val - 10.0) < 0.0001:
                            match_value = 10
                        data['matches'][i][key] = match_value
    
    return data

def save_player_data(player_name, data):
    # Round all numerical values before saving
    data = round_data_values(data)
    
    filename = f"players/{unidecode.unidecode(player_name)}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_fbref_stats(player, info, year=25):
    names = pd.read_csv('resources/NAME_DB.csv')

    names = names.set_index('Name')

    url = names.loc[player].values[1]

    url = url.split('/')

    name = url[4] + '-Domestic-League-Stats'

    url[4] = 'dom_lg'

    url[0] = 'https://fbref.com'

    url += ['2023-2024',name]

    url = '/'.join(url)

    match_log = pd.read_html(url)

    try:
        gsca = match_log[5]

        xga = match_log[1]

        xga.loc[:,"Progression"]
    except:
        # When the season is over the table indexed 0 of "Last 5 Matches disapears"
        gsca = match_log[4]

        xga = match_log[0]

    try:
        xga = xga.loc[:,'Unnamed: 0_level_0'].join(xga.loc[:,'Progression'].join(xga.loc[:,'Per 90 Minutes'].join(xga.loc[:,'Playing Time']))).fillna(0).set_index("Season").loc[f'20{year-1}-20{year}']
        
    except:
        xga = match_log[0]
        xga = xga.loc[:,'Unnamed: 0_level_0'].join(xga.loc[:,'Progression'].join(xga.loc[:,'Per 90 Minutes'].join(xga.loc[:,'Playing Time']))).fillna(0).set_index("Season").loc[f'20{year}']
    
    try: 
        gsca = gsca.loc[:,'Unnamed: 0_level_0'].join(gsca.loc[:,'SCA'].join(gsca.loc[:,'GCA'])).fillna(0).set_index('Season').loc[f'20{year-1}-20{year}']
    except:
        gsca = match_log[4]
        gsca = gsca.loc[:,'Unnamed: 0_level_0'].join(gsca.loc[:,'SCA'].join(gsca.loc[:,'GCA'])).fillna(0).set_index('Season').loc[f'20{year}']
        

    if type(xga) == pd.DataFrame:
        matches = float(xga.loc[:,'90s'].tolist()[-1])

        progresive_carries = float(xga.loc[:,'PrgC'].tolist()[-1]) 

        progresive_passes = float(xga.loc[:,'PrgP'].tolist()[-1]) 

        progresive_passes_rec = float(xga.loc[:,'PrgR'].tolist()[-1])

        npxg = float(xga.loc[:,'npxG'].tolist()[-1])

        xa = float(xga.loc[:,'xAG'].tolist()[-1])

        sca = float(gsca.loc[:,'SCA'].tolist()[-1])

        gca = float(gsca.loc[:,'GCA'].tolist()[-1])

    else:
        matches = float(xga.loc['90s'])

        progresive_carries = float(xga.loc['PrgC']) 

        progresive_passes = float(xga.loc['PrgP']) 

        progresive_passes_rec = float(xga.loc['PrgR'])

        npxg = float(xga.loc['npxG'])

        xa = float(xga.loc['xAG'])   
        
        sca = float(gsca.loc['SCA'])

        gca = float(gsca.loc['GCA'])



    url = url.replace('-Domestic-League-Stats','-International-Cup-Stats')

    match_log = pd.read_html(url)

    try:
        gsca = match_log[5]

        xga = match_log[1]

        xga.loc[:,"Progression"]
    except:
        # When the season is over the table indexed 0 of "Last 5 Matches disapears"
        gsca = match_log[4]

        xga = match_log[0]

    try:
        xga = xga.loc[:,'Unnamed: 0_level_0'].join(xga.loc[:,'Progression'].join(xga.loc[:,'Per 90 Minutes'].join(xga.loc[:,'Playing Time']))).fillna(0).set_index("Season").loc[f'20{year-1}-20{year}']
    except: # Brazilian League Exception
        xga = match_log[0]
        xga = xga.loc[:,'Unnamed: 0_level_0'].join(xga.loc[:,'Progression'].join(xga.loc[:,'Per 90 Minutes'].join(xga.loc[:,'Playing Time']))).fillna(0).set_index("Season").loc[f'20{year}']
    
    try:
        gsca = gsca.loc[:,'Unnamed: 0_level_0'].join(gsca.loc[:,'SCA'].join(gsca.loc[:,'GCA'])).fillna(0).set_index('Season').loc[f'20{year-1}-20{year}']
    except:
        gsca = match_log[4]
        gsca = gsca.loc[:,'Unnamed: 0_level_0'].join(gsca.loc[:,'SCA'].join(gsca.loc[:,'GCA'])).fillna(0).set_index('Season').loc[f'20{year}']

    if type(xga) == pd.DataFrame:
        matches += float(xga.loc[:,'90s'].tolist()[-1])

        progresive_carries += float(xga.loc[:,'PrgC'].tolist()[-1]) 

        progresive_passes += float(xga.loc[:,'PrgP'].tolist()[-1]) 

        progresive_passes_rec += float(xga.loc[:,'PrgR'].tolist()[-1])

        npxg += float(xga.loc[:,'npxG'].tolist()[-1])

        xa += float(xga.loc[:,'xAG'].tolist()[-1])

        sca += float(gsca.loc[:,'SCA'].tolist()[-1])

        gca += float(gsca.loc[:,'GCA'].tolist()[-1])

    else:
        matches += float(xga.loc['90s'])

        progresive_carries += float(xga.loc['PrgC']) 

        progresive_passes += float(xga.loc['PrgP']) 

        progresive_passes_rec += float(xga.loc['PrgR'])

        npxg += float(xga.loc['npxG'])

        xa += float(xga.loc['xAG'])

        sca += float(gsca.loc['SCA'])

        gca += float(gsca.loc['GCA'])

    info['Progressive carries per 90'] = round(progresive_carries  / matches,2)    

    info['Progressive passes per 90'] = round(progresive_passes / matches,2)

    info['Progressive passes recieved per 90'] = round(progresive_passes_rec / matches,2)

    info['npXG'] = round(npxg,2)

    info['XA'] = round(xa,2)

    info['SCA'] = round(sca / matches,2)

    info['GCA'] = round(gca / matches,2)

    return info

def get_fbref_percentiles(player, default=True, year=25):
    names = pd.read_csv('resources/NAME_DB.csv')
    names = names.set_index('Name')

    url = names.loc[player].values[1]
    url = url.split('/')
    name = url[4] + '-Scouting-Report'
    url[4] = 'scout'
    url[0] = 'https://fbref.com'
    url += ['365_m1', name]
    url = '/'.join(url)
    
    try:
        data = pd.read_html(url)[-1]
        data = data.loc[:,'Standard Stats']

        attributes = ['Goals', 'Assists', 'xG: Expected Goals', 'xAG: Exp. Assisted Goals', 'Progressive Carries', 'Progressive Passes', 'Progressive Passes Rec', 'Shots Total', 'Shots on Target', 'Shots on Target %', 'Goals/Shot', 'Passes Completed', 'Passes Attempted', 'Pass Completion %', 'Total Passing Distance', 'Progressive Passing Distance', 'xAG: Exp. Assisted Goals', 'xA: Expected Assists', 'Key Passes', 'Through Balls', 'Switches', 'Crosses', 'Shot-Creating Actions', 'Goal-Creating Actions', 'Tackles', 'Tackles Won', 'Dribblers Tackled', 'Blocks', 'Interceptions', 'Clearances', 'Errors', 'Touches', 'Take-Ons Attempted', 'Successful Take-Ons', 'Successful Take-On %', 'Carries', 'Progressive Carrying Distance', 'Progressive Carries', 'Miscontrols', 'Dispossessed', 'Progressive Passes Rec', 'Fouls Committed', 'Fouls Drawn', 'Ball Recoveries','Aerials Won', "% of Aerials Won"]

        ranks = data[data['Statistic'].isin(attributes)]
        ranks["Percentile"] = pd.to_numeric(ranks["Percentile"])
        ranks = ranks.drop_duplicates()

        ranks = ranks.loc[ranks['Percentile'] > 80].sort_values(by=['Percentile'], ascending=False)
        attributes = ranks['Statistic'].tolist()

        if len(attributes) < 10:
            ranks = data[data['Statistic'].isin(attributes)]
            ranks["Percentile"] = pd.to_numeric(ranks["Percentile"])
            ranks = ranks.drop_duplicates()
            ranks = ranks.loc[ranks['Percentile'] > 60].sort_values(by=['Percentile'], ascending=False)
            attributes = ranks['Statistic'].tolist()

        if default:
            attributes = attributes[:15]

        # Save ranks to CSV for debugging
        ranks.to_csv('ranks.csv', index=False)

        percentiles = ranks.set_index('Statistic').loc[attributes, 'Percentile'].tolist()
        attributes_list = [attribute.replace("Progressive", "Prog.") for attribute in attributes]

        return percentiles, attributes_list

    except Exception as e:
        print(f"Error in get_fbref_percentiles for {player}: {str(e)}")
        return [], []

def get_best_matches_and_positions(matches, player, year):
    names = pd.read_csv('resources/NAME_DB.csv')
    names = names.set_index('Name')
    try:
        url = names.loc[player].values[1]
    except:
        input(f"Add {player} to the NAME_DB")
        names = pd.read_csv('resources/NAME_DB.csv')
        names = names.set_index('Name')
        url = names.loc[player].values[1]

    url = url.split('/')
    name = url[4] + '-Match-Logs'
    url[4] = 'matchlogs'
    url[0] = 'https://fbref.com'
    url += [f'20{year-1}-20{year}', name]
    url = '/'.join(url)

    match_log = pd.read_html(url)
    match_log = match_log[0].loc[:, ['Unnamed: 0_level_0', 'Unnamed: 7_level_0', 'Unnamed: 9_level_0', 'Performance']]

    # Convert the list of dictionaries to a DataFrame
    matches_df = pd.DataFrame(matches)
    matches_df['Date'] = pd.to_datetime(matches_df['date'])
    matches_df['Rating'] = matches_df['rating'].astype(float)
    matches_df = matches_df.sort_values('Rating', ascending=False)

    ratings = matches_df['Rating'].tolist()
    selected_matches = matches_df['Date'].dt.strftime('%Y-%m-%d').tolist()

    # Rest of the function remains the same
    current = False
    e = 0
    while not current:
        if e >= len(selected_matches):
            break
        date = selected_matches[e]
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        if date_obj.year == year - 1 and date_obj.month <= 7:
            selected_matches.pop(e)
            ratings.pop(e)
        else:
            e += 1
        if e == len(selected_matches):
            current = True

    selected_matches = selected_matches[:8]
    ratings = ratings[:8]

    dates = match_log.loc[:, 'Unnamed: 0_level_0'].loc[:, 'Date'].tolist()
    opponent = match_log.loc[:, 'Unnamed: 7_level_0'].loc[:, 'Opponent'].tolist()
    gls = match_log.loc[:, 'Performance'].loc[:, 'Gls'].tolist()
    ast = match_log.loc[:, 'Performance'].loc[:, 'Ast'].tolist()
    positions = match_log.fillna('').loc[:, 'Unnamed: 9_level_0'].loc[:, 'Pos'].tolist()

    all_positions = []
    for pos in positions:
        if pos != '':
            if ',' in pos:
                all_positions += pos.split(",")
            else:
                all_positions += [pos]
    positions = [e for e in set(all_positions) if all_positions.count(e) >= 10]

    matches_result = []
    index = 0

    for date in selected_matches:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        try:
            fbref_index = dates.index(f'{date_obj.year}-{date_obj.month:02d}-{date_obj.day:02d}')
            matches_result += [unidecode.unidecode(opponent[fbref_index]), gls[fbref_index], ast[fbref_index], ratings[index]]
        except ValueError:
            try:
                fbref_index = dates.index(f'{date_obj.year}-{date_obj.month:02d}-{date_obj.day-1:02d}')
                matches_result += [unidecode.unidecode(opponent[fbref_index]), gls[fbref_index], ast[fbref_index], ratings[index]]
            except ValueError:
                pass
        index += 1
        if len(matches_result) == 5:
            break

    return matches_result, positions

def clean_script():
    destination_path = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Player Analysis/scripts/"
    index = len(os.listdir(f"{destination_path}video/"))
    if "script.txt" in os.listdir():
        shutil.copy2(os.getcwd()+"/script.txt",destination_path+f"video/script{index+1}.txt" )
    if "sort_script.txt" in os.listdir():
        shutil.copy2(os.getcwd()+"/sort_script.txt",destination_path+f"sorts/sort_script{index+1}.txt")

def make_post(player, positions, youngster, short_photo, short=False, year=24, translate=False, clone=False):
    with open(f'players/{player}.json') as json_file:
        data = json.load(json_file)
    matches = data['matches']
    info = [data['value'],data['height'].replace(' cm',''),data['age'].replace(' yrs',''),data['nationality'],data['team'],'right' == data['preferred foot'],data['positions']]
    if data['Total played'] == data['Started']:
        match = f"Matches played: {data['Total played']}"
    else:
        match = f"Matches played: {data['Total played']}({int(data['Started'])})"
    stats = [data['rating']]
    goals = float(data['Goals'])
    assists = float(data['Assists'])
    totw = float(data['Team of the week'])
    big_chances = float(data['Big chances created'])
    dribbles = data['Succ. dribbles']
    min_goal = data['Scoring frequency'].replace(" min",'')
    shots = data['Shots per game']
    shot_conv = data['Goal conversion'].replace('%','')
    shots_ot = float(data['Shots on target per game']) / float(shots)
    key_pases = data['Key passes']
    interceptions = data['Interceptions per game']
    crosses = data['Acc. crosses']
    recoveries = data['Balls recovered per game']
    clearences = data['Clearances per game']
    tackles = data['Tackles per game']
    big_chances_missed = float(data['Big chances missed'])
    sca = data['SCA']
    gca = data['GCA']
    proc = data['Progressive carries per 90']
    prop = data['Progressive passes per 90']
    propr = data['Progressive passes recieved per 90']
    offsides = data['Offsides']
    yellows = float(data['Yellow'])
    reds = float(data['Red cards'])
    pass_acuracy = data['Accurate per game'].split('(')[1].replace('%)','')
    offset = 0
    if data['position'] == 'f':
        stats += [match,f'Goals: {int(goals)}',f'Assists: {int(assists)}']
        if int(big_chances_missed) >= int(goals) and int(big_chances_missed)-int(big_chances) >= 0:
            stats += [f'Big Chances Miss: {int(big_chances_missed)}']
            offset += 1
        elif int(big_chances) >= 5:
            stats += [f'Big Chances: {int(big_chances)}']
            offset += 1
        if int(totw) >= 1:
            stats += [f'Team of the Week: {int(totw)}']
            if int(totw) >= 5:
                offset += 1
        if float(offsides) >= 0.8:
            stats += [f'Offsides: {offsides}']
        if float(gca) >= 0.6:
            stats += [f'Goal Creating Actions: {gca}']
            if float(sca) >= 6.0:
                stats.insert(3+offset,f'Shot Creating Actions: {sca}')
                offset += 1
        elif float(sca) >= 4.0:
            stats += [f'Shot Creating Actions: {sca}']
        if float(propr) >= 10:
            if float(propr) >= 15:
                stats.insert(3+offset,f'Prog. Passes Recieved: {propr}')
                offset += 1
            elif float(prop) >= 9:
                stats.insert(3+offset,f'Prog. Passes: {prop}')
                offset += 1
            elif float(proc) >= 6:
                stats.insert(3+offset,f'Prog. Carries: {proc}')
                offset += 1
            else:
                stats += [f'Prog. Passes Recieved: {propr}']  
        elif float(prop) >= 6:
            stats += [f'Prog. Passes: {prop}']
            if float(proc) >= 4:
                stats += [f'Prog. Carries: {proc}']
        if float(prop) >= 9:
                stats.insert(3+offset,f'Prog. Passes: {prop}')
                offset += 1
        if float(proc) >= 6:
            stats.insert(3+offset,f'Prog. Carries: {proc}')
            offset += 1
        if float(dribbles.split('(')[0]) >= 2.0 :
            if float(dribbles.split('(')[0]) >= 3.0 :
                stats.insert(3+offset,f'Dribbles: {dribbles}')
                offset += 1
            else:
                stats += [f'Dribbles: {dribbles}']
        if float(min_goal) <= 150:
            if float(min_goal) <= 100:
                stats.insert(3+offset,f'Minutes per goal: {min_goal} min')
                offset += 1
            else:
                stats += [f'Minutes per goal: {min_goal} min']
        if float(shots) >= 1.5:
            if float(shots) >= 2.25:
                stats.insert(3+offset,f'Shots: {shots}')
                offset += 1
            else:
                stats += [f'Shots: {shots}']
        if float(shot_conv) >= 20:
            if float(shot_conv) >= 30:
                stats.insert(3+offset,f'Goal convertion %: {shot_conv}%')
                offset += 1
            else:
                stats += [f'Goal convertion %: {shot_conv}%']
        if float(shots_ot) >= 45:
            if float(shots_ot) >= 67.5:
                stats.insert(3+offset,f'Shot on target %: {shots_ot}%')
                offset += 1
            else:
                stats += [f'Shot on target %: {shots_ot}%']
        if float(key_pases) >= 1.5:
            if float(key_pases) >= 2.25:
                stats.insert(3+offset,f'Key Passes: {key_pases}')
                offset += 1
            else:
                stats += [f'Key Passes: {key_pases}']
        if float(crosses.split('(')[0]) >= 4.5:
            if float(crosses.split('(')[0]) >= 6.75 or float(crosses.split("(")[1].replace('%)','')) >= 80:
                stats.insert(3+offset,f'Crosses: {crosses}')
                offset += 1
            else:
               stats += [f'Crosses: {crosses}']
        if len(stats) > 10:
            stats = stats[0:11]
        elif len(stats) < 10:
            if int(big_chances) >= 1:
                stats += [f'Big Chances: {int(big_chances)}']
            if float(sca) >= 3:
                stats += [f'Shot Creating Actions: {sca}']
            if float(gca) >= 0.45:
                stats += [f'Goal Creating Actions: {gca}']
            if float(proc) >= 2.5:
                stats += [f'Prog. Carries: {proc}']
            if float(prop) >= 4:
                stats += [f'Prog. Passes: {prop}']
            if float(dribbles.split('(')[0]) >= 1.5:
                stats += [f'Dribbles: {dribbles}']
            if float(min_goal) <= 200:
                stats += [f'Minutes per goal: {min_goal} min']
            
            stats += [f'Shots: {shots}',f'Goal convertion %: {shot_conv}%',f'Shot on target %: {shots_ot}%']
            stats = stats[0:11]
    elif data['position'] == 'm':
        if int(goals) + int(assists) >= 5:
            stats += [match,f'Goals: {int(goals)}',f'Assists: {int(assists)}']
        else:
            stats += [match,f'Goals and Assists: {int(goals)+int(assists)}']
            offset -= 1
        if int(big_chances) >= 5:
            stats += [f'Big Chances: {int(big_chances)}']
            offset += 1
        if int(totw) >= 1:
            stats += [f'Team of the Week: {int(totw)}']
            if int(totw) >= 5:
                offset += 1
        if float(pass_acuracy) >= 90:
            stats += [f'Pass accuracy: {pass_acuracy}%']
        if float(key_pases) >= 1.5:
            stats += [f'Key Passes: {key_pases}']
        if float(dribbles.split('(')[0]) >= 2.0 :
            if float(dribbles.split('(')[0]) >= 3.0 :
                stats.insert(3+offset,f'Dribbles: {propr}')
                offset += 1
            else:
                stats += [f'Dribbles: {dribbles}']
        if float(min_goal) <= 150:
            if float(min_goal) <= 100:
                stats.insert(3+offset,f'Minutes per goal: {min_goal} min')
                offset += 1
            else:
                stats += [f'Minutes per goal: {min_goal} min']
        if float(shots) >= 1.5:
            if float(shots) >= 2.25:
                stats.insert(3+offset,f'Shots: {shots}')
                offset += 1
            else:
                stats += [f'Shots: {shots}']
        if float(shot_conv) >= 20:
            if float(shot_conv) >= 30:
                stats.insert(3+offset,f'Goal convertion %: {shot_conv}%')
                offset += 1
            else:
                stats += [f'Goal convertion %: {shot_conv}%']
        if float(shots_ot) >= 45:
            if float(shots_ot) >= 67.5:
                stats.insert(3+offset,f'Shot on target %: {shots_ot}%')
                offset += 1
            else:
                stats += [f'Shot on target %: {shots_ot}%']
        if float(crosses.split('(')[0]) >= 4.5:
            if float(crosses.split('(')[0]) >= 6.75 or float(crosses.split("(")[1].replace('%)','')) >= 80:
                stats.insert(3+offset,f'Crosses: {crosses}')
                offset += 1
            else:
               stats += [f'Crosses: {crosses}']
        if float(interceptions) >= 1:
            if float(interceptions) >= 1.5:
                stats.insert(3+offset,f'Interceptions: {interceptions}')
                offset += 1
            else:
                stats += [f'Interceptions: {interceptions}']
        if float(tackles) >= 3:
            if float(tackles) >= 4.5:
                stats.insert(3+offset,f'Tackles: {tackles}')
                offset += 1
            else:
                stats += [f'Tackles: {tackles}']
        if float(clearences) >= 3:
            if float(clearences) >= 4.5:
                stats.insert(3+offset,f'Clearences: {clearences}')
                offset += 1
            else:
                stats += [f'Clearences: {clearences}']
        if float(recoveries) >= 2.5:
            if float(recoveries) >= 3.25:
                stats.insert(3+offset,f'Recoveries: {recoveries}')
                offset += 1
            else:
                stats += [f'Recoveries: {recoveries}']
        
        if len(stats) > 10:
            stats = stats[0:11]
        elif len(stats) < 10:
            if int(big_chances) >= 1:
                stats += [f'Big Chances: {int(big_chances)}']
            if float(sca) >= 3:
                stats += [f'Shot Creating Actions: {sca}']
            if float(gca) >= 0.45:
                stats += [f'Goal Creating Actions: {gca}']
            if float(proc) >= 2.5:
                stats += [f'Progresive Carries: {proc}']
            if float(prop) >= 4:
                stats += [f'Progresive Passes: {prop}']
            if float(key_pases) >= 1:
                stats += [f'Key Passes: {key_pases}']
            if float(pass_acuracy) >= 85:
                stats += [f'Pass accuracy: {pass_acuracy}%']
            if float(crosses.split('(')[0]) >= 3.5:
                stats += [f'Crosses: {crosses}']
            if float(recoveries) >= 2:
                stats += [f'Recoveries: {recoveries}']
            
            stats += [f'Key Passes: {key_pases}',f'Pass accurary: {pass_acuracy}%',f'Interceptions: {interceptions}']
            stats = stats[0:11]
    elif data['position'] == 'd':
        if int(goals) + int(assists) >= 5:
            stats += [match,f'Goals: {int(goals)}',f'Assists: {int(assists)}']
        else:
            stats += [match,f'Goals and Assists: {int(goals)+int(assists)}']
            offset -= 1
        if int(big_chances) >= 5:
            stats += [f'Big Chances: {int(big_chances)}']
            offset += 1
        if int(totw) >= 1:
            stats += [f'Team of the Week: {int(totw)}']
            if int(totw) >= 5:
                offset += 1
        if float(data['Clean sheets'])/int(data['Started']) >= 0.35:
            stats += [f'Clean Sheets: {int(data["Clean sheets"])}']
            offset += 1
        if int(yellows) >= int(data['Started'])/2:
            stats += [f'Yellow cards: {int(yellows)}']
        if int(reds)/int(data['Started']) >= 0.2:
            stats += [f'Red cards: {int(reds)}']
        if float(pass_acuracy) >= 90:
            stats += [f'Pass accuracy: {pass_acuracy}%']
        if float(key_pases) >= 1.5:
            stats += [f'Key Passes: {key_pases}']
        if float(dribbles.split('(')[0]) >= 2.0 :
            if float(dribbles.split('(')[0]) >= 3.0 :
                stats.insert(3+offset,f'Dribbles: {dribbles}')
                offset += 1
            else:
                stats += [f'Dribbles: {dribbles}']
        if float(min_goal) <= 150:
            if float(min_goal) <= 100:
                stats.insert(3+offset,f'Minutes per goal: {min_goal} min')
                offset += 1
            else:
                stats += [f'Minutes per goal: {min_goal} min']
        if float(shots) >= 1.5:
            if float(shots) >= 2.25:
                stats.insert(3+offset,f'Shots: {shots}')
                offset += 1
            else:
                stats += [f'Shots: {shots}']
        if float(shot_conv) >= 20:
            if float(shot_conv) >= 30:
                stats.insert(3+offset,f'Goal convertion %: {shot_conv}%')
                offset += 1
            else:
                stats += [f'Goal convertion %: {shot_conv}%']
        if float(shots_ot) >= 45:
            if float(shots_ot) >= 67.5:
                stats.insert(3+offset,f'Shot on target %: {shots_ot}%')
                offset += 1
            else:
                stats += [f'Shot on target %: {shots_ot}%']
        if float(crosses.split('(')[0]) >= 4.5:
            if float(crosses.split('(')[0]) >= 6.75 or float(crosses.split("(")[1].replace('%)','')) >= 80:
                stats.insert(3+offset,f'Crosses: {crosses}')
                offset += 1
            else:
               stats += [f'Crosses: {crosses}']
        if float(interceptions) >= 1:
            if float(interceptions) >= 1.5:
                stats.insert(3+offset,f'Interceptions: {interceptions}')
                offset += 1
            else:
                stats += [f'Interceptions: {interceptions}']
        if float(tackles) >= 3:
            if float(tackles) >= 4.5:
                stats.insert(3+offset,f'Tackles: {tackles}')
                offset += 1
            else:
                stats += [f'Tackles: {tackles}']
        if float(clearences) >= 3:
            if float(clearences) >= 4.5:
                stats.insert(3+offset,f'Clearences: {clearences}')
                offset += 1
            else:
                stats += [f'Clearences: {clearences}']
        if float(recoveries) >= 2.5:
            if float(recoveries) >= 3.25:
                stats.insert(3+offset,f'Recoveries: {recoveries}')
                offset += 1
            else:
                stats += [f'Recoveries: {recoveries}']
        
        
        if len(stats) > 10:
            stats = stats[0:11]
        elif len(stats) < 10:
            if int(big_chances) >= 1:
                stats += [f'Big Chances: {big_chances}']
            if float(key_pases) >= 1:
                stats += [f'Key Passes per game: {key_pases}']
            if float(crosses.split('(')[0]) >= 3.5:
                stats += [f'Crosses per game: {crosses}']
            if float(recoveries) >= 2:
                stats += [f'Recoveries per game: {recoveries}']
            if float(tackles) >= 2.5:
                stats += [f'Tackles per game: {tackles}']
            if float(clearences) >= 2.5:
                stats += [f'Clearences per game: {clearences}']
            stats += [f'Recoveries per game: {recoveries}',f'Tackles per game: {tackles}',f'Interceptions per game: {interceptions}']
            stats = stats[0:11]
    
    
    match_list = []
    for index in range(5):
        if matches[0+4*index][0].islower():
            matches[0+4*index] = matches[0+4*index].split(' ')[1]
        match_list += [[matches[0+4*index],int(matches[1+4*index]),int(matches[2+4*index]),float(matches[3+4*index])]]
    path = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/Video Output/"
    percentile = pd.DataFrame({"Statistic":data["percentile_attributes"],"Percentile":data["percentiles"]})
    clean_script()  # Add this line before make_script call
    make_script(player, stats, match_list)
    make_yt_videos(path, player, youngster, match_list, stats, info, positions, short_photo, short, percentile, translate, clone=clone)

def process_all_players(positions, short_photo, youngster=False, short=True, clone=True):
    next_players = load_next_players()
    all_teams = load_all_teams()
    all_players = load_all_players()
    next_players = [next_players[0]]  # For testing, only process first player

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-ssl-errors=yes")
    chrome_options.add_argument("--ignore-certificate-errors")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        for player_info in next_players:
            player_name = player_info['name']
            player = unidecode.unidecode(player_name)
            print(f"Processing {player_name}...")
            
            try:
                # Scrape player data
                player_data = scrape_player(driver, player_info, all_teams, all_players)
                if player_data:
                    # Save player data
                    save_player_data(player_name, player_data)
                    print(f"Data for {player_name} has been saved.")
                    
                    # Search for images
                    #ImageSearch(player)
                    
                    # Make post
                    make_post(player, positions, youngster=youngster, 
                            short_photo=short_photo, short=short, clone=clone)
                    
                    print(f"Post for {player_name} has been created.")
                else:
                    print(f"Failed to retrieve data for {player_name}")
            except Exception as e:
                print(f"Error processing {player_name}: {str(e)}")
                traceback.print_exc()
                
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Cleaning up...")
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting driver: {str(e)}")

if __name__ == "__main__":
    positions = {
        "V1": {"background": "top", "hook": "bottom"},
        "V2": {"background": "middle", "description": "bottom", "position": False}
    }
    short_photo = ['photo1', 'photo3']
    
    process_all_players(positions, short_photo, youngster=False, short=True, clone=False)