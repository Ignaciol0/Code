import ollama
import json
from threading import Thread
import unidecode
import sys
# This makes the code think is in the root folder. Only done for organizing
sys.path.append("C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code")

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self):
        Thread.join(self)
        return self._return

def get_profile_script(player):
    name = player
    with open(f'players\{player}.json') as f:
        player = json.load(f)

    player_stats = f'Player from {player["team"]} of age {player["age"]} and nationality {player["nationality"]} and a transfer value of {player["value"]} million euros. And playing as a {player["position"]}'
    prompt = f'Write a two sentence description of {name} with this information {player_stats}.'
    response = ollama.chat(model='llama3', messages=[
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
        'content': prompt
    }
    ])
    with open("prompts.txt","a+") as file:
        if f"Prompt Description: {prompt}" not in file.read():
            file.write(f"Prompt Description: {prompt}\n")
    return unidecode.unidecode(response['message']['content'].split('\n')[-1])
def get_match_script(player,stats,match_list):
    with open(f'players\{player}.json') as f:
        description = json.load(f)
    matches = ''
    for x in match_list:
        matches += f' Against {x[0]} with {"a hack trick" if x[1] == 3 else f"{x[1]} goals" if x[1]>0 else ""} {f"and {x[2]} assists" if x[2] > 0 else ""} and a rating for the match of {x[3]}.'
    prompt = f"write a small paragraph analysis about {player}'s top performances with a {stats[0]} average rating in sofascore and this are his best matches this season, you don't have to mention them all,:{matches} Other information that doesn't have to be mentioned is that he plays as a {description['position']} and he is {description['age']} years old"
    response = ollama.chat(model='llama3', messages=[
        {
            'role':'user',
            'content':"write a small paragraph analysis about Kobbie Mainoo's top performances with a 7.69 average rating in sofascore and this are his best matches this season, you don't have to mention them all,: Against Stuttgart with  and 2 assists and a rating for the match of 8.7. Against Frankfurt with 1 goals and 1 assists and a rating for the match of 8.4. Other information that doesn't have to be mentioned is that he plays as a m and he is 19 yrs years old"
        },{
            'role':'assistant',
            'content':"Kobbie Mainoo has been on fire this season, boasting an impressive average rating of 7.69 on Sofascore. A key highlight from his campaign was his outstanding display against Stuttgart, where he notched up two assists to complement a stellar 8.7 match rating. He also impressed against Frankfurt, netting one goal and providing another assist, earning himself a 8.4 match rating in the process."
        },{
            'role': 'user',
            'content':"write a small paragraph analysis about Federico Valverde's top performances with a 7.34 average rating in sofascore and this are his best matches this season, you don't have to mention them all,: Against Osasuna with  and 3 assists and a rating for the match of 8.8. Against Atletico Madrid with   and a rating for the match of 8.3. Against Mallorca with   and a rating for the match of 8.0. Against Celta Vigo with   and a rating for the match of 7.9. Against Rayo Vallecano with  and 1 assists and a rating for the match of 7.8. Other information that doesn't have to be mentioned is that he plays as a m and he is 25 yrs years old"
        },{
            'role': 'assistant',
            'content':"Federico Valverde has been a force to be reckoned with this season, showcasing his attacking prowess with an impressive average rating of 7.34 on Sofascore. One of his standout performances came against Osasuna, where he netted two goals and contributed three assists, earning himself a 8.8 match rating. He also impressed in matches against Atletico Madrid, Mallorca, Celta Vigo, and Rayo Vallecano, notching up notable ratings of 8.3, 8.0, 7.9, and 7.8 respectively."
        },{
            'role':'user',
            'content':"No, you should not add goals or assists that do not exist"
        },{
            'role':'assistant',
            'content':"Federico Valverde has been a force to be reckoned with this season, showcasing his attacking prowess with an impressive average rating of 7.34 on Sofascore. One of his standout performances came against Osasuna, where he contributed three assists, earning himself a 8.8 match rating. He also impressed in matches against Atletico Madrid, Mallorca, Celta Vigo, and Rayo Vallecano, notching up notable ratings of 8.3, 8.0, 7.9, and 7.8 respectively."
        },{
            'role':'user',
            'content':prompt
    }])
    with open("prompts.txt","a+") as file:
        if f"Prompt Stats: {prompt}" not in file.read():
            file.write(f"Prompt match: {prompt}\n")
    return response['message']['content'].split('\n')[-1]
def get_stats_script(player,stats):
    with open(f'players\{player}.json') as f:
        description = json.load(f)
    prompt = f"write a small paragraph analysis about {player}'s season with this key stats {', '.join(stats[1:]).replace(':','')}. Other information that doesn't have to be mentioned is that he plays as a {description['position']} and he is {description['age']} years old playing for {description['team']}"
    response = ollama.chat(model='llama3', messages=[
        {
            'role':'system',
            'content':'Write ONLY one paragraph'
        },{
            'role':'user',
            'content':"write a small paragraph analysis about Kobbie Mainoo's season with this key stats Matches played 32(28.0), Goals 10.0, Assists 14.0, Big Chances 15.0, Shots per game 4.2, Key Passes per game 5.5. Other information that doesn't have to be mentioned is that he plays as a m and he is 19 yrs years old playing for Manchester United"
        },{
            'role':'assistant',
            'content':"Kobbie Mainoo's impressive rookie season with Manchester United is a testament to his exceptional skill and vision on the pitch. Despite only playing in 32 matches, the 19-year-old midfielder made a significant impact, netting 10 goals and providing 14 assists. His ability to create big chances for his teammates (15.0) is particularly noteworthy, as is his impressive shot rate per game (4.2). Furthermore, Mainoo's key passes per game average of 5.5 suggests that he is not only a threat in the final third but also an astute playmaker who can unlock defenses with precision and accuracy. Overall, Mainoo's debut campaign with Manchester United has been nothing short of remarkable, and it will be exciting to see how he continues to develop and grow as a player in the seasons to come."
        },{
        'role':'user',
        'content':prompt
    }])
    with open("prompts.txt","a+") as file:
        if f"Prompt Stats: {prompt}" not in file.read():
            file.write(f"Prompt Stats: {prompt}\n")
    return response['message']['content'].split('\n')[-1]
def get_percentiles_script(player):
    with open(f'players\{player}.json') as f:
        description = json.load(f)
    matches = ''
    percentile_text = ''
    percentiles = description['percentiles']
    statistics = description['statistics']
    for attribute in statistics:
        percentile_text += f"He is in the {100-int(percentiles[statistics.index(attribute)])} percentile for {attribute} "
    
    prompt = f"write a paragraph analysis about {player}'s percentiles this season here is the text {percentile_text}. Other information that doesn't have to be mentioned is that he plays as a {description['position']} and he is {description['age']} years old"
    response = ollama.chat(model='llama3', messages=[
        {
            'role':'system',
            'content':'Write ONLY one paragraph'
        },{
            'role':'user',
            'content':"write a paragraph analysis about Kobbie Mainoo's percentiles this season here is the text He is in the 1 percentile for Goals/ShotHe is in the 3 percentile for Shots on Target %He is in the 5 percentile for Goals - xGHe is in the 8 percentile for Goals/Shot on TargetHe is in the 13 percentile for Through BallsHe is in the 19 percentile for Take-Ons AttemptedHe is in the 20 percentile for ClearancesHe is in the 23 percentile for Successful Take-OnsHe is in the 25 percentile for Carries into Penalty AreaHe is in the 29 percentile for Goals. Other information that doesn't have to be mentioned is that he plays as a m and he is 19 yrs years old"
        },{
            'role':'assistant',
            'content':"Kobbie Mainoo's impressive statistics this season are a testament to his exceptional skill on the field. Sitting comfortably within the top 1-20 percentiles in various categories, including goals per shot, shots on target percentage, and carries into the penalty area, Mainoo's clinical finishing ability is undeniable. Moreover, his exceptional take-on success rate and clearance numbers suggest that he is not only a goal-scoring threat but also a well-rounded midfielder who contributes to his team's overall defensive solidity. Additionally, his ranking in the top 25 percentiles for successful take-ons and carries into penalty areas highlights his vision, speed, and agility on the field. Overall, Mainoo's impressive statistics make a strong case for him being one of the most exciting young midfielders in the game today."
        },{
        'role':'user',
        'content':prompt
    }])
    with open("prompts.txt","a+") as file:
        if f"Prompt Stats: {prompt}" not in file.read():
            file.write(f"Prompt percentiles: {prompt}\n")
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

def make_short_script(p2,p3):
    scripts = [p2,p3]
    results = []
    for paragraph in scripts:
        prompt = f'I am going to give you a paragraph of a script make a new shorter paragraph script: {paragraph}'
        response = ollama.chat(model='llama3',messages=[
        {'role':'user',
        'content':"I am going to give you a paragraph of a script make a new shorter paragraph script: This is a player that has been at the top of his game for many years, consistently delivering excellent performances for both club and now again country. Toni Kroos, a German midfielder currently playing for Real Madrid at the age of 34, has a transfer value of 11.6 million euros, known for his exceptional passing ability and leadership on the pitch."
        },{
            'role':'assistant',
            'content':"Toni Kroos has been a mainstay in the world of football for many years, consistently delivering exceptional performances at the highest level. At 34, he continues to demonstrate his incredible skill and leadership on the pitch, with an impressive transfer value of 11.6 million euros. Known for his outstanding passing ability and work ethic, Kroos has proven himself to be an invaluable asset to any team he plays for."
        },{
            'role':'user',
            'content':"I am going to give you a paragraph of a script make a new shorter paragraph script: Lautaro Martinez is a highly skilled Argentine forward currently playing for Inter at the age of 26, with a transfer value of 103 million euros, known for his exceptional finishing and ability to score crucial goals in big games. He has been a key player for Inter this season, leading them to a strong position in the Serie A table and into the Champions League knockout stages, although they were later knocked out by Atletico."
        },{
            'role':'assistant',
            'content':"Lautaro Martinez is a highly skilled attacker who has proven himself to be a valuable asset to his team this season. At just 26 years old, he has already demonstrated exceptional finishing ability and the ability to score crucial goals in big games. With a transfer value of 103 million euros, Martinez is highly sought after by top clubs around the world."
        },{
            'role':'user',
            'content':"I am going to give you a paragraph of a script make a new shorter paragraph script: Lautaro Martinez has had an impressive season, with an average SofaScore rating of 7.39. The Argentine forward has played 36 matches, finding the back of the net 25 times, while providing 2 assists. While his shot output per game is solid at 3.49, he has missed a significant number of big chances with 16.0. Martinez ranks as one of the top goal-scorers in Expected Goals and shots on target, while also being among the best in everything related to playmaking abilities, like progressive passes, shot-creating actions, and expected assists. His standout performances this season include his two-goal display against Lecce, which earned him a rating of 8.5, and his two-goal effort against Monza, which earned him a rating of 8.3. These outings demonstrate Martinez's ability to produce high-quality performances on a consistent basis, making him one of the top forwards in the league. At just 26 years old, he has plenty of time to continue improving and potentially become even more dominant in the future. So is it best for him to stay at Inter or to go to Barca, Chelsea or even other top tier team?"
        },{
            'role':'assistant',
            'content':"This season, Martinez has had an impressive SofaScore rating of 7.39, playing a key role in Inter's first position in the Serie A table. He has scored 25 goals in 36 matches and ranks among the top in Expected Goals and shots on target, as well as being one of the best in playmaking abilities such as progressive passes, shot-creating actions, and expected assists. So, the question remains, is it best for him to stay at Inter or to go to Barca, Chelsea or even other top tier team?"
        },{
            'role':'user',
            'content':"I am going to give you a paragraph of a script make a new shorter paragraph script: Toni Kroos has had an impressive season, with an average SofaScore rating of 7.58. The German midfielder has played 36 matches, contributing one goal and seven assists to his team's success. Kroos has also made a significant number of recoveries per game with 4.8, showcasing his work rate and defensive abilities. His standout performances this season include his zero-goal, one-assist display against Las Palmas, which earned him a rating of 8.9, and his zero-goal, zero-assist effort against Atletico Madrid, which earned him a rating of 8.6. These outings demonstrate Kroos's consistency and reliability in midfield, making him an integral part of any team he plays for. At the age of 34, Kroos continues to perform at a high level, cementing his status as one of the top midfielders in the league."
        },{
            'role':'assistant',
            'content':"This season, he has averaged a remarkable SofaScore rating of 7.58, contributing one goal and seven assists to his team's success. His tireless efforts have earned him an impressive number of recoveries per game, with 4.8, showcasing his dedication to the sport. Standout performances this season include his zero-goal, one-assist display against Las Palmas, which earned him a rating of 8.9, and his zero-goal, zero-assist effort against Atletico Madrid, which earned him a rating of 8.6. These outings demonstrate Kroos's enduring consistency and reliability in midfield, cementing his status as one of the top midfielders in the league."
        },{
            'role':'user',
            'content':prompt
        }
        ])
        with open("prompts.txt","a+") as file:
            if f"Prompt Short{scripts.index(paragraph)}: {prompt}" not in file.read():
                file.write(f"Prompt Short {scripts.index(paragraph)+1}: {prompt}")
        results += [response['message']['content']+"\n\n"]
    
    return "".join(results)

def translate(script):
    with open(f"{script}.txt") as t:
        lines = t.readlines()
    text = ''
    texts = []
    for e in lines:
        if e == '\n':
            texts += [text]
            text = ''
        else:
            text += e
    textos = []
    for text in texts:
        response = ollama.chat(model='llama3', messages=[
        {
            'role':'system',
            'content':'You are a pro english to spanish translator. Here are the translation of some unusual terms. Transfer Value: Valor de Mercado, Side: Equipo, defensive dutie: papel defensivo'
        },{
            'role':'user',
            'content':"English: Serhou Guirassy is a highly skilled French-Guinean forward who has been impressing audiences with his exceptional finishing ability on the pitch. Currently playing for VfB Stuttgart at the age of 28, he has a transfer value of 42 million euros and has attracted attention from top clubs in Europe for his remarkable performances this season.\n Spanish: ..."
        },{
            'role':'assistant',
            'content':"Serhou Guirassy es un extremo francés-guineano de gran habilidad que ha estado impresionando a todos con su increíble definición. Actualmente jugando para el Stuttgart y con 28 años de edad, tiene un valor de mercado de unos 42 millones de euros y ha atraído la atención de clubes top del fútbol europeo por su destacado rendimiento esta temporada."
        },{
            'role':'user',
            'content':"English: Guirassy's SofaScore rating for the season is an impressive 7.77, playing a key role in Stuttgart's push for Europe. He has scored an incredible 25 goals in 23 matches, with an efficiency that ranks him among the best in the world. He has had some key performances with a couple of hacktricks and some braces. Do you think he will remain at Stuttgart or will he leave for another team?\n Spanish: ..."
        },{
            'role':'assistant',
            'content':"Guirassy tiene una nota media en SofaScore de 7.7 esta temporada. Está jugando un papel clave en el sueño Europeo del Stuttgart. Ha marcado la increíble cantidad 25 goles en 23 partidos, con una eficacia que lo posiciona entre los mejores del mundo. Guirassy tenido algunas actuaciones clave esta temporada con un par de hacktricks y algunos dobletes. ¿Creéis que se quedará en Stuttgart o se irá a otro equipo?"
        },{
            'role': 'user',
            'content': f"English:\n {text}, Spanish: ..."
        }])
        textos += [response['message']['content']]
    return "\n".join(textos)

def get_stats_script_es(player):
    name = player
    with open(f'players\{player}.json') as f:
        player = json.load(f)

    player_stats = f'Jugador del {player["team"]} de {player["age"]} años y su pais es {player["nationality"]} cuenta con un valor de mercado de {player["value"]} millones de euros. Juega como un {player["position"]}'
    prompt = f'Escribe una descrición de dos frases sobre {name} con esta información {player_stats}.'
    response = ollama.chat(model='llama3', messages=[
        {
            'role':'system',
            'content':'Escribe en español de España menciona aspectos importantes como la edad, nacionalidad, equipo y valor de mercado.'
        },{
        'role':'user',
        'content': prompt
    }
    ])
    with open("prompts.txt","a+") as file:
        if f"Prompt Description: {prompt}" not in file.read():
            file.write(f"Prompt Description: {prompt}\n")
    return response['message']['content'].split('\n')[-1]
def get_season_script_es(player,stats,match_list):
    with open(f'players\{player}.json') as f:
        description = json.load(f)
    matches = ''
    percentile_text = ''
    percentiles = description['percentiles']
    statistics = description['statistics']
    for attribute in statistics:
        percentile_text += f"He is in the {100-int(percentiles[statistics.index(attribute)])} for {attribute}"
    for x in match_list:
        matches += f' Against {x[0]} with {"a hack trick" if x[1] == 3 else f"{x[1]} goals" if x[1]>0 else ""} {f"and {x[2]} assists" if x[2] > 0 else ""} and a rating for the match of {x[3]}.'
    prompt = f"write a paragraph analysis about {player}'s season with a {stats[0]} average rating in sofascore and this other key stats {', '.join(stats[1:]).replace(':','')} also here are some other stats {percentile_text} his best matches this season are:{matches}. Other information that doesn't have to be mentioned is that he plays as a {description['position']} and he is {description['age']} years old"
    response = ollama.chat(model='llama3', messages=[
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
        'role': 'user',
        'content': "write a paragraph analysis about Harry Kane's season with a 7.75 average rating in sofascore and this other key stats Matches played 35, Goals 37.0, Assists 10.0, Big Chances Missed 26.0, Minutes per goal 86.37 min, Shots per game 4.23 also his best matches this season are: Against Dortmund with 3 goals and 0 assists and a rating for the match of 9.9. Against Mainz 05 with 3 goals and 1 assists and a rating for the match of 9.8.. Other information that doesn't have to be mentioned is that he plays as a f and he is 30 yrs years old",
    },{
        'role':'assistant',
        'content':"Harry Kane's season has been nothing short of remarkable, with an average SofaScore rating of 7.75. The England international has played 35 matches, finding the back of the net an impressive 37 times, while providing 10 assists. However, he has also missed a significant number of big chances with  26. Despite this, Kane's scores a goal every 86.37 minutes being among the best in Europe, showcasing his efficiency in attack. His standout performances this season include his Hack Trick against Borussia Dortmund, which earned him a rating of 9.9, and his Hack Trick and one-assist against Mainz, which earned him a rating of 9.8. These outings demonstrate Kane's ability to produce high-quality performances on a consistent basis, and cement his status as one of the top strikers in the league. Could the Champions league be his first carrear title?"
    },{
        'role':'user',
        'content':"write a paragraph analysis about Antoine Griezmann's season with a 7.53 average rating in sofascore and this other key stats Matches played 34(32.0), Goals 17.0, Assists 6.0, Shots per game 2.37, Big Chances Missed 13.0, Team of the Week 4.0 also here are some other stats ['Passes Completed', 'Touches', 'Total Passing Distance', 'Progressive Passing Distance', 'xAG: Exp. Assisted Goals', 'Shot-Creating Actions', 'Switches', 'Miscontrols', 'Key Passes', 'Assists', 'xA: Expected Assists', 'Progressive Passes', 'Crosses', 'Carries', 'Goal-Creating Actions'] his best matches this season are: Against Celtic with 2 goals  and a rating for the match of 9.8. Against Inter with 1 goals  and a rating for the match of 8.8.. Other information that doesn't have to be mentioned is that he plays as a f and he is 33 yrs years old"
    },{
        'role':'assistant',
        'content':"Antoine Griezmann's season has been spectacular, although this Atletico is not the same team he left years ago, with an average SofaScore rating of 7.53. The French forward has played 34 matches, finding the back of the net 17 times, while providing 6 assists. While his shot output per game is impressive at 2.37, he has missed a significant number of big chances with 13.0. Also he ranks as the best forward in Expected Assists and touches, while also being among the best in everything related to playmaking abilities, like progressive passes, key passes, shot and goal creating actions and expected assisted goals. It is also worth noting the efect a manager like Simeone has had on this player making him one of the Strikers with the best defensive performances. Griezmann's standout performances this season include his two-goal display against Celtic, which earned him a rating of 9.8, and his one-goal effort against Inter, which earned him a rating of 8.8. These outings demonstrate Griezmann's ability to produce high-quality performances on a consistent basis, although he may not be at the same level as some of the other top scorers in the league. Nonetheless, his experience and consistency make him the key player of his team."
    },{
        'role':'user',
        'content':"write a paragraph analysis about Serhou Guirassy's season with a 7.77 average rating in sofascore and this other key stats Matches played 23(20.0), Goals 25, Assists 1, Big Chances Miss 13, Minutes per goal 71.0 min, Shots 3.2 also here are some other stats [99, 98, 97, 97, 94, 94, 93, 93, 92, 92] his best matches this season are: Against Mainz 05 with a hack trick  and a rating for the match of 10.0. Against Wolfsburg with a hack trick  and a rating for the match of 9.8.. Other information that doesn't have to be mentioned is that he plays as a f and he is 28 yrs years old"
    },{
        'role':'assistant',
        'content':"Serhou Guirassy's season has been nothing short of impressive, with an average SofaScore rating of 7.77. The Guinean forward has played 23 matches, finding the back of the net a remarkable 25 times, while providing one assist. He scores a goal every 71.0 min being amoung the best in the world, showcasing his efficiency in attack. He is also very good in the creating aspect, despite the believe his is a bulky striker, he is in the top percentiles for shot and goal creating actions. Also he does well for himself in key passes and expected assists. Guirassy's standout performances this season include his hack-tricks against Wolfsburg and Mainz, which earned him a rating of 9.8, and 10 respectively. Also to note a couple braces like the one with one-assist against Darmstadt, which earned him a rating of 9.3. These outings demonstrate Guirassy's ability to produce high-quality performances on a consistent basis, and cement his status as one of the top strikers in the league. His impressive goal-scoring record and 3.2 shots per game make him a indispensable asset for his team, and he is likely to be a key player in their push for Europe this season."
    },{
        'role':'user',
        'content':prompt
    }])
    with open("prompts.txt","a+") as file:
        if f"Prompt Stats: {prompt}" not in file.read():
            file.write(f"Prompt Stats: {prompt}\n")
    return response['message']['content'].split('\n')[-1]


def make_script(player,stats,match_list):
    if input('Do you want to create a script? ') == 'no':
        return
    
    threat1 =ThreadWithReturnValue(target=get_profile_script,args=(player,))
    thread2 =ThreadWithReturnValue(target=get_match_script,args=(player,stats,match_list,))
    thread3 =ThreadWithReturnValue(target=get_stats_script,args=(player,stats,))
    thread4 =ThreadWithReturnValue(target=get_percentiles_script,args=(player,))
    threat1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    paragraph1 = input(f'Give me the first parragraph about {player}\n')
    paragraph2 = threat1.join()
    paragraph3 = thread2.join()
    paragraph4 = thread3.join()
    paragraph5 = thread4.join()
    
    
    while True:
        try:
            script = paragraph1 + '\n\n' + paragraph2 + '\n\n' + paragraph3 + "\n\n" + paragraph4 + "\n\n" + paragraph5 + "\n\n"
            meResponse = input(f'Script:\n\n{script}\n\nIs this script ok? (ok/p1/p2/p3/all/exit) ')
        except:
            meResponse = 'loop'
        
        if meResponse == 'ok':
            break
        elif meResponse == 'p1':
            paragraph1 = input('Write the paragraph 1: ')
        elif meResponse == 'p2':
            paragraph2 = asyncio.run(get_stats_script(player))
        elif meResponse == 'p3':
            paragraph3 = asyncio.run(get_season_script(player,stats,match_list))
        elif meResponse == 'all':
            paragraph2 = asyncio.run(get_stats_script(player))
            paragraph3 = asyncio.run(get_season_script(player,stats,match_list))
        elif meResponse == 'exit':
            return
    with open('script.txt','w') as f:
        f.write(script + '\n')
    input('Script is writen modify it now if you want ')
    with open("script.txt") as t:
        lines = t.readlines()
    text = ''
    texts = []
    for e in lines:
        if e == '\n':
            texts += [text]
            text = ''
        else:
            text += e
    with open("prompts.txt","a+") as file:
        if f"Description: {texts[1]}\nStats: {texts[2]}\n" not in file.read():
            file.write(f"Description: {texts[1]}\nStats: {texts[2]}\n")
    thread3 = ThreadWithReturnValue(target=make_short_script,args=(texts[1],texts[2],))
    thread3.start()
    if input('Do you want to do the sorts script? ') == 'no':
        return
    script_sorts =thread3.join()
    print(script_sorts)
    while True:
        if input("Do you like the sorts script? ") == 'no':
            script_sorts = make_short_script(texts[1],texts[2])
        else:   
            break
    with open('sort_script.txt','w') as f:
        f.write(script_sorts+'\n\n\n')
    input('\nModify the short now If you want')
    with open("sort_script.txt") as t:
        lines = t.readlines()
    text = ''
    texts = []
    for e in lines:
        if e == '\n':
            texts += [text]
            text = ''
        else:
            text += e
    with open("prompts.txt","a+") as file:
        if f"Response Short 1: {texts[0]}" not in file.read():
            file.write(f"Response Short 1: {texts[0]}\n")
        if f"Response Short 2: {texts[1]}" not in file.read():
            file.write(f"Response Short 2: {texts[1]}\n")
 
player = 'Federico Valverde'

#make_script(player,[7.69, 'Matches played: 32(28.0)', 'Goals: 10.0', 'Assists: 14.0', 'Big Chances: 15.0', 'Shots per game: 4.2', 'Key Passes per game: 5.5'],[['Stuttgart', 0, 2, 8.7], ['Frankfurt', 1, 1, 8.4]],get_fbref_percentiles(player,False))
#get_season_script(player,[7.69, 'Matches played: 32(28.0)', 'Goals: 10.0', 'Assists: 14.0', 'Big Chances: 15.0', 'Shots per game: 4.2', 'Key Passes per game: 5.5'],[['Stuttgart', 0, 2, 8.7], ['Frankfurt', 1, 1, 8.4]])
#print(get_stats_script_es(player))

