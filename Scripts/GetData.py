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
    parsed_stats = {
        'rating': stats.get('rating', 0),
        'Total played': stats.get('appearances', 0),
        'Started': stats.get('matchesStarted', 0),
        'Minutes per game': stats.get('minutesPlayed', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Goals': stats.get('goals', 0),
        'Assists': stats.get('assists', 0),
        'Yellow cards': stats.get('yellowCards', 0),
        'Red cards': stats.get('redCards', 0),
        'Shots per game': stats.get('shotsTotal', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Pass accuracy': f"{stats.get('passesAccuracy', 0)}%",
        'Key passes': stats.get('keyPasses', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Dribbles': f"{stats.get('dribbleSuccessful', 0)}({stats.get('dribbleSuccess', 0)}%)",
        'Tackles': stats.get('tackles', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Interceptions': stats.get('interceptions', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Big chances created': stats.get('bigChanceCreated', 0),
        'Accurate crosses': f"{stats.get('accurateCrosses', 0)}({stats.get('accurateCrossesPercentage', 0)}%)",
        'Accurate long balls': f"{stats.get('accurateLongBalls', 0)}({stats.get('accurateLongBallsPercentage', 0)}%)",
        'Clearances': stats.get('clearances', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Was fouled': stats.get('wasFouled', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Fouls': stats.get('fouls', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
        'Offsides': stats.get('offsides', 0) / stats.get('appearances', 1) if stats.get('appearances', 0) > 0 else 0,
    }
    return parsed_stats

def combine_stats(league_stats, euro_stats):
    combined_stats = {}
    total_appearances = league_stats.get('Total played', 0) + euro_stats.get('Total played', 0)

    for key in league_stats.keys():
        if key in ['rating', 'Pass accuracy', 'Dribbles', 'Accurate crosses', 'Accurate long balls']:
            # Weighted average for percentages and ratings
            league_weight = league_stats['Total played'] / total_appearances if total_appearances > 0 else 0
            euro_weight = euro_stats['Total played'] / total_appearances if total_appearances > 0 else 0
            
            if key == 'rating':
                combined_stats[key] = (league_stats[key] * league_weight + euro_stats[key] * euro_weight)
            else:
                try:
                    league_value = float(league_stats[key].split('(')[1].replace('%)', '')) if '(' in league_stats[key] else float(league_stats[key].replace('%', ''))
                    euro_value = float(euro_stats[key].split('(')[1].replace('%)', '')) if '(' in euro_stats[key] else float(euro_stats[key].replace('%', ''))
                    combined_value = league_value * league_weight + euro_value * euro_weight
                    combined_stats[key] = f"{combined_value:.1f}%"
                except (IndexError, ValueError):
                    # If we can't parse the percentage, just use the league value
                    combined_stats[key] = league_stats[key]
        elif key in ['Minutes per game', 'Shots per game', 'Key passes', 'Tackles', 'Interceptions', 'Clearances', 'Was fouled', 'Fouls', 'Offsides']:
            # Weighted average for per game stats
            combined_stats[key] = (league_stats[key] * league_stats['Total played'] + euro_stats[key] * euro_stats['Total played']) / total_appearances if total_appearances > 0 else 0
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
        parsed_matches.append({
            'date': datetime.fromtimestamp(match['timestamp']).strftime('%Y-%m-%d'),
            'rating': match['value']
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

        # Get league stats
        league_id = team_data['league_id']
        league_season_id = team_data['league_season_id']
        if league_id and league_season_id:
            try:
                stats_data = get_player_stats(driver, player_id, league_id, league_season_id)
                if stats_data:
                    info['league_stats'] = parse_player_stats(stats_data)
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
                    info['euro_stats'] = parse_player_stats(stats_data)
            except Exception as e:
                print(f"Error getting euro stats for {player_name}: {str(e)}")
                traceback.print_exc()

        # Combine stats if both league and euro stats are available
        if 'league_stats' in info and 'euro_stats' in info:
            try:
                info['combined_stats'] = combine_stats(info['league_stats'], info['euro_stats'])
            except Exception as e:
                print(f"Error combining stats for {player_name}: {str(e)}")
                traceback.print_exc()

        # Get match data
        try:
            matches_data = get_player_matches(driver, player_id)
            matches_played = info.get('combined_stats', info.get('league_stats', {})).get('Total played', 0)
            info['matches'] = parse_player_matches(matches_data['summary'], matches_played)
        except Exception as e:
            print(f"Error getting match data for {player_name}: {str(e)}")
            traceback.print_exc()

        # After getting all Sofascore data, add FBRef data
        try:
            # Add FBRef stats
            info = get_fbref_stats(player_info['name'], info)
            
            # Add FBRef percentiles
            percentiles, attributes_list = get_fbref_percentiles(player_info['name'])
            info['percentiles'] = percentiles
            info['percentile_attributes'] = attributes_list
            
            # Update matches with FBRef data
            matches, positions = get_best_matches_and_positions(info['matches'], player_info['name'], 25)  # Assuming current year is 2025
            info['matches'] = matches
            info['positions'] = positions
        except Exception as e:
            print(f"Error getting FBRef data for {player_info['name']}: {str(e)}")
            traceback.print_exc()

        return info

    except Exception as e:
        print(f"Unexpected error processing {player_name}: {str(e)}")
        traceback.print_exc()
        return None

def save_player_data(player_name, data):
    filename = f"players/{unidecode.unidecode(player_name)}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_all_players():
    next_players = load_next_players()
    all_teams = load_all_teams()
    all_players = load_all_players()
    next_players = [next_players[0]]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-ssl-errors=yes")
    chrome_options.add_argument("--ignore-certificate-errors")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        for player_info in next_players:
            print(f"Processing {player_info['name']}...")
            try:
                player_data = scrape_player(driver, player_info, all_teams, all_players)
                if player_data:
                    save_player_data(player_info['name'], player_data)
                    print(f"Data for {player_info['name']} has been saved.")
                else:
                    print(f"Failed to retrieve data for {player_info['name']}")
            except Exception as e:
                print(f"Error processing {player_info['name']}: {str(e)}")
                traceback.print_exc()
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Cleaning up...")
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting driver: {str(e)}")

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

if __name__ == "__main__":
    process_all_players()
