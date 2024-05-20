from playwright.sync_api import sync_playwright
import time
import shutil
import json
import pandas as pd
import os
import unidecode
from ScriptWriter import make_script
from MakePosts import make_ig_posts, make_yt_videos
import datetime
import sys


# This makes the code think is in the root folder. Only done for organizing
sys.path.append("C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code")


# Para el funcionamient es necesario NAME_DB.csv


delay = 0

player_list = ['Alexander Sørloth']

 

def scrape_player_list(player_list,delay, post=True,youngster=True, year=24,positions={'V1':{'background':'middle','hook':'top'},'V2':{'background':'middle','description':'top','position':'bottom'},'V3':{'background':'middle'}},short_photo=['photo1','photo2'],short=True,verbose = True, translate = False,clone=False):

    with sync_playwright() as p:

        #browser = p.chromium.launch()

        browser = p.chromium.launch(headless=False, slow_mo=500)

        page = browser.new_page()

        page.goto("https://sofascore.com")

        time.sleep(4+delay)

        for e in range(3):

            page.keyboard.press("Tab")

        page.keyboard.press("Enter")

        for player in player_list:
            scrape_player(player, page, year)
    if post:
        clean_script()
        player = unidecode.unidecode(player)
        make_post(player,positions,youngster,short_photo,short,year=year,translate=translate,clone=clone)


def scrape_player(player,page, verbose=True, year = 24):

    info = {}
    old_player = player
    player = unidecode.unidecode(player)
    player_file = "players/"+ player + ".json"

    with open(player_file, "w") as f:

        time.sleep(delay)

        page.click('//*[@id="__next"]/header/div[1]/div/div/div[2]/div/form')

        page.fill('//*[@id="__next"]/header/div[1]/div/div/div[2]/div/form/input',player)

        page.keyboard.press("ArrowDown")

        time.sleep(3+delay)

        page.keyboard.press("Enter")

        time.sleep(delay)

        print("done")

        time.sleep(6)

        # Get the general info
        profile = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]').all_inner_texts()

        contract = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/a/div/div').all_inner_texts()

        value = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[3]/div/div[1]/div[2]').all_inner_texts()

        position = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[5]/div/div[2]').all_inner_texts()

        positions = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[4]/div/div[2]/svg/g[2]').all_inner_texts()

        contract = contract[0]

        profile = profile[0]

        value = value[0]

        contract = contract.split('\n')

        info['team'] = contract[0]

                      
        info['matches'], info['positions'] = get_best_matches_and_positions(matches_sofascore(page),old_player,year)
        
        info['contract'] = contract[1]

        profile = profile.lower().split('\n')
        profile[2] = 'age'

        for e in range(len(profile)//2):

            info[profile[e*2]] = profile[e*2+1]

        if 'M' in value:

            value = value.split("M")[0]            

        elif 'K' in value:

            value = value.split('K')[0]

        info['value'] = value  

        info = get_stats(info,old_player,page,year)
        
        info['percentiles'],info['statistics'] = get_fbref_percentiles(old_player,not verbose, year)

        json.dump(info,f)

def clean_script():
    destination_path = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Player Analysis/scripts/"
    index = len(os.listdir(f"{destination_path}video/"))
    if "script.txt" in os.listdir():
        shutil.copy2(os.getcwd()+"/script.txt",destination_path+f"video/script{index+1}.txt" )
    if "sort_script.txt" in os.listdir():
        shutil.copy2(os.getcwd()+"/sort_script.txt",destination_path+f"sorts/sort_script{index+1}.txt")

def get_best_matches_and_positions(matches,player, year):

    names = pd.read_csv('resources/NAME_DB.csv')

    names = names.set_index('Name')

    url = names.loc[player].values[1]

    url = url.split('/')

    name = url[4] + '-Match-Logs'
    url[4] = 'matchlogs'

    url[0] = 'https://fbref.com'

    url += ['2023-2024',name]

    url = '/'.join(url)

    match_log = pd.read_html(url)

    match_log = match_log[0].loc[:,['Unnamed: 0_level_0','Unnamed: 7_level_0','Unnamed: 9_level_0','Performance']]

    matches = pd.DataFrame({'Date':matches[0],'Rating':matches[1]})

    matches['Rating'] = matches['Rating'].astype(float)

    matches = matches.sort_values('Rating',ascending=False)

    ratings = matches.loc[:,'Rating'].tolist()

    selected_matches = matches.loc[:,'Date'].tolist()

    current = False
    e = 0
    while not current:
        if "/" in selected_matches[e]:
            if (selected_matches[e].split("/")[2][:2] == (year - 1) and int(selected_matches[e].split("/")[1]) <= 7) or "/" not in selected_matches[e]:
                selected_matches.remove(selected_matches[e])
                ratings.remove(ratings[e])
        else:
            if 'T' in selected_matches[e].split("\n")[1]:
                if datetime.datetime.now().replace(hour =int(selected_matches[e].split("\n")[0].split(":")[0]),minute=int(selected_matches[e].split('\n')[0].split(":")[1])) <= datetime.datetime.now():
                    pass
                else:
                    selected_matches.remove(selected_matches[e])
                    ratings.remove(ratings[e])
            else:
                selected_matches.remove(selected_matches[e])
                ratings.remove(ratings[e])
        e += 1
        if e == len(selected_matches):
            current = True

    selected_matches = selected_matches[0:5]

    ratings = ratings[0:5]

    dates = match_log.loc[:,'Unnamed: 0_level_0'].loc[:,'Date'].tolist()

    opponent = match_log.loc[:,'Unnamed: 7_level_0'].loc[:,'Opponent'].tolist()

    gls = match_log.loc[:,'Performance'].loc[:,'Gls'].tolist()

    ast = match_log.loc[:,'Performance'].loc[:,'Ast'].tolist()

    positions = match_log.fillna('').loc[:,'Unnamed: 9_level_0'].loc[:,'Pos'].tolist()
    
    all_positions = []
    for pos in positions:
        if pos != '':
            if ',' in pos:
                all_positions += pos.split(",")
            else:
                all_positions += [pos]
    positions = []
    for e in set(all_positions):
        if all_positions.count(e) >= 10:
            positions += [e]

    matches = []

    match_log = match_log.iloc[1]

    index = 0

    for date in selected_matches:
        if '/' not in date:
            today = datetime.datetime.now()
            date = [str(today.day),str(today.month),str(today.year-2000)]
        else:
            date = date.split('/')

        try:
            fbref_index = dates.index(f'20{date[2][:2]}-{date[1]}-{date[0]}')
            matches += [unidecode.unidecode(opponent[fbref_index]),gls[fbref_index],ast[fbref_index],ratings[index]]
        except:
            try:
                fbref_index = dates.index(f'20{date[2][:2]}-{date[1]}-{int(date[0])-1}')
                matches += [unidecode.unidecode(opponent[fbref_index]),gls[fbref_index],ast[fbref_index],ratings[index]]
            except:
                pass
        index += 1

    return matches, positions

def matches_sofascore(page):
    ratings = []
    dates = []
    num = 0
    for e in range(0,5):
        while True:
            try:
                rating = page.locator(f'//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{num}]/a/div/div/div[6]/div/button/div/div/span/div/span').all_inner_texts()
                if rating == []:
                    rating = page.locator(f'//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{num}]/a/div/div/div[6]/div/button/div/div/span').all_inner_texts()
                date = page.locator(f'//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{num}]/a/div/div/div[2]').all_inner_texts()
                if rating != []:
                    ratings += [rating[0]]
                    dates += [date[0]]
                num += 1
                if num > 15:
                    num = 0
                    break
            except:
                num = 0
                break
        page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/button').click()

        time.sleep(5)
    return [dates,ratings]
   
def combine_sofascore_data_2(info,int_stats, int_rating, int_stats2, int_rating2, league_rating, league_stats, league_rating2, league_stats2):
    with open('resources/All_Atributes.json','r') as f:
        stats = json.load(f)
    attributes = stats.keys()
    match90slist = []
    for competition in [int_stats,int_stats2,league_stats,league_stats2]:
        if competition != '':
            stats['Total played'] += int(competition[competition.index('Total played')+1])
            stats['Started'] += float(competition[competition.index('Started')+1])
            stats['Minutes per game'] += float(competition[competition.index('Minutes per game')+1])*int(competition[competition.index('Total played')+1])
            match90slist += [(float(competition[competition.index('Minutes per game')+1])* float(competition[competition.index('Total played')+1])/90)]    
    match90stotal = stats['Minutes per game'] / 90
    stats['Minutes per game'] = match90stotal * 90 / stats['Total played']
    attributes = list(attributes)
    attributes.remove('Total played')
    attributes.remove('Started')
    attributes.remove( 'Minutes per game')
    
    for attribute in attributes:
        competitions =[int_stats,int_stats2,league_stats,league_stats2]
        competitions_it = []
        float_value, int_value = 0,0
        for e in range(4):
            if attribute in competitions[e]:
                competitions_it += [competitions[e]]
                competition = competitions[e]
        competitions = competitions_it
        for competition in competitions:
            attribute_value = competition[competition.index(attribute)+1]
            if '(' in attribute_value:

                stat_type = 1
                float_num = float(attribute_value.split('(')[0])
                int_num = float(attribute_value.split('(')[1].replace('%)',''))
                float_value += float_num * match90slist[competitions.index(competition)]
                int_value += int_num * match90slist[competitions.index(competition)]

            elif '/' in attribute_value:

                stat_type = 2
                float_num = float(attribute_value.split('/')[0])
                int_num = float(attribute_value.split('/')[1])
                float_value += float_num * match90slist[competitions.index(competition)]
                int_value += int_num * match90slist[competitions.index(competition)]

            elif '%' in attribute_value:

                stat_type = 3
                int_num = float(attribute_value.replace('%','')) 
                stats[attribute] += int_num * match90slist[competitions.index(competition)]

            elif ' min' in attribute_value:

                stat_type = 4
                int_num = float(attribute_value.replace(' min','')) 
                stats[attribute] += int_num * match90slist[competitions.index(competition)]

            elif 'per game' in attribute or attribute in ['Touches','Key passes','Possession won','Possession lost','Fouls','Offsides','Was fouled']:
                
                stat_type = 5
                int_num = float(attribute_value)
                stats[attribute] += int_num * match90slist[competitions.index(competition)]
            elif competition[e*2] == 'Yellow-Red':
                stat_type =0
                stats['Red'] += float(attribute_value)
            else:
                stat_type =0
                int_num = float(attribute_value)            
                stats[attribute] += int_num

        if stat_type == 1:
            stats[attribute] = f'{round(float_num/90,2)}({round(int_num/90,1)}%)'
        elif stat_type == 2:
            stats[attribute] = f'{round(float_num,0)}/{round(int_num,0)}'
        elif stat_type == 3:
            stats[attribute] = f'{round(stats[attribute]/match90stotal,1)}%'
        elif stat_type == 4:
            stats[attribute] = f'{round(stats[attribute]/match90stotal,2)} min'
        elif stat_type == 5:
            stats[attribute] = f'{round(stats[attribute]/match90stotal,2)}'
            
    rating_average = 0
    ratings =[int_rating,int_rating2,league_rating,league_rating2]
    rating_it = [int_rating,int_rating2,league_rating,league_rating2]
    for rating in rating_it:
        if rating == '':
            ratings.remove(rating)
    for rating in ratings:
        rating_average += float(rating) * match90slist[ratings.index(rating)] 
    info['rating'] = round(rating_average/match90stotal,2)
    info.update(stats)

    return info 
  

def get_fbref_stats(player,info,year=24):

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

    gsca = match_log[5]

    xga = match_log[1]


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

    gsca = match_log[5]

    xga = match_log[1]

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

def get_sofascore_stats(info,page,year=24):

    # Get the competitions stats

    league_botton = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/button')

    league_botton.click()

    drop_down = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/ul').all_inner_texts()[0]

    drop_down= drop_down.split('\n')

    int_stats, int_rating, int_stats2, int_rating2, league_rating, league_stats, league_rating2, league_stats2 = '','','','','','','',''

    # Get league stats

    for e in drop_down:

        if e in ['UEFA Europa Conference League','UEFA Champions League','UEFA Europa League','CONMEBOL Libertadores','CONMEBOL Sudamericana','European Championship, Qualification']:

            element = page.locator(f'//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/ul/li[{drop_down.index(e)+1}]')
                         
            element.click()

            period = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/button').all_inner_texts()[0]

            if period in [f'{year-1}/{year}',f'20{year}']:

                    if int_stats == '' and int_rating == '':

                        int_stats = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[5]').all_inner_texts()[0].split('\n')

                        int_rating = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[2]/div/div/span/div/span').all_inner_texts()[0]

                        for e in ["Other","Cards","Passing","Defending","Attacking","Matches"]:

                            int_stats.remove(e)

                    else:

                        int_stats2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[5]').all_inner_texts()[0].split('\n')

                        int_rating2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[2]/div/div/span/div/span').all_inner_texts()[0]

                        for e in ["Other","Cards","Passing","Defending","Attacking","Matches"]:

                            int_stats2.remove(e)

            league_botton.click()

        elif e in ['Premier League','LaLiga','Bundesliga','Serie A','Ligue 1','Eredivisie','Brasileirão Série A','Pro League','Liga Portugal Betclic','Liga Profesional de Fútbol','Trendyol Süper Lig']:

            element = page.locator(f'//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/ul/li[{drop_down.index(e)+1}]')

            element.click() 

            period = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/button').all_inner_texts()[0]

            if period in [f'{year-1}/{year}',f'20{year}']:

                    if league_stats == '' and league_rating == '':

                        league_stats = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[5]').all_inner_texts()[0].split('\n')

                        league_rating = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[2]/div/div/span/div/span').all_inner_texts()[0]

                        for e in ["Other","Cards","Passing","Defending","Attacking","Matches"]:

                            league_stats.remove(e)

                    else:

                        league_stats2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[5]').all_inner_texts()[0].split('\n')

                        league_rating2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[2]/div/div/span/div/span').all_inner_texts()[0]

                        for e in ["Other","Cards","Passing","Defending","Attacking","Matches"]:

                            league_stats2.remove(e)

            league_botton.click()
        
        
    return combine_sofascore_data_2(info, int_stats, int_rating, int_stats2, int_rating2, league_rating, league_stats, league_rating2, league_stats2)

def get_stats(info,player,page,year=24):
    return get_sofascore_stats(get_fbref_stats(player,info,year),page,year)
    
def get_fbref_percentiles(player,default=True,year=24):
    names = pd.read_csv('resources/NAME_DB.csv')

    names = names.set_index('Name')

    url = names.loc[player].values[1]

    url = url.split('/')

    name = url[4] + '-Scouting-Report'

    url[4] = 'scout'

    url[0] = 'https://fbref.com'

    url += ['365_m1',name]

    url = '/'.join(url)
    
    data = pd.read_html(url)[-1]

    data = data.loc[:,'Standard Stats']

    attributes = ['Goals', 'Assists', 'xG: Expected Goals', 'xAG: Exp. Assisted Goals', 'Progressive Carries', 'Progressive Passes', 'Progressive Passes Rec', 'Shots Total', 'Shots on Target', 'Shots on Target %', 'Goals/Shot', 'Passes Completed', 'Passes Attempted', 'Pass Completion %', 'Total Passing Distance', 'Progressive Passing Distance', 'xAG: Exp. Assisted Goals', 'xA: Expected Assists', 'Key Passes', 'Through Balls', 'Switches', 'Crosses', 'Shot-Creating Actions', 'Goal-Creating Actions', 'Tackles', 'Tackles Won', 'Dribblers Tackled', 'Blocks', 'Interceptions', 'Clearances', 'Errors', 'Touches', 'Take-Ons Attempted', 'Successful Take-Ons', 'Successful Take-On %', 'Carries', 'Progressive Carrying Distance', 'Progressive Carries', 'Miscontrols', 'Dispossessed', 'Progressive Passes Rec', 'Fouls Committed', 'Fouls Drawn', 'Ball Recoveries','Aerials Won', "% of Aerials Won"]

    row_position = {'Goals':0, 'Assists':1, 'Goals + Assists':2, 'Non-Penalty Goals':3, 'xG: Expected Goals':8, 'npxG: Non-Penalty xG':9, 'xAG: Exp. Assisted Goals':10, 'npxG + xAG':11,  'Progressive Carries':13, 'Progressive Passes':14, 'Progressive Passes Rec':15,  'Shots Total':19, 'Shots on Target':20, 'Shots on Target %':21, 'Goals/Shot':22, 'Goals/Shot on Target':23, 'npxG/Shot':31, 'Goals - xG':32, 'Passes Completed':36, 'Passes Attempted':37, 'Pass Completion %':38, 'Total Passing Distance':39, 'Progressive Passing Distance':40, 'xA: Expected Assists':55, 'Key Passes':56, 'Passes into Final Third':57, 'Passes into Penalty Area':58, 'Crosses into Penalty Area':59, 'Progressive Passes':60, 'Passes Attempted':63, 'Through Balls':68, 'Switches':69, 'Crosses':70, 'Passes Completed':78, 'Shot-Creating Actions':83, 'Goal-Creating Actions':92, 'Tackles':102, 'Tackles Won':103, 'Dribblers Tackled':108, 'Blocks':113, 'Interceptions':117, 'Clearances':119, 'Errors':120, 'Touches':123, 'Take-Ons Attempted':131, 'Successful Take-Ons':132, 'Successful Take-On %':133, 'Carries':137, 'Total Carrying Distance':138, 'Progressive Carrying Distance':139, 'Carries into Final Third':142, 'Carries into Penalty Area':143, 'Fouls Committed':154, 'Fouls Drawn':155, 'Crosses':157, 'Interceptions':159, 'Tackles Won':160, 'Penalty Kicks Won':161, 'Ball Recoveries':164,'Aerials Won':166, '% of Aerials Won':168}
    
    match_log = data

    ranks = match_log[match_log['Statistic'].isin(attributes)]

    ranks["Percentile"] = pd.to_numeric(ranks["Percentile"])

    ranks = ranks.drop_duplicates()

    match_log = match_log.drop_duplicates()

    ranks = ranks.loc[ranks['Percentile'] > 80].sort_values(by=['Percentile'],ascending=False)

    attributes = ranks.loc[:,'Statistic'].tolist()

    if len(attributes) < 10:
        attributes = ['Goals', 'Assists', 'Goals + Assists', 'Non-Penalty Goals', 'xG: Expected Goals', 'npxG: Non-Penalty xG', 'xAG: Exp. Assisted Goals', 'npxG + xAG',  'Progressive Carries', 'Progressive Passes', 'Progressive Passes Rec',  'Shots Total', 'Shots on Target', 'Shots on Target %', 'Goals/Shot', 'Goals/Shot on Target', 'npxG/Shot', 'Goals - xG', 'Passes Completed', 'Passes Attempted', 'Pass Completion %', 'Total Passing Distance', 'Progressive Passing Distance',  'xAG: Exp. Assisted Goals', 'xA: Expected Assists', 'Key Passes', 'Passes into Final Third', 'Passes into Penalty Area', 'Crosses into Penalty Area', 'Progressive Passes', 'Passes Attempted', 'Through Balls', 'Switches', 'Crosses', 'Passes Completed', 'Shot-Creating Actions', 'Goal-Creating Actions', 'Tackles', 'Tackles Won', 'Dribblers Tackled', 'Challenges Lost', 'Blocks', 'Interceptions', 'Clearances', 'Errors', 'Touches', 'Take-Ons Attempted', 'Successful Take-Ons', 'Successful Take-On %', 'Carries', 'Total Carrying Distance', 'Progressive Carrying Distance', 'Progressive Carries', 'Carries into Final Third', 'Carries into Penalty Area', 'Progressive Passes Rec', 'Fouls Committed', 'Fouls Drawn', 'Crosses', 'Interceptions', 'Tackles Won', 'Penalty Kicks Won', 'Ball Recoveries','Aerials Won', '% of Aerials Won']

        match_log = data

        ranks = match_log[match_log['Statistic'].isin(attributes)]

        ranks["Percentile"] = pd.to_numeric(ranks["Percentile"])

        ranks = ranks.drop_duplicates()

        match_log = match_log.drop_duplicates()

        ranks = ranks.loc[ranks['Percentile'] > 60].sort_values(by=['Percentile'],ascending=False)

        attributes_two = ranks.loc[:,'Statistic'].tolist()
        attributes_two = [item for item in attributes_two if item not in attributes]
        if len(attributes_two) == 10:
            attributes += attributes_two[:10]
        else:
            attributes += attributes_two
    if not default:
        top_attributes = ranks.loc[:,"Statistic"].tolist()
        ranks = ranks.set_index('Statistic')
        inputtext = f'This are the top inputs put the number of the ones you want to select in this way (1,2,3,...)\n\n'
        for attribute in top_attributes:
            inputtext += f'{1+top_attributes.index(attribute)}. {attribute}:{ranks.loc[attribute,"Percentile"]}\t'
        answer = input(inputtext+'Attributes selected: ').split(',')
        attributes = [top_attributes[int(x)-1] for x in answer]
    else:
        attributes = attributes[:15]
    try:
        percentiles = ranks.loc[attributes,'Percentile'].set_index("Statistic").tolist()
    except:
        percentiles = ranks.loc[attributes,'Percentile'].tolist()
    attributes_list = []
    for attribute in attributes:
        attributes_list += [attribute.replace("Progressive","Prog.")]
    return percentiles, attributes_list
    
def make_post(player,positions, youngster,short_photo,short=False,year = 24, translate = False,clone=False):
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
    percentile = pd.DataFrame({"Statistic":data["statistics"],"Percentile":data["percentiles"]})
    make_script(player,stats,match_list)
    make_yt_videos(path,player,youngster,match_list,stats,info,positions,short_photo,short,percentile,translate,clone=clone)
 

positions={
"V1":{"background":"middle","hook":"bottom"},
"V2":{"background":"middle","description":"bottom","position":False}
}
short_photo = ['photo1','photo2']
player = unidecode.unidecode(player_list[0])
#scrape_player_list(player_list,0.3,post=True,youngster=False,positions=positions,short_photo=short_photo,clone=True)
make_post(player,positions,youngster=False,short_photo=short_photo,short=True,clone=True)

