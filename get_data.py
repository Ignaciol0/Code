from playwright.sync_api import sync_playwright
import time

import json
import pandas as pd

from make_posts import make_posts



# Para el funcionamient es necesario NAME_DB.csv


delay = 0

player_list = ['Matías Soulé','Albert Guðmundsson']

def scrape_player_list(player_list,delay, post=True):

    with sync_playwright() as p:

        #browser = p.chromium.launch()

        browser = p.chromium.launch(headless=False, slow_mo=500)

        page = browser.new_page()

        page.goto("https://sofascore.com")

        time.sleep(4+delay)

        for e in range(3):

            page.keyboard.press("Tab")

        page.keyboard.press("Enter")

        for e in player_list:

            scrape_player(e, page)
            if post:
                make_post(e)


def scrape_player(e,page, year = 24):

    player = e

    info = {}

    title = e + ".json"

    with open(title, "w") as f:

        time.sleep(delay)

        page.click('//*[@id="__next"]/header/div[1]/div/div/div[2]/div/form')

        page.fill('//*[@id="__next"]/header/div[1]/div/div/div[2]/div/form/input',e)

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

        matches1 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[2]').all_inner_texts()

        page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/button').click()

        time.sleep(5)

        matches2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[2]').all_inner_texts()

        page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/button').click()

        time.sleep(5)

        matches3 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[2]').all_inner_texts()
        

        contract = contract[0]

        profile = profile[0]

        matches = matches1[0] + "\n" + matches2[0] + '\n' + matches3[0] 

        value = value[0]

        contract = contract.split('\n')

        info['team'] = contract[0]

        matches = matches.replace('\nSofasco','@')

        matches = matches.replace('FT\n','')

        matches = matches.replace('Int. Friendly Games\n','')

        matches = matches.replace('Club Friendly Games\n','')

        # This is done because some teams with long names like Bayern Leverkusen are reduced to an abreviated name
        pre_lenght = len(matches)
        matches = matches.replace(f'{contract[0]}\n','')
        if pre_lenght == len(matches):
            matches = matches.replace(f'{contract[0].split(" ")[-1]}\n','')

        league_botton = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/button')

        league_botton.click()

        drop_down = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/ul').all_inner_texts()[0]

        drop_down = drop_down.split('\n')

        elemento = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/ul/li[1]')

        elemento.click()

        for element in drop_down:

            matches = matches.replace(f'{element}\n','')

        matches = matches.split('\n')
        games = []
        

        for e in matches:

            if '@' not in e:

                if ('.' in e and e.replace('.','',1).isdigit()) or '/' in e or e.isalpha() or ' ' in e:

                    games += [e]

        matches_list = []

        for e in range(len(games)-2):

            if '/' in games[e] and (games[e+1].isalpha() or ' ' in games[e+1]) and '.' in games[e+2]:

                matches_list += [[games[e],games[e+1],games[e+2]]]

        info['matches'] = get_best_matches(matches_list,player)
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

        #nation = nation.split('src="')[1].split('"')[0]

        #info['nationality'] = nation.split('/')[-1].split('.')[0]


        info = get_stats(info,player,page)

        try:

            info['positions'] = position[0].split('\n')

        except:
            info['positions'] = position


        json.dump(info,f)


def get_best_matches(matches,player):

    names = pd.read_csv('NAME_DB.csv')

    names = names.set_index('Name')

    url = names.loc[player].values[1]

    url = url.split('/')

    name = url[4] + '-Match-Logs'

    url[4] = 'matchlogs'

    url[0] = 'https://fbref.com'

    url += ['2023-2024',name]

    url = '/'.join(url)

    match_log = pd.read_html(url)

    match_log = match_log[0].loc[:,['Unnamed: 0_level_0','Performance']]

    matches = pd.DataFrame(matches,columns=['Date','Opponent','Rating'])

    matches = matches.sort_values('Rating',ascending=False)

    ratings = matches.loc[:,'Rating'].tolist()

    opponent = matches.loc[:,'Opponent'].tolist()

    selected_matches = matches.loc[:,'Date'].tolist()

    current = False
    e = 0
    while not current:
        if selected_matches[e].split("/")[2] == '23' and int(selected_matches[e].split("/")[1]) <= 7:
            selected_matches.remove(selected_matches[e])
            ratings.remove(ratings[e])
            opponent.remove(opponent[e])

        e += 1
        if e == len(selected_matches):
            current = True

    selected_matches = selected_matches[0:3]

    opponent = opponent[0:3]

    ratings = ratings[0:3]

    dates = match_log.loc[:,'Unnamed: 0_level_0'].loc[:,'Date'].tolist()

    gls = match_log.loc[:,'Performance'].loc[:,'Gls'].tolist()

    ast = match_log.loc[:,'Performance'].loc[:,'Ast'].tolist()

    matches = []

    match_log = match_log.iloc[1]

    index = 0

    for date in selected_matches:

        date = date.split('/')

        matches += [opponent[index],gls[dates.index(f'20{date[2]}-{date[1]}-{date[0]}')],ast[dates.index(f'20{date[2]}-{date[1]}-{date[0]}')],ratings[index]]

        index += 1

    return matches

# Añadir nuevos datos

def combine_sofascore_data(info,int_stats, int_rating, int_stats2, int_rating2, league_rating, league_stats, league_rating2, league_stats2):
    with open('All_Atributes.txt','r') as f:
        list =f.readlines()
    list = ''.join(list)
    list = list.split('\n')

    competitions =[int_stats,int_stats2,league_stats,league_stats2]
    competitions_it = [int_stats,int_stats2,league_stats,league_stats2]
    for competition in competitions_it:
        if competition == '':
            competitions.remove(competition)
    match90stotal = 0
    match90slist = []
    for e in competitions:
        match90stotal += (float(e[1]) * float(e[5])) /90
        match90slist += [(float(e[1]) * float(e[5])) /90]
    for e in range(len(list)):
        stat_type = 0
        float_value = 0
        int_value = 0
        label = list[e]
        for competition in competitions:
            if list[e] in competition:
                e = competition.index(label)//2
                if '(' in competition[e*2+1]:

                    stat_type = 1
                    float_num = float(competition[e*2+1].split('(')[0])
                    int_num = float(competition[e*2+1].split('(')[1].replace('%)',''))
                    float_value += float_num * match90slist[competitions.index(competition)]
                    int_value += int_num * match90slist[competitions.index(competition)]

                elif '/' in competition[e*2+1]:

                    stat_type = 2
                    float_num = float(competition[e*2+1].split('/')[0])
                    int_num = float(competition[e*2+1].split('/')[1])
                    float_value += float_num * match90slist[competitions.index(competition)]
                    int_value += int_num * match90slist[competitions.index(competition)]

                elif '%' in competition[e*2+1]:

                    stat_type = 3
                    int_num = float(competition[e*2+1].replace('%','')) 
                    info[label] = info.setdefault(label, 0) + int_num * match90slist[competitions.index(competition)]

                elif ' min' in competition[e*2+1]:

                    stat_type = 4
                    int_num = float(competition[e*2+1].replace(' min','')) 
                    info[label] = info.setdefault(label, 0) + int_num * match90slist[competitions.index(competition)]

                elif 'per game' in competition[e*2] or competition[e*2] in ['Touches','Key passes','Minutes per game','Possession won','Possession lost','Fouls','Offsides','Was fouled']:
                    
                    stat_type = 5
                    int_num = float(competition[e*2+1])
                    info[label] = info.setdefault(label, 0) + int_num * match90slist[competitions.index(competition)]
                elif competition[e*2] == 'Yellow-Red':
                    info['Red'] = info.setdefault(label, 0) + float(competition[e*2+1])
                else:

                    int_num = float(competition[e*2+1])            
                    info[label] = info.setdefault(label, 0) + int_num

        if stat_type == 1:
            info[label] = f'{round(float_num/90,2)}({round(int_num/90,1)}%)'
        elif stat_type == 2:
            info[label] = f'{round(float_num,0)}/{round(int_num,0)}'
        elif stat_type == 3:
            info[label] = f'{round(info[label]/90,1)}%'
        elif stat_type == 4:
            info[label] = f'{round(info[label]/90,2)} min'
        elif stat_type == 5:
            info[label] = f'{round(info[label]/90,2)}'
    
    rating_average = 0
    ratings =[int_rating,int_rating2,league_rating,league_rating2]
    rating_it = [int_rating,int_rating2,league_rating,league_rating2]
    for rating in rating_it:
        if rating == '':
            ratings.remove(rating)
    for rating in ratings:
        rating_average += float(rating) * match90slist[ratings.index(rating)] 
    info['rating'] = round(rating_average/match90stotal,2)
        

    return info
  

def get_fbref_stats(player,info,year=24):

    names = pd.read_csv('NAME_DB.csv')

    names = names.set_index('Name')

    url = names.loc[player].values[1]

    url = url.split('/')

    name = url[4] + '-Domestic-League-Stats'

    url[4] = 'dom_lg'

    url[0] = 'https://fbref.com'

    url += ['2023-2024',name]

    url = '/'.join(url)

    match_log = pd.read_html(url)

    team_stats = match_log[8]

    gsca = match_log[5]

    xga = match_log[1]
    xga = xga.loc[:,'Unnamed: 0_level_0'].join(xga.loc[:,'Progression'].join(xga.loc[:,'Per 90 Minutes'].join(xga.loc[:,'Playing Time']))).fillna(0).set_index("Season").loc[f'20{year-1}-20{year}']
    
    gsca = gsca.loc[:,'Unnamed: 0_level_0'].join(gsca.loc[:,'SCA'].join(gsca.loc[:,'GCA'])).fillna(0).set_index('Season').loc[f'20{year-1}-20{year}']

    team_stat = team_stats.loc[:,'Unnamed: 0_level_0'].join(team_stats.loc[:,'Team Success']).fillna(0).set_index('Season').loc[f'20{year-1}-20{year}']

    team_stats= team_stats.loc[:,'Unnamed: 0_level_0'].join(team_stats.loc[:,'Team Success (xG)']).fillna(0).set_index('Season').loc[f'20{year-1}-20{year}']

    if type(xga) == pd.DataFrame:
        matches = float(xga.loc[:,'90s'].tolist()[-1])

        progresive_carries = float(xga.loc[:,'PrgC'].tolist()[-1]) 

        progresive_passes = float(xga.loc[:,'PrgP'].tolist()[-1]) 

        progresive_passes_rec = float(xga.loc[:,'PrgR'].tolist()[-1])

        npxg = float(xga.loc[:,'npxG'].tolist()[-1])

        xa = float(xga.loc[:,'xAG'].tolist()[-1])
        
        on_off = float(team_stat.loc[:,'On-Off'].tolist()[-1])

    else:
        matches = float(xga.loc['90s'])

        progresive_carries = float(xga.loc['PrgC']) 

        progresive_passes = float(xga.loc['PrgP']) 

        progresive_passes_rec = float(xga.loc['PrgR'])

        npxg = float(xga.loc['npxG'])

        xa = float(xga.loc['xAG'])   
        
        on_off = float(team_stat.loc['On-Off'])

    sca = float(gsca.loc['SCA'])

    gca = float(gsca.loc['GCA'])



    url = url.replace('-Domestic-League-Stats','-International-Cup-Stats')

    match_log = pd.read_html(url)

    team_stats = match_log[8]

    gsca = match_log[5]

    xga = match_log[1]

    xga = xga.loc[:,'Unnamed: 0_level_0'].join(xga.loc[:,'Progression'].join(xga.loc[:,'Per 90 Minutes'].join(xga.loc[:,'Playing Time']))).fillna(0).set_index("Season").loc[f'20{year-1}-20{year}']

    gsca = gsca.loc[:,'Unnamed: 0_level_0'].join(gsca.loc[:,'SCA'].join(gsca.loc[:,'GCA'])).fillna(0).set_index('Season').loc[f'20{year-1}-20{year}']

    team_stat = team_stats.loc[:,'Unnamed: 0_level_0'].join(team_stats.loc[:,'Team Success']).fillna(0).set_index('Season').loc[f'20{year-1}-20{year}']

    team_stats= team_stats.loc[:,'Unnamed: 0_level_0'].join(team_stats.loc[:,'Team Success (xG)']).fillna(0).set_index('Season').loc[f'20{year-1}-20{year}']

    if type(xga) == pd.DataFrame:
        matches += float(xga.loc[:,'90s'].tolist()[-1])

        progresive_carries += float(xga.loc[:,'PrgC'].tolist()[-1]) 

        progresive_passes += float(xga.loc[:,'PrgP'].tolist()[-1]) 

        progresive_passes_rec += float(xga.loc[:,'PrgR'].tolist()[-1])

        npxg += float(xga.loc[:,'npxG'].tolist()[-1])

        xa += float(xga.loc[:,'xAG'].tolist()[-1])

        on_off += float(team_stat.loc[:,'On-Off'].tolist()[-1])

    else:
        matches += float(xga.loc['90s'])

        progresive_carries += float(xga.loc['PrgC']) 

        progresive_passes += float(xga.loc['PrgP']) 

        progresive_passes_rec += float(xga.loc['PrgR'])

        npxg += float(xga.loc['npxG'])

        xa += float(xga.loc['xAG'])

        on_off += float(team_stat.loc['On-Off'])


    sca += float(gsca.loc['SCA'])

    gca += float(gsca.loc['GCA'])

    info['Progressive carries per 90'] = round(progresive_carries  / matches,2)    

    info['Progressive passes per 90'] = round(progresive_passes / matches,2)

    info['Progressive passes recieved per 90'] = round(progresive_passes_rec / matches,2)

    info['npXG'] = round(npxg,2)

    info['XA'] = round(xa,2)

    info['SCA'] = round(sca / matches,2)

    info['GCA'] = round(gca / matches,2)

    info['Goal difference on off'] = on_off

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

        if e in ['UEFA Europa Conference League','UEFA Champions League','UEFA Europa League','CONMEBOL Libertadores','CONMEBOL Sudamericana']:

            element = page.locator(f'//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/ul/li[{drop_down.index(e)+1}]')

            element.click()

            period = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/button').all_inner_texts()[0]

            if period in [f'{year-1}/{year}',f'20{year}']:

                    if int_stats == '' and int_rating == '':

                        int_stats = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[5]').all_inner_texts()[0].split('\n')

                        int_rating = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[2]/div/div').all_inner_texts()[0]

                        for e in ["Other","Cards","Passing","Defending","Attacking","Matches"]:

                            int_stats.remove(e)

                    else:

                        int_stats2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[5]').all_inner_texts()[0].split('\n')

                        int_rating2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[2]/div/div').all_inner_texts()[0]

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

                        league_rating = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[2]/div/div').all_inner_texts()[0]

                        for e in ["Other","Cards","Passing","Defending","Attacking","Matches"]:

                            league_stats.remove(e)

                    else:

                        league_stats2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[5]').all_inner_texts()[0].split('\n')

                        league_rating2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[2]/div[1]/div[2]/div/div').all_inner_texts()[0]

                        for e in ["Other","Cards","Passing","Defending","Attacking","Matches"]:

                            league_stats2.remove(e)

            league_botton.click()
        
        
    return combine_sofascore_data(info, int_stats, int_rating, int_stats2, int_rating2, league_rating, league_stats, league_rating2, league_stats2)

def get_stats(info,player,page,year=24):

    return get_sofascore_stats(get_fbref_stats(player,info,year),page,year)
    

def make_post(player):
    with open(f'{player}.json') as json_file:
        data = json.load(json_file)
    matches = data['matches']
    info = [data['value'],data['height'].replace(' cm',''),data['age'].replace(' yrs',''),data['nationality'],data['team'],'right' == data['preferred foot'],data['positions']]
    if data['Total played'] == data['Started']:
        match = f"Matches played: {data['Total played']}"
    else:
        match = f"Matches played: {data['Total played']}({data['Started']})"
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
        stats += [match,f'Goals: {goals}',f'Assists: {assists}']
        if int(big_chances_missed) >= int(goals)/2 and int(big_chances_missed) >=5 and int(big_chances_missed)-int(big_chances) >= 0:
            stats += [f'Big Chances Missed: {big_chances_missed}']
            offset += 1
        elif int(big_chances) >= 5:
            stats += [f'Big Chances: {big_chances}']
            offset += 1
        if int(totw) >= 1:
            stats += [f'Team of the Week: {totw}']
            if int(totw) >= 5:
                offset += 1
        if float(offsides) >= 0.8:
            stats += [f'Offsides per game: {offsides}']
        if float(gca) >= 0.6:
            stats += [f'Goal Creating Actions per game: {gca}']
            if float(sca) >= 6.0:
                stats.insert(3+offset,f'Shot Creating Actions per game: {sca}')
                offset += 1
        elif float(sca) >= 4.0:
            stats += [f'Shot Creating Actions per game: {sca}']
        if float(propr) >= 10:
            if float(propr) >= 15:
                stats.insert(3+offset,f'Progresive Passes Recieved per game: {propr}')
                offset += 1
            elif float(prop) >= 9:
                stats.insert(3+offset,f'Progresive Passes per game: {prop}')
                offset += 1
            elif float(proc) >= 6:
                stats.insert(3+offset,f'Progresive Carries per game: {proc}')
                offset += 1
            else:
                stats += [f'Progresive Passes Recieved per game: {propr}']  
        elif float(prop) >= 6:
            stats += [f'Progresive Passes per game: {prop}']
            if float(proc) >= 4:
                stats += [f'Progresive Carries per game: {proc}']
        if float(prop) >= 9:
                stats.insert(3+offset,f'Progresive Passes per game: {prop}')
                offset += 1
        if float(proc) >= 6:
            stats.insert(3+offset,f'Progresive Carries per game: {proc}')
            offset += 1
        if float(dribbles.split('(')[0]) >= 2.0 :
            if float(dribbles.split('(')[0]) >= 3.0 :
                stats.insert(3+offset,f'Progresive Passes Recieved per game: {propr}')
                offset += 1
            else:
                stats += [f'Dribbles per game: {dribbles}']
        if float(min_goal) <= 150:
            if float(min_goal) <= 100:
                stats.insert(3+offset,f'Minutes per goal: {min_goal} min')
                offset += 1
            else:
                stats += [f'Minutes per goal: {min_goal} min']
        if float(shots) >= 1.5:
            if float(shots) >= 2.25:
                stats.insert(3+offset,f'Shots per game: {shots}')
                offset += 1
            else:
                stats += [f'Shots per game: {shots}']
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
                stats.insert(3+offset,f'Key Passes per game: {key_pases}')
                offset += 1
            else:
                stats += [f'Key Passes per game: {key_pases}']
        if float(crosses.split('(')[0]) >= 4.5:
            if float(crosses.split('(')[0]) >= 6.75 or float(crosses.split("(")[1].replace('%)','')) >= 80:
                stats.insert(3+offset,f'Crosses per game: {crosses}')
                offset += 1
            else:
               stats += [f'Crosses per game: {crosses}']
        if len(stats) > 6:
            stats = stats[0:7]
        elif len(stats) < 6:
            if int(big_chances) >= 1:
                stats += [f'Big Chances: {big_chances}']
            if float(sca) >= 3:
                stats += [f'Shot Creating Actions per game: {sca}']
            if float(gca) >= 0.45:
                stats += [f'Goal Creating Actions per game: {gca}']
            if float(proc) >= 2.5:
                stats += [f'Progresive Carries per game: {proc}']
            if float(prop) >= 4:
                stats += [f'Progresive Passes per game: {prop}']
            if float(dribbles.split('(')[0]) >= 1.5:
                stats += [f'Dribbles per game: {dribbles}']
            if float(min_goal) <= 200:
                stats += [f'Minutes per goal: {min_goal} min']
            
            stats += [f'Shots per game: {shots}',f'Goal convertion %: {shot_conv}%',f'Shot on target %: {shots_ot}%']
            stats = stats[0:7]
    elif data['position'] == 'm':
        if int(goals) + int(assists) >= 5:
            stats += [match,f'Goals: {goals}',f'Assists: {assists}']
        else:
            stats += [match,f'Goals & Assists: {int(goals)+int(assists)}']
            offset -= 1
        if int(big_chances) >= 5:
            stats += [f'Big Chances: {big_chances}']
            offset += 1
        if int(totw) >= 1:
            stats += [f'Team of the Week: {totw}']
            if int(totw) >= 5:
                offset += 1
        if float(pass_acuracy) >= 90:
            stats += [f'Pass accuracy: {pass_acuracy}%']
        if float(key_pases) >= 1.5:
            stats += [f'Key Passes per game: {key_pases}']
        if float(dribbles.split('(')[0]) >= 2.0 :
            if float(dribbles.split('(')[0]) >= 3.0 :
                stats.insert(3+offset,f'Progresive Passes Recieved per game: {propr}')
                offset += 1
            else:
                stats += [f'Dribbles per game: {dribbles}']
        if float(min_goal) <= 150:
            if float(min_goal) <= 100:
                stats.insert(3+offset,f'Minutes per goal: {min_goal} min')
                offset += 1
            else:
                stats += [f'Minutes per goal: {min_goal} min']
        if float(shots) >= 1.5:
            if float(shots) >= 2.25:
                stats.insert(3+offset,f'Shots per game: {shots}')
                offset += 1
            else:
                stats += [f'Shots per game: {shots}']
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
                stats.insert(3+offset,f'Crosses per game: {crosses}')
                offset += 1
            else:
               stats += [f'Crosses per game: {crosses}']
        if float(interceptions) >= 1:
            if float(interceptions) >= 1.5:
                stats.insert(3+offset,f'Interceptions per game: {interceptions}')
                offset += 1
            else:
                stats += [f'Interceptions per game: {interceptions}']
        if float(tackles) >= 3:
            if float(tackles) >= 4.5:
                stats.insert(3+offset,f'Tackles per game: {tackles}')
                offset += 1
            else:
                stats += [f'Tackles per game: {tackles}']
        if float(clearences) >= 3:
            if float(clearences) >= 4.5:
                stats.insert(3+offset,f'Clearences per game: {clearences}')
                offset += 1
            else:
                stats += [f'Clearences per game: {clearences}']
        if float(recoveries) >= 2.5:
            if float(recoveries) >= 3.25:
                stats.insert(3+offset,f'Recoveries per game: {recoveries}')
                offset += 1
            else:
                stats += [f'Recoveries per game: {recoveries}']
        
        if len(stats) > 6:
            stats = stats[0:7]
        elif len(stats) < 6:
            if int(big_chances) >= 1:
                stats += [f'Big Chances: {big_chances}']
            if float(sca) >= 3:
                stats += [f'Shot Creating Actions per game: {sca}']
            if float(gca) >= 0.45:
                stats += [f'Goal Creating Actions per game: {gca}']
            if float(proc) >= 2.5:
                stats += [f'Progresive Carries per game: {proc}']
            if float(prop) >= 4:
                stats += [f'Progresive Passes per game: {prop}']
            if float(key_pases) >= 1:
                stats += [f'Key Passes per game: {key_pases}']
            if float(pass_acuracy) >= 85:
                stats += [f'Pass accuracy: {pass_acuracy}%']
            if float(crosses.split('(')[0]) >= 3.5:
                stats += [f'Crosses per game: {crosses}']
            if float(recoveries) >= 2:
                stats += [f'Recoveries per game: {recoveries}']
            
            stats += [f'Key Passes: {key_pases}',f'Pass accurary: {pass_acuracy}%',f'Interceptions per game: {interceptions}']
            stats = stats[0:7]
    elif data['position'] == 'd':
        if int(goals) + int(assists) >= 5:
            stats += [match,f'Goals: {goals}',f'Assists: {assists}']
        else:
            stats += [match,f'Goals & Assists: {int(goals)+int(assists)}']
            offset -= 1
        if int(big_chances) >= 5:
            stats += [f'Big Chances: {big_chances}']
            offset += 1
        if int(totw) >= 1:
            stats += [f'Team of the Week: {totw}']
            if int(totw) >= 5:
                offset += 1
        if float(data['Clean sheets'])/int(data['Started']) >= 0.35:
            stats += [f'Clean Sheets: {data["Clean sheets"]}']
            offset += 1
        if int(yellows) >= int(data['Started'])/2:
            stats += [f'Yellow cards: {yellows}']
        if int(reds)/int(data['Started']) >= 0.2:
            stats += [f'Red cards: {reds}']
        if float(pass_acuracy) >= 90:
            stats += [f'Pass accuracy: {pass_acuracy}%']
        if float(key_pases) >= 1.5:
            stats += [f'Key Passes per game: {key_pases}']
        if float(dribbles.split('(')[0]) >= 2.0 :
            if float(dribbles.split('(')[0]) >= 3.0 :
                stats.insert(3+offset,f'Progresive Passes Recieved per game: {propr}')
                offset += 1
            else:
                stats += [f'Dribbles per game: {dribbles}']
        if float(min_goal) <= 150:
            if float(min_goal) <= 100:
                stats.insert(3+offset,f'Minutes per goal: {min_goal} min')
                offset += 1
            else:
                stats += [f'Minutes per goal: {min_goal} min']
        if float(shots) >= 1.5:
            if float(shots) >= 2.25:
                stats.insert(3+offset,f'Shots per game: {shots}')
                offset += 1
            else:
                stats += [f'Shots per game: {shots}']
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
                stats.insert(3+offset,f'Crosses per game: {crosses}')
                offset += 1
            else:
               stats += [f'Crosses per game: {crosses}']
        if float(interceptions) >= 1:
            if float(interceptions) >= 1.5:
                stats.insert(3+offset,f'Interceptions per game: {interceptions}')
                offset += 1
            else:
                stats += [f'Interceptions per game: {interceptions}']
        if float(tackles) >= 3:
            if float(tackles) >= 4.5:
                stats.insert(3+offset,f'Tackles per game: {tackles}')
                offset += 1
            else:
                stats += [f'Tackles per game: {tackles}']
        if float(clearences) >= 3:
            if float(clearences) >= 4.5:
                stats.insert(3+offset,f'Clearences per game: {clearences}')
                offset += 1
            else:
                stats += [f'Clearences per game: {clearences}']
        if float(recoveries) >= 2.5:
            if float(recoveries) >= 3.25:
                stats.insert(3+offset,f'Recoveries per game: {recoveries}')
                offset += 1
            else:
                stats += [f'Recoveries per game: {recoveries}']
        
        
        if len(stats) > 6:
            stats = stats[0:7]
        elif len(stats) < 6:
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
            stats = stats[0:7]
    matches = matches[0:8]
    if matches[0][0].islower():
        matches[0] = matches[0].split(' ')[1]
    if matches[4][0].islower():
        matches[4] = matches[4].split(' ')[1]
    match1 = [matches[0],int(matches[1]),int(matches[2]),float(matches[3])]
    match2 = [matches[4],int(matches[5]),int(matches[6]),float(matches[7])]
    matches = [match1,match2]
    path = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/"
    make_posts(path,player,True,f"Do you like {player}",matches,stats,info)
 

#scrape_player_list(player_list,delay,False)
make_post('Matías Soulé')