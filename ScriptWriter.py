import ollama
import json

def get_stats_script(player):
    name = player
    with open(f'players\{player}.json') as f:
        player = json.load(f)

    player_stats = f'Player from {player["team"]} of age {player["age"]} and nationality {player["nationality"]} and a transfer value of {player["value"]} million euros. And playing as a {player["position"]}'
    response = ollama.chat(model='llama2', messages=[
        {
            'role':'system',
            'content':'Write a two sentence script and DO NOT use one of the most sought-after players in the world and DO NOT describe the information given.'
        },
    {
        'role': 'user',
        'content': f'Write a two sentence description of Pascal Gross with this information Player from Brighton & Hove Albion of age 32 yrs and nationality ger and a transfer value of 7.3 million euros. And playing as a m',
    },{
        'role': 'assistant',
        'content': 'This is a a player that has not been in the spotlight at all even though it consistently deliveres very good campaings. But this season he has shined with a different light. He has been called up to his national team and will be subject of debate in the upcoming euros.\nThis player is Pascal Gross a german 32 year-old midfielder from Brighton that even dough he is only valued at 7 million euros he is looking like one of the best players in the prem this year.'
    },{
        'role':'user',
        'content':f'Write a two sentence description of Aleksandr Golovin with this information Player from AS Monaco of age 27 yrs and nationality rus and a transfer value of 29 million euros. And playing as a m'
    },{
        'role' : 'assistant',
        'content':'Aleksandr Golovin is a highly skilled Russian midfielder currently playing for AS Monaco at the age of 27, with a transfer value of 29 million euros, known for his exceptional dribbling and creative playmaking abilities on the pitch. Despite his impressive talent, he often flies under the radar compared to some of the more high-profile players in the world.'
    },{
        'role':'user',
        'content':f'Write a two sentence description of Florian Wirtz with this information Player from Bayern Leverkusen of age 20 and nationality ger and a transfer value of 95 million euros. And playing as a m '
    },{
        'role':'assistant',
        'content':'This is Florian Wirtz a 20-year-old midfielder from Bayer 04 Leverkusen, has been making waves in the football world with his impressive skills and performances on the pitch. With a transfer value of 95 million euros, he is one of the most highly rated young players in the game today, known for his exceptional dribbling and creative playmaking abilities.'
    },{
        'role':'user',
        'content':'Yes, absolutely what I wanted very good job'
    },{
        'role':'user',
        'content':f'Write a two sentence description of {name} with this information {player_stats}." '
    }
    ])
    return response['message']['content'].split('\n')[-1]
def get_season_script(player,stats,match_list):
    with open(f'players\{player}.json') as f:
        description = json.load(f)
    matches = ''
    for x in match_list:
        matches += f' Against {x[0]} with {x[1]} goals and {x[2]} assists and a rating for the match of {x[3]}.'
    prompt = f"write a paragraph analysis about {player}'s season with a {stats[0]} average rating in sofascore and this other key stats {', '.join(stats[1:]).replace(':','')} also his best matches this season are:{matches}. Other information that doesn't have to be mentioned is that he plays as a {description['position']} and he is {description['age']} years old"
    response = ollama.chat(model='llama2', messages=[
        {
            'role':'system',
            'content':'Write ONLY one paragraph'
        },
    {
        'role': 'user',
        'content': "write a descrition about Alejandro Grimaldo's season with a 7.7 average rating in sofascore and this other key stats Matches played 28.0(26.0), Goals 10.0, Assists 9.0, Big Chances 12.0, Team of the Week 6.0, Minutes per goal 71.9 min also his best matches this season are Against Qarabağ with 2 goals and 1 assists and a rating for the match of 9.3.Against Leipzig with 0 goals and 2 assists and a rating for the match of 8.9.",
    },{
        'role':'assistant',
        'content':"Alejandro Grimaldo's season has been nothing short of impressive, with an average rating of 7.7 on SofaScore. The left-back has played 28 matches, scoring 10 goals and providing 9 assists, while creating a significant amount of big chances for his team. His minutes per goal rate of 71.9 min is among the best in the league, showcasing his efficiency in attack. Grimaldo's standout performances this season include his two-goal, one-assist display against Qarabağ, which earned him a rating of 9.3, and his zero-goal, two-assist effort against Leipzig, which earned him a rating of 8.9. These outings demonstrate Grimaldo's ability to produce high-quality performances on a consistent basis."
    },{
        'role':'user',
        'content':prompt
    }])
    return response['message']['content'].split('\n')[-1]

def make_post(player, youngster=True):
    with open(f'players/{player}.json') as json_file:
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
    return [matches,stats]


def make_script(player,stats,match_list):
    if input('Do you want to create a script? ') == 'no':
        return
    paragraph1 = input(f'Give me the first parragraph about {player}\n')
    paragraph2 = get_stats_script(player)
    paragraph3 = get_season_script(player,stats,match_list)
    while True:
        script = paragraph1 + '\n\n' + paragraph2 + '\n\n' + paragraph3
        meResponse = input(f'Script:\n\n{script}\n\nIs this script ok? (ok/p1/p2/p3/all)')
        if meResponse == 'ok':
            break
        elif meResponse == 'p1':
            paragraph1 = input('Write the paragraph 1: ')
        elif meResponse == 'p2':
            paragraph2 = get_stats_script(player)
        elif meResponse == 'p3':
            paragraph3 = get_season_script(player,stats,match_list)
        elif meResponse == 'all':
            aiResponse = ollama.chat(model='llama2', message=f'Fix any coherence error in this script {script}')
            meResponse = input(f'Script:\n{aiResponse}\nIs this script ok? (yes/no)')
            if meResponse == 'yes':
                script = aiResponse
                break
            else:
                paragraph2 = get_stats_script(player)
                paragraph3 = get_season_script(player,stats,match_list)
    with open('script.txt','w') as f:
        f.write(script + '\n')
    input('Script is writen modify it now if you want ')


#make_script(player,[7.69, 'Matches played: 32(28.0)', 'Goals: 10.0', 'Assists: 14.0', 'Big Chances: 15.0', 'Shots per game: 4.2', 'Key Passes per game: 5.5'],[['Stuttgart', 0, 2, 8.7], ['Frankfurt', 1, 1, 8.4]])

