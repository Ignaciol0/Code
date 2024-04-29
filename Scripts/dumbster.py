import pandas as pd 
import json
import sys
import time
import os
import pyautogui
import sys
from ScriptWriter import translate
# This makes the code think is in the root folder. Only done for organizing
sys.path.append("C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code")

int_stats, int_rating, int_stats2, int_rating2, league_rating, league_stats, league_rating2, league_stats2 = '','','','','','','',''

def old_form():
    if int_stats2 != '':

        # Player has played in two international competitions

        if league_stats2 != '':

            matches = float(int_stats[1]) + float(int_stats2[1]) + float(league_stats[1]) + float(league_stats2[1])
            starts = float(int_stats[3]) + float(int_stats2[3]) + float(league_stats[3]) + float(league_stats2[3])

            match90s1 = (float(league_stats[1]) * float(league_stats[5]))/90

            match90s2 = (float(league_stats2[1]) * float(league_stats2[5]))/90

            match90s3 = (float(int_stats[1]) * float(int_stats[5]))/90

            match90s4 = (float(int_stats2[1]) * float(int_stats2[5]))/90

            match90s = match90s1 + match90s2 + match90s3 + match90s4

            for e in range(len(int_stats)//2):
                if league_stats[e*2] == league_stats2[e*2] == int_stats[e*2] == int_stats2[e*2]:
                    if '(' in league_stats[e*2+1]:

                        float1 = float(league_stats[e*2+1].split('(')[0])

                        float2 = float(league_stats2[e*2+1].split('(')[0])

                        float3 = float(int_stats[e*2+1].split('(')[0])

                        float4 = float(int_stats2[e*2+1].split('(')[0])
                        int1 = float(league_stats[e*2+1].split('(')[1].replace('%)',''))
                        int2 = float(league_stats2[e*2+1].split('(')[1].replace('%)',''))

                        int3 = float(int_stats[e*2+1].split('(')[1].replace('%)',''))

                        int4 = float(int_stats2[e*2+1].split('(')[1].replace('%)',''))

                        info[int_stats[e*2]] = f'{round((float1*match90s1+float2*match90s2+float3*match90s3+float4*match90s4)/match90s,2)}({(round(int1*match90s1+int2*match90s2+int3*match90s3+int4*match90s4)/match90s,1)}%)'

                    elif '/' in league_stats[e*2+1]:
                        float1 = float(league_stats[e*2+1].split('/')[0])
                        float2 = float(league_stats2[e*2+1].split('/')[0])

                        float3 = float(int_stats[e*2+1].split('/')[0])

                        float4 = float(int_stats2[e*2+1].split('/')[0])
                        int1 = float(league_stats[e*2+1].split('/')[1])
                        int2 = float(league_stats2[e*2+1].split('/')[1])

                        int3 = float(int_stats[e*2+1].split('/')[1])

                        int4 = float(int_stats2[e*2+1].split('/')[1])

                        info[int_stats[e*2]] = f'{float1+float2+float3+float4}/{int1+int2+int3+int4}'

                    elif '%' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace('%','')) 
                        int2 = float(league_stats2[e*2+1].replace('%','')) 

                        int3 = float(int_stats[e*2+1].replace('%','')) 

                        int4 = float(int_stats2[e*2+1].replace('%',''))

                        info[int_stats[e*2]] =  f'{round((int1*match90s1+int2*match90s2+int3*match90s3+int4*match90s4)/match90s,1)}%'

                    elif ' min' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace(' min','')) 
                        int2 = float(league_stats2[e*2+1].replace(' min','')) 

                        int3 = float(int_stats[e*2+1].replace(' min','')) 

                        int4 = float(int_stats2[e*2+1].replace(' min',''))

                        info[int_stats[e*2]] =  f'{(int1*match90s1+int2*match90s2+int3*match90s3+int4*match90s4)//match90s} min'

                    else:

                        try:

                            if 'per game' in int_stats[e*2] or int_stats[e*2] in ['Touches','Key passes','Minutes per game','Possession won','Possession lost','Fouls','Offsides','Was fouled']:

                                info[int_stats[e*2]] = str(round((float(league_stats[e*2+1])*match90s1 + float(league_stats2[e*2+1])*match90s2 + float(int_stats[e*2+1])*match90s3 + float(int_stats2[e*2+1])*match90s4)/match90s,2))

                            else:

                                info[int_stats[e*2]] = str(round(float(league_stats[e*2+1]) + float(league_stats2[e*2+1]) + float(int_stats[e*2+1]) + float(int_stats2[e*2+1]),2))

                        except:
                                pass

            float1 = float(league_rating)

            float2 = float(league_rating2)

            float3 = float(int_rating)

            float4 = float(int_rating2)

            info['rating'] = str(round((float1*match90s1+float2*match90s2+float3*match90s3+float4*match90s4)/match90s,2))
            # This is done because sometimes if the player has no asist in one competition the stat doesn't appear
            try:
                asist1 = float(int_stats[int_stats.index('Assists')+1])
            except:
                asist1 = 0
            try:
                asist2 = float(int_stats2[int_stats2.index('Assists')+1])
            except:
                asist2 = 0
            try:
                asist3 = float(league_stats[league_stats.index('Assists')+1])
            except:
                asist3 = 0
            try:
                asist4 = float(league2_stats[league2_stats.index('Assists')+1])
            except:
                asist4 = 0
            info['Assists'] = asist1 + asist2 + asist3 + asist4
            info[int_stats[0]] = matches
            info[int_stats[2]] = starts

        else:

            matches = float(int_stats[1]) + float(int_stats2[1]) + float(league_stats[1]) 
            starts = float(int_stats[3]) + float(int_stats2[3]) + float(league_stats[3]) 

            match90s1 = (float(league_stats[1]) * float(league_stats[5]))/90

            match90s3 = (float(int_stats[1]) * float(int_stats[5]))/90

            match90s4 = (float(int_stats2[1]) * float(int_stats2[5]))/90

            match90s = match90s1 + match90s3 + match90s4

            for e in range(len(int_stats)//2):
                if league_stats[e*2] == int_stats[e*2] == int_stats2[e*2]:
                    if '(' in league_stats[e*2+1]:

                        float1 = float(league_stats[e*2+1].split('(')[0])

                        float3 = float(int_stats[e*2+1].split('(')[0])

                        float4 = float(int_stats2[e*2+1].split('(')[0])
                        int1 = float(league_stats[e*2+1].split('(')[1].replace('%)',''))

                        int3 = float(int_stats[e*2+1].split('(')[1].replace('%)',''))

                        int4 = float(int_stats2[e*2+1].split('(')[1].replace('%)',''))

                        info[int_stats[e*2]] = f'{round((float1*match90s1+float3*match90s3+float4*match90s4)/match90s,2)}({round((int1*match90s1+int3*match90s3+int4*match90s4)/match90s,1)}%)'

                    elif '/' in league_stats[e*2+1]:
                        float1 = float(league_stats[e*2+1].split('/')[0])

                        float3 = float(int_stats[e*2+1].split('/')[0])

                        float4 = float(int_stats2[e*2+1].split('/')[0])
                        int1 = float(league_stats[e*2+1].split('/')[1])

                        int3 = float(int_stats[e*2+1].split('/')[1])

                        int4 = float(int_stats2[e*2+1].split('/')[1])

                        info[int_stats[e*2]] = f'{float1+float3+float4}/{int1+int3+int4}'

                    elif '%' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace('%','')) 

                        int3 = float(int_stats[e*2+1].replace('%','')) 

                        int4 = float(int_stats2[e*2+1].replace('%',''))

                        info[int_stats[e*2]] =  f'{round((int1*match90s1+int3*match90s3+int4*match90s4)/match90s,1)}%'

                    elif ' min' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace(' min','')) 

                        int3 = float(int_stats[e*2+1].replace(' min','')) 

                        int4 = float(int_stats2[e*2+1].replace(' min',''))

                        info[int_stats[e*2]] =  f'{(int1*match90s1+int3*match90s3+int4*match90s4)//match90s} min'

                    else:

                        try:

                            if 'per game' in int_stats[e*2] or int_stats[e*2] in ['Touches','Key passes','Minutes per game','Possession won','Possession lost','Fouls','Offsides','Was fouled']:

                                info[int_stats[e*2]] = str(round((float(league_stats[e*2+1])*match90s1 + float(int_stats[e*2+1])*match90s3 + float(int_stats2[e*2+1])*match90s4)/match90s,2))

                            else:

                                info[int_stats[e*2]] = str(round(float(league_stats[e*2+1]) + float(int_stats[e*2+1]) + float(int_stats2[e*2+1]),2))

                        except:
                                pass   

            float1 = float(league_rating)

            float3 = float(int_rating)

            float4 = float(int_rating2)

            info['rating'] = str(round((float1*match90s1+float3*match90s3+float4*match90s4)/match90s,2))
            # This is done because sometimes if the player has no asist in one competition the stat doesn't appear
            try:
                asist1 = float(int_stats[int_stats.index('Assists')+1])
            except:
                asist1 = 0
            try:
                asist2 = float(int_stats2[int_stats2.index('Assists')+1])
            except:
                asist2 = 0
            try:
                asist3 = float(league_stats[league_stats.index('Assists')+1])
            except:
                asist3 = 0
            info['Assists'] = asist1 + asist2 + asist3
            info[int_stats[0]] = matches
            info[int_stats[2]] = starts

    elif int_stats != '':

        if league_stats2 != '':

            matches = float(int_stats[1])  + float(league_stats[1]) + float(league_stats2[1])
            starts = float(int_stats[3])  + float(league_stats[3]) + float(league_stats2[3])

            match90s1 = (float(league_stats[1]) * float(league_stats[5]))/90

            match90s2 = (float(league_stats2[1]) * float(league_stats2[5]))/90

            match90s3 = (float(int_stats[1]) * float(int_stats[5]))/90

            match90s = match90s1 + match90s2 + match90s3 

            for e in range(len(int_stats)//2):
                if league_stats[e*2] == league_stats2[e*2] == int_stats[e*2]:
                    if '(' in league_stats[e*2+1]:

                        float1 = float(league_stats[e*2+1].split('(')[0])

                        float2 = float(league_stats2[e*2+1].split('(')[0])

                        float3 = float(int_stats[e*2+1].split('(')[0])
                        int1 = float(league_stats[e*2+1].split('(')[1].replace('%)',''))
                        int2 = float(league_stats2[e*2+1].split('(')[1].replace('%)',''))

                        int3 = float(int_stats[e*2+1].split('(')[1].replace('%)',''))

                        info[int_stats[e*2]] = f'{round((float1*match90s1+float2*match90s2+float3*match90s3)/match90s,2)}({round((int1*match90s1+int2*match90s2+int3*match90s3)/match90s,1)}%)'

                    elif '/' in league_stats[e*2+1]:
                        float1 = float(league_stats[e*2+1].split('/')[0])
                        float2 = float(league_stats2[e*2+1].split('/')[0])

                        float3 = float(int_stats[e*2+1].split('/')[0])
                        int1 = float(league_stats[e*2+1].split('/')[1])
                        int2 = float(league_stats2[e*2+1].split('/')[1])

                        int3 = float(int_stats[e*2+1].split('/')[1])

                        info[int_stats[e*2]] = f'{float1+float2+float3}/{int1+int2+int3}'

                    elif '%' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace('%','')) 
                        int2 = float(league_stats2[e*2+1].replace('%','')) 

                        int3 = float(int_stats[e*2+1].replace('%','')) 

                        info[int_stats[e*2]] =  f'{round((int1*match90s1+int2*match90s2+int3*match90s3)/match90s,1)}%'

                    elif ' min' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace(' min','')) 
                        int2 = float(league_stats2[e*2+1].replace(' min','')) 

                        int3 = float(int_stats[e*2+1].replace(' min','')) 

                        info[int_stats[e*2]] =  f'{(int1*match90s1+int2*match90s2+int3*match90s3)//match90s} min'

                    else:

                        try:

                            if 'per game' in int_stats[e*2] or int_stats[e*2] in ['Touches','Key passes','Minutes per game','Possession won','Possession lost','Fouls','Offsides','Was fouled']:

                                info[int_stats[e*2]] = str(round((float(league_stats[e*2+1])*match90s1 + float(league_stats2[e*2+1])*match90s2 + float(int_stats[e*2+1])*match90s3)/match90s,2))

                            else:

                                info[int_stats[e*2]] = str(round(float(league_stats[e*2+1]) + float(league_stats2[e*2+1]) + float(int_stats[e*2+1]),2))

                        except:
                                pass

            float1 = float(league_rating)

            float2 = float(league_rating2)

            float3 = float(int_rating)

            info['rating'] = str(round((float1*match90s1+float2*match90s2+float3*match90s3)/match90s,2))
            # This is done because sometimes if the player has no asist in one competition the stat doesn't appear
            try:
                asist1 = float(int_stats[int_stats.index('Assists')+1])
            except:
                asist1 = 0
            try:
                asist3 = float(league_stats[league_stats.index('Assists')+1])
            except:
                asist3 = 0
            try:
                asist4 = float(league2_stats[league2_stats.index('Assists')+1])
            except:
                asist4 = 0
            info['Assists'] = asist1 + asist3 + asist4
            info[int_stats[0]] = matches
            info[int_stats[2]] = starts

        else:

            # Player has played in one international competition

            matches = float(int_stats[1]) + float(league_stats[1]) 
            starts = float(int_stats[3]) + float(league_stats[3]) 

            match90s1 = (float(league_stats[1]) * float(league_stats[5]))/90

            match90s3 = (float(int_stats[1]) * float(int_stats[5]))/90

            match90s = match90s1 + match90s3 

            for e in range(len(int_stats)//2):
                if league_stats[e*2] == int_stats[e*2]:
                    if '(' in league_stats[e*2+1]:

                        float1 = float(league_stats[e*2+1].split('(')[0])

                        float3 = float(int_stats[e*2+1].split('(')[0])
                        int1 = float(league_stats[e*2+1].split('(')[1].replace('%)',''))

                        int3 = float(int_stats[e*2+1].split('(')[1].replace('%)',''))

                        info[int_stats[e*2]] = f'{round((float1*match90s1+float3*match90s3)/match90s,2)}({round((int1*match90s1+int3*match90s3)/match90s,1)}%)'

                    elif '/' in league_stats[e*2+1]:
                        float1 = float(league_stats[e*2+1].split('/')[0])

                        float3 = float(int_stats[e*2+1].split('/')[0])
                        int1 = float(league_stats[e*2+1].split('/')[1])

                        int3 = float(int_stats[e*2+1].split('/')[1])

                        info[int_stats[e*2]] = f'{float1+float3}/{int1+int3}'

                    elif '%' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace('%','')) 

                        int3 = float(int_stats[e*2+1].replace('%','')) 

                        info[int_stats[e*2]] =  f'{round((int1*match90s1+int3*match90s3)/match90s,1)}%'

                    elif 'min' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace(' min','')) 

                        int3 = float(int_stats[e*2+1].replace(' min','')) 

                        info[int_stats[e*2]] =  f'{(int1*match90s1+int3*match90s3)//match90s} min'

                    else:

                        try:

                            if 'per game' in int_stats[e*2] or int_stats[e*2] in ['Touches','Key passes','Minutes per game','Possession won','Possession lost','Fouls','Offsides','Was fouled']:

                                info[int_stats[e*2]] = str(round((float(league_stats[e*2+1])*match90s1 + float(int_stats[e*2+1])*match90s3)/match90s,2))

                            else:

                                info[int_stats[e*2]] = str(round(float(league_stats[e*2+1]) + float(int_stats[e*2+1]),2))

                        except:
                                pass

            float1 = float(league_rating)

            float3 = float(int_rating)

            info['rating'] = str(round((float1*match90s1+float3*match90s3)/match90s,2))
            # This is done because sometimes if the player has no asist in one competition the stat doesn't appear
            try:
                asist1 = float(int_stats[int_stats.index('Assists')+1])
            except:
                asist1 = 0
            try:
                asist3 = float(league_stats[league_stats.index('Assists')+1])
            except:
                asist3 = 0
            info['Assists'] = asist1 + asist3
            info[int_stats[0]] = matches
            info[int_stats[2]] = starts

    else:

        if league_stats2 != '':

            matches = float(league_stats[1]) + float(league_stats2[1])
            starts = float(league_stats[3]) + float(league_stats2[3])

            match90s1 = (float(league_stats[1]) * float(league_stats[5]))/90

            match90s2 = (float(league_stats2[1]) * float(league_stats2[5]))/90

            match90s = match90s1 + match90s2 

            for e in range(len(int_stats)//2):
                if league_stats[e*2] == league_stats2[e*2]:
                    if '(' in league_stats[e*2+1]:

                        float1 = float(league_stats[e*2+1].split('(')[0])

                        float2 = float(league_stats2[e*2+1].split('(')[0])
                        int1 = float(league_stats[e*2+1].split('(')[1].replace('%)',''))
                        int2 = float(league_stats2[e*2+1].split('(')[1].replace('%)',''))

                        info[int_stats[e*2]] = f'{round((float1*match90s1+float2*match90s2)/match90s,2)}({round((int1*match90s1+int2*match90s2)/match90s,1)}%)'

                    elif '/' in league_stats[e*2+1]:
                        float1 = float(league_stats[e*2+1].split('/')[0])
                        float2 = float(league_stats2[e*2+1].split('/')[0])
                        int1 = float(league_stats[e*2+1].split('/')[1])
                        int2 = float(league_stats2[e*2+1].split('/')[1])

                        info[int_stats[e*2]] = f'{float1+float2}/{int1+int2}'

                    elif '%' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace('%','')) 
                        int2 = float(league_stats2[e*2+1].replace('%','')) 

                        info[int_stats[e*2]] =  f'{round((int1*match90s1+int2*match90s2)/match90s,1)}%'

                    elif ' min' in league_stats[e*2+1]:
                        int1 = float(league_stats[e*2+1].replace(' min','')) 
                        int2 = float(league_stats2[e*2+1].replace(' min','')) 

                        info[int_stats[e*2]] =  f'{(int1*match90s1+int2*match90s2)//match90s} min'

                    else:

                        try:

                            if 'per game' in int_stats[e*2] or int_stats[e*2] in ['Touches','Key passes','Minutes per game','Possession won','Possession lost','Fouls','Offsides','Was fouled']:

                                info[int_stats[e*2]] = str(round((float(league_stats[e*2+1])*match90s1 + float(league_stats2[e*2+1])*match90s2)/match90s,2))

                            else:

                                info[int_stats[e*2]] = str(round(float(league_stats[e*2+1]) + float(league_stats2[e*2+1]),2))

                        except:
                                pass                    

            float1 = float(league_rating)

            float2 = float(league_rating2)

            info['rating'] = str(round((float1*match90s1+float2*match90s2)/match90s,2))
            # This is done because sometimes if the player has no asist in one competition the stat doesn't appear
            try:
                asist3 = float(league_stats[league_stats.index('Assists')+1])
            except:
                asist3 = 0
            try:
                asist4 = float(league2_stats[league2_stats.index('Assists')+1])
            except:
                asist4 = 0
            info['Assists'] = asist3 + asist4
            info[int_stats[0]] = matches
            info[int_stats[2]] = starts

        else:

            # Player has played in one international competition

            for e in range(len(league_stats)//2):

                info[league_stats[e*2]] = league_stats[e*2+1]

            info['rating'] = league_rating

def make_post2(player):
    with open(f'{player}.json') as json_file:
        data = json.load(json_file)
    matches = data['matches']
    info = [data['value'],data['height'].replace(' cm',''),data['age'].replace(' yrs',''),data['nationality'],data['team'],'right' == data['preferred foot'],data['positions']]
    if data['Total played'] == data['Started']:
        match = f"Matches played: {data['Total played']}"
    else:
        match = f"Matches played: {data['Total played']}({data['Started']})"
    stats = [data['rating']]
    goals = data['Goals']
    assists = data['Assists']
    totw = data['Team of the week']
    big_chances = data['Big chances created']
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
    big_chances_missed = data['Big chances missed']
    sca = data['SCA']
    gca = data['GCA']
    proc = data['Progressive carries per 90']
    prop = data['Progressive passes per 90']
    propr = data['Progressive passes recieved per 90']
    offsides = data['Offsides']
    yellows = data['Yellow']
    reds = data['Red cards']
    pass_acuracy = data['Accurate per game'].split('(')[1].replace('%)','')
    offset = 0
    if data['position'] == 'f':
        stats += [match,f'Goals: {int(goals)}',f'Assists: {int(assists)}']
        if float(big_chances_missed) >= float(goals)/2 and float(big_chances_missed) >=5 and float(big_chances_missed)-float(big_chances) >= 0:
            stats += [f'Big Chances Missed: {big_chances_missed}']
            offset += 1
        elif float(big_chances) >= 5:
            stats += [f'Big Chances: {big_chances}']
            offset += 1
        if float(totw) >= 1:
            stats += [f'Team of the Week: {totw}']
            if float(totw) >= 5:
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
            if float(big_chances) >= 1:
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
        if float(goals) + float(assists) >= 5:
            stats += [match,f'Goals: {goals}',f'Assists: {assists}']
        else:
            stats += [match,f'Goals & Assists: {float(goals)+float(assists)}']
            offset -= 1
        if float(big_chances) >= 5:
            stats += [f'Big Chances: {big_chances}']
            offset += 1
        if float(totw) >= 1:
            stats += [f'Team of the Week: {totw}']
            if float(totw) >= 5:
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
            if float(big_chances) >= 1:
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
        if float(goals) + float(assists) >= 5:
            stats += [match,f'Goals: {goals}',f'Assists: {assists}']
        else:
            stats += [match,f'Goals & Assists: {float(goals)+float(assists)}']
            offset -= 1
        if float(big_chances) >= 5:
            stats += [f'Big Chances: {big_chances}']
            offset += 1
        if float(totw) >= 1:
            stats += [f'Team of the Week: {totw}']
            if float(totw) >= 5:
                offset += 1
        if float(data['Clean sheets'])/float(data['Started']) >= 0.35:
            stats += [f'Clean Sheets: {data["Clean sheets"]}']
            offset += 1
        if float(yellows) >= float(data['Started'])/2:
            stats += [f'Yellow cards: {yellows}']
        if float(reds)/float(data['Started']) >= 0.2:
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
            if float(big_chances) >= 1:
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
    match1 = [matches[0],float(matches[1]),float(matches[2]),float(matches[3])]
    match2 = [matches[4],float(matches[5]),float(matches[6]),float(matches[7])]
    matches = [match1,match2]
    path = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/"
    make_posts(path,player,True,f"Do you like {player}",matches,stats,info)
 
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
  
def matches_sofascore(page):
        matches1 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[2]').all_inner_texts()

        page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/button').click()

        time.sleep(5)

        matches2 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[2]').all_inner_texts()

        page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/button').click()

        time.sleep(5)

        matches3 = page.locator('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div/div[2]').all_inner_texts()
        
        matches = matches1[0] + "\n" + matches2[0] + '\n' + matches3[0] 

        matches = matches.replace('\nSofasco','@')

        matches = matches.replace('FT\n','')

        matches = matches.replace('AET\n','')

        matches = matches.replace('AP\n','')

        #matches = matches.replace('Int. Friendly Games\n','')

        matches = matches.replace('Club Friendly Games\n','')

        matches = matches.replace('Int. Friendly Games\n','')

        # This is done because some teams with long names like Bayern Leverkusen are reduced to an abreviated name
        pre_lenght = len(matches)
        matches = matches.replace(f'{contract[0]}\n','')
        
        if pre_lenght == len(matches):
            if contract[0] == 'Manchester City':
                matches = matches.replace(f'Man City\n','')
            elif contract[0] == 'Manchester United':
                matches = matches.replace(f'Man United\n','')
            elif contract[0] == 'Atl\u00e9tico Madrid':
                matches = matches.replace(f'Atl. Madrid', '')
            elif contract[0] == "Paris Saint-Germain":
                matches = matches.replace(f'PSG', '')
            else:
                matches = matches.replace(f'{contract[0].split(" ")[-1]}\n','')
                if pre_lenght == len(matches):
                    matches = matches.replace(f'{contract[0].split(" ")[0]}\n','')
                    if pre_lenght == len(matches):
                        matches = matches.replace(f'{contract[0].split(" ")[1]}\n','')
        

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

                if (('.' in e and e.replace('.','',1).isdigit()) or e == "10") or '/' in e or e.isalpha() or ' ' in e:

                    games += [e]

        matches_list = []

        for e in range(len(games)-2):

            if '/' in games[e] and (games[e+1].isalpha() or ' ' in games[e+1]) and ('.' in games[e+2] or '10' == games[e+2]):

                matches_list += [[games[e],games[e+1],games[e+2]]]
        return  matches_list

def get_best_matches(matches,player):

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

    match_log = match_log[0].loc[:,['Unnamed: 0_level_0','Performance']]

    matches = pd.DataFrame(matches,columns=['Date','Opponent','Rating'])

    matches['Rating'] = matches['Rating'].astype(float)

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

    selected_matches = selected_matches[0:5]

    opponent = opponent[0:5]

    ratings = ratings[0:5]

    dates = match_log.loc[:,'Unnamed: 0_level_0'].loc[:,'Date'].tolist()

    gls = match_log.loc[:,'Performance'].loc[:,'Gls'].tolist()

    ast = match_log.loc[:,'Performance'].loc[:,'Ast'].tolist()

    matches = []

    match_log = match_log.iloc[1]

    index = 0

    for date in selected_matches:

        date = date.split('/')

        try:
            matches += [opponent[index],gls[dates.index(f'20{date[2]}-{date[1]}-{date[0]}')],ast[dates.index(f'20{date[2]}-{date[1]}-{date[0]}')],ratings[index]]
        except:
            try:
                matches += [opponent[index],gls[dates.index(f'20{date[2]}-{date[1]}-{date[0]-1}')],ast[dates.index(f'20{date[2]}-{date[1]}-{date[0]-1}')],ratings[index]]
            except:
                ...
        index += 1

    return matches

def old_make_video_frame3(path,matches,stats,percentiles,position='middle'):
    """Path: is the path to the directory all the images are in
       matches: is a list with the match stats. [[club name,goals,assists,rating],[club name,goals,assists,rating]]
       stats: is a list with the season stats. [rating,matches_played,goals (g/a in case of a defender),assists (good stat 1 in case a defender),good stat 1, good stat 2, good stat 3, good stat 4, good stat 5]
    """
    path_resources = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/images/'
    
    '''
    # Percentiles
    percentiles = Image.open(path+f'images/percentiles.png')
    width, height = percentiles.size
    real_width = 280
    multiplier = width / real_width
    height = int(height / multiplier)
    percentiles = percentiles.resize((real_width,height))
    percentile_offset = 1280//2 - real_width // 2 
    percentiles = add_corners(percentiles,5)
    # We are getting the stats of the square by duplicating the texts that appear and making the y increase
    '''
    year_rating = stats[0]
    stats = stats[1:]
    stats_text = ''
    text_height = 280
    text_separation = 35
    for stat in stats:
        stats_text += f'<text fill="white" font-family="Inter" font-size="25" font-weight="bold" x="100" y="{text_height+stats.index(stat)*text_separation}">{stat}</text>\n'
    percentile_height = text_height+(len(stats)-1)*(text_separation) + 20
    # Now we are making the match part of the post
        # We start calculating the separation needed between the rating and the badges
    gamatch1 = matches[0][1]+matches[0][2]
    gamatch2 = matches[1][1]+matches[1][2]
    match_separation_half = (261 - (max(gamatch1,gamatch2)*50//2)) + ((max(gamatch1,gamatch2) * 50))
    gamatch1_text = ''
    g1,a1 = matches[0][1], matches[0][2]
    gamatch2_text = ''
    g2,a2 = matches[1][1], matches[1][2]
    
    # Now we calculate the first match goals and assists
            
    # First we calculate the initial points knowing that the desired point is the half of the width 544 minus half of the ga's width
            # In the one of the goal we substract 472 due to this being the displacement of the path
            # In the one of the assist we add the length of the goals
    # The path doesn't start at 0,0
    starting_point = 38

    inital_x_g = (261 - ((gamatch1*50)//2)) - starting_point#290, 370, 450
    inital_x_a = inital_x_g + 50*g1 
    if g1 > 0:
        for g in range(g1):
            gamatch1_text += f'<path transform="translate({inital_x_g+50*g},90) scale(0.65)" d="M38 76C32.7433 76 27.8033 75.0019 23.18 73.0056C18.5567 71.0119 14.535 68.305 11.115 64.885C7.695 61.465 4.98813 57.4433 2.9944 52.82C0.998134 48.1967 0 43.2567 0 38C0 32.7433 0.998134 27.8033 2.9944 23.18C4.98813 18.5567 7.695 14.535 11.115 11.115C14.535 7.695 18.5567 4.98687 23.18 2.9906C27.8033 0.996866 32.7433 0 38 0C43.2567 0 48.1967 0.996866 52.82 2.9906C57.4433 4.98687 61.465 7.695 64.885 11.115C68.305 14.535 71.0119 18.5567 73.0056 23.18C75.0019 27.8033 76 32.7433 76 38C76 43.2567 75.0019 48.1967 73.0056 52.82C71.0119 57.4433 68.305 61.465 64.885 64.885C61.465 68.305 57.4433 71.0119 52.82 73.0056C48.1967 75.0019 43.2567 76 38 76ZM57 28.5L62.13 26.79L63.65 21.66C61.6233 18.62 59.185 16.0069 56.335 13.8206C53.485 11.6369 50.35 10.0067 46.93 8.93L41.8 12.54V17.86L57 28.5ZM19 28.5L34.2 17.86V12.54L29.07 8.93C25.65 10.0067 22.515 11.6369 19.665 13.8206C16.815 16.0069 14.3767 18.62 12.35 21.66L13.87 26.79L19 28.5ZM15.01 57.76L19.38 57.38L22.23 52.25L16.72 35.72L11.4 33.82L7.6 36.67C7.6 40.7867 8.17 44.5385 9.31 47.9256C10.45 51.3152 12.35 54.5933 15.01 57.76ZM38 68.4C39.6467 68.4 41.2617 68.2733 42.845 68.02C44.4283 67.7667 45.98 67.3867 47.5 66.88L50.16 61.18L47.69 57H28.31L25.84 61.18L28.5 66.88C30.02 67.3867 31.5717 67.7667 33.155 68.02C34.7383 68.2733 36.3533 68.4 38 68.4ZM29.45 49.4H46.55L51.87 34.2L38 24.51L24.32 34.2L29.45 49.4ZM60.99 57.76C63.65 54.5933 65.55 51.3152 66.69 47.9256C67.83 44.5385 68.4 40.7867 68.4 36.67L64.6 34.01L59.28 35.72L53.77 52.25L56.62 57.38L60.99 57.76Z" fill="#0FB916"/>\n'
    if a1 > 0:
        for a in range(a1):
            gamatch1_text += f'''<g width="59" height="50" fill="none" transform = "translate({inital_x_a+50*a},90) scale(0.9)">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M37.9998 3C37.9998 1 32.4998 0 32.4998 0L26.4998 10.5C24.4998 10.5 23.4998 14.5 23.4998 14.5C23.4998 14.5 21.1664 16.5 20.9998 18C19.7998 18.4 11.4998 26.5 7.49983 30.5C0.429491 36.1562 0.468828 38.2577 0.496511 39.7366C0.498194 39.8265 0.499834 39.914 0.499831 40C2.99983 44 7.1665 44 9.99983 44C12.0245 45.4666 57.9998 22 57.9998 19.5C57.9998 17 57.1998 15.5 53.9998 9.5C50.7998 3.5 45.9998 1.33333 43.9998 1V5C40.3998 10.6 36.1665 10.6667 34.4998 10C34.4998 10 37.9998 5 37.9998 3ZM21.4998 37.5L27.4998 34.5C26.4998 32 33.4998 24 37.9998 20.5C41.5998 17.7 47.8331 10.8333 50.4998 7.5L49.4998 6C47.3507 11.5877 37.4422 19.0228 31.8444 23.2233C30.9305 23.9091 30.1314 24.5087 29.4998 25C25.8998 27.8 22.6664 34.5 21.4998 37.5ZM52.4999 9L52.9999 9.5C51.3332 12 46.4998 18 46.4998 18C46.4998 18 38.4999 27 39.9999 28L33.4998 31.5C33.4998 31.5 35.4998 26.5 38.9998 23.5C42.4998 20.5 49.4998 13 52.4999 9Z" fill="#33F000"/>
    <path d="M58 22.5L52.5 25.5L55 29L58.5 27.5L58 22.5Z" fill="#33F000"/>
    <path d="M49.5 27L44 30L46.5 33.5L50 32L49.5 27Z" fill="#33F000"/>
    <path d="M24.5 40L19 43L21.5 46L25.5 44L24.5 40Z" fill="#33F000"/>
    <path d="M17 43.5L11.5 45L14.5 49.5L18 48L17 43.5Z" fill="#33F000"/>
    </g>\n'''    
    
    # Now we calculate the second match goals and assists
            
    # First we calculate the initial points knowing that the desired point is the half of the width 544 minus half of the ga's width
            # In the one of the goal we substract 472 due to this being the displacement of the path
            # In the one of the assist we add the length of the goals
    inital_x_g = (261 -((gamatch2*50)//2)) - starting_point # 290, 370, 450
    inital_x_a = inital_x_g + 50*g2 
    if g2 > 0:
        for g in range(g2):
            gamatch2_text += f'<path transform="translate({inital_x_g+50*g},160) scale(0.65)" d="M38 76C32.7433 76 27.8033 75.0019 23.18 73.0056C18.5567 71.0119 14.535 68.305 11.115 64.885C7.695 61.465 4.98813 57.4433 2.9944 52.82C0.998134 48.1967 0 43.2567 0 38C0 32.7433 0.998134 27.8033 2.9944 23.18C4.98813 18.5567 7.695 14.535 11.115 11.115C14.535 7.695 18.5567 4.98687 23.18 2.9906C27.8033 0.996866 32.7433 0 38 0C43.2567 0 48.1967 0.996866 52.82 2.9906C57.4433 4.98687 61.465 7.695 64.885 11.115C68.305 14.535 71.0119 18.5567 73.0056 23.18C75.0019 27.8033 76 32.7433 76 38C76 43.2567 75.0019 48.1967 73.0056 52.82C71.0119 57.4433 68.305 61.465 64.885 64.885C61.465 68.305 57.4433 71.0119 52.82 73.0056C48.1967 75.0019 43.2567 76 38 76ZM57 28.5L62.13 26.79L63.65 21.66C61.6233 18.62 59.185 16.0069 56.335 13.8206C53.485 11.6369 50.35 10.0067 46.93 8.93L41.8 12.54V17.86L57 28.5ZM19 28.5L34.2 17.86V12.54L29.07 8.93C25.65 10.0067 22.515 11.6369 19.665 13.8206C16.815 16.0069 14.3767 18.62 12.35 21.66L13.87 26.79L19 28.5ZM15.01 57.76L19.38 57.38L22.23 52.25L16.72 35.72L11.4 33.82L7.6 36.67C7.6 40.7867 8.17 44.5385 9.31 47.9256C10.45 51.3152 12.35 54.5933 15.01 57.76ZM38 68.4C39.6467 68.4 41.2617 68.2733 42.845 68.02C44.4283 67.7667 45.98 67.3867 47.5 66.88L50.16 61.18L47.69 57H28.31L25.84 61.18L28.5 66.88C30.02 67.3867 31.5717 67.7667 33.155 68.02C34.7383 68.2733 36.3533 68.4 38 68.4ZM29.45 49.4H46.55L51.87 34.2L38 24.51L24.32 34.2L29.45 49.4ZM60.99 57.76C63.65 54.5933 65.55 51.3152 66.69 47.9256C67.83 44.5385 68.4 40.7867 68.4 36.67L64.6 34.01L59.28 35.72L53.77 52.25L56.62 57.38L60.99 57.76Z" fill="#0FB916"/>\n'
    if a2 > 0:
        for a in range(a2):
            gamatch2_text += f'''<g width="59" height="50" fill="none" transform = "translate({inital_x_a+50*a},160) scale(0.9)">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M37.9998 3C37.9998 1 32.4998 0 32.4998 0L26.4998 10.5C24.4998 10.5 23.4998 14.5 23.4998 14.5C23.4998 14.5 21.1664 16.5 20.9998 18C19.7998 18.4 11.4998 26.5 7.49983 30.5C0.429491 36.1562 0.468828 38.2577 0.496511 39.7366C0.498194 39.8265 0.499834 39.914 0.499831 40C2.99983 44 7.1665 44 9.99983 44C12.0245 45.4666 57.9998 22 57.9998 19.5C57.9998 17 57.1998 15.5 53.9998 9.5C50.7998 3.5 45.9998 1.33333 43.9998 1V5C40.3998 10.6 36.1665 10.6667 34.4998 10C34.4998 10 37.9998 5 37.9998 3ZM21.4998 37.5L27.4998 34.5C26.4998 32 33.4998 24 37.9998 20.5C41.5998 17.7 47.8331 10.8333 50.4998 7.5L49.4998 6C47.3507 11.5877 37.4422 19.0228 31.8444 23.2233C30.9305 23.9091 30.1314 24.5087 29.4998 25C25.8998 27.8 22.6664 34.5 21.4998 37.5ZM52.4999 9L52.9999 9.5C51.3332 12 46.4998 18 46.4998 18C46.4998 18 38.4999 27 39.9999 28L33.4998 31.5C33.4998 31.5 35.4998 26.5 38.9998 23.5C42.4998 20.5 49.4998 13 52.4999 9Z" fill="#33F000"/>
    <path d="M58 22.5L52.5 25.5L55 29L58.5 27.5L58 22.5Z" fill="#33F000"/>
    <path d="M49.5 27L44 30L46.5 33.5L50 32L49.5 27Z" fill="#33F000"/>
    <path d="M24.5 40L19 43L21.5 46L25.5 44L24.5 40Z" fill="#33F000"/>
    <path d="M17 43.5L11.5 45L14.5 49.5L18 48L17 43.5Z" fill="#33F000"/>
    </g>\n'''    



    
    # In these part we will create the percentiles
    percentile_text = ''
    percentile_list = percentiles.loc[:,"Statistic"].tolist()
    percentile_separation = 20
    for attribute in percentile_list:
        percentile = percentiles.set_index("Statistic").loc[attribute,'Percentile']
        percentile_text += f"""
            <text x="90" y="{percentile_height+10+percentile_list.index(attribute)*percentile_separation}" fill="black" font-family="Inter" font-size="12">{attribute}</text>
            <text x="260" y="{percentile_height+10+percentile_list.index(attribute)*percentile_separation}" fill="black" font-family="Inter" font-size="12">{percentile}</text>
            <rect width="{160*(percentile/100)}" height="12" fill="{'green' if percentile >90 else 'lightgreen' if percentile >75 else "yellow" }" transform="translate(280,{percentile_height+10+percentile_list.index(attribute)*percentile_separation-10})" rx="3"/>
            <path d="M0 10H360 11" transform="translate(80,{percentile_height+10+percentile_list.index(attribute)*percentile_separation-5})" stroke="black"/>
            """
    percentile_size = (len(percentile_list))*percentile_separation+20
    
        
            
    
    stats_height = 215
    extra_height = 50
    # THIS IS THE SVG CODE
    svg_code =f"""<svg width="522" height="{percentile_size + percentile_height + extra_height}" viewBox="0 0 522 {percentile_size + percentile_height + extra_height}" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <text fill="white" font-family="Inter" font-size="30" font-weight="bold" x="10" y="35">Season 2022/2023 Achievements</text>

                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="25" x="54" y="75">Average Season Rating</text>
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="30" x="345" y="75">{year_rating}</text>
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="25" x="420" y="75">rtg</text>

                    {gamatch1_text}
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="40" x="{10+match_separation_half}" y="128">{matches[0][3]}</text><text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="25" x="{100+match_separation_half}" y="128">rtg</text>

                    {gamatch2_text}
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="40" x="{10+match_separation_half}" y="195">{matches[1][3]}</text><text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="25" x="{100+match_separation_half}" y="195">rtg</text>

                    <rect width="450" height="{percentile_height+percentile_size-stats_height+ 40}" rx="40" transform="translate(36,{stats_height})" fill="#1D1D1D"/>
                    <text fill="white" font-family="Inter" font-size="30" font-weight="bold" x="132" y="245">This season stats</text>
                    <path transform="translate(-150,-162)" d="M206.373 415.18H615.355" stroke="#525252" stroke-linecap="round"/>

                    {stats_text}

                    <rect width="400" rx="15" height="{percentile_size}" transform="translate(60,{percentile_height -10})" fill="white"/>
                    <path d="M0 10L1 {percentile_size - 10}" transform="translate(250,{percentile_height-10})" stroke="black"/>
                    {percentile_text}
    
                    
                </svg>"""


    with open(path+'svg.svg','w') as f:
        f.write(svg_code)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(path +"svg.svg")
    shape.image_data.save(path +"svg.png")
    

    background = cv2.imread(path_resources+'background.png')
    overlay = cv2.imread(path+'svg.png', cv2.IMREAD_UNCHANGED)
    img_path = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Resources/'
    club1 = Image.open(img_path+f'Clubs/{matches[0][0]}.webp').convert("RGBA")
    club2 = Image.open(img_path+f'Clubs/{matches[1][0]}.webp').convert("RGBA")

    #Background adjusting
    height, width, channels = background.shape
    scale = width / 1280
    height = int(height / scale)
    offset = abs((height-720)//2)
    background = cv2.resize(background,(1280,height))
    if position == 'top':
        background = background[0:720,0:1280]
    elif position == 'middle':
        background = background[offset:720 + offset,0:1280]
    elif position == 'bottom':
        background = background[2*offset:720 + 2*offset,0:1280]

    #Overlay adjusting
    height, width, channels = overlay.shape
    width = 1280//2 - width//2
    imgResult = cvzone.overlayPNG(background,overlay,[width,50])
    cv2.imwrite(path+'Video3(no clubs).png', imgResult)


    # Club adjusting
    club_size = 30

    width, height = club1.size
    scale = width / club_size
    height1 = int(height / scale)
    if height1 > club_size * 1.5:
        scale = int(height / (club_size*1.5))
        width1 = int(width / scale)
        height1 = int(club_size*1.5)
        club1 = club1.resize((width1,int(club_size*1.5)))
    else:
        width1 = club_size
        club1 = club1.resize((club_size,height1))
    width,height = club2.size
    scale = width / club_size
    height2 = int(height / scale)
    if height2 > club_size * 1.5:
        scale = int(height / (club_size*1.5))
        width2 = int(width / scale)
        height2 = int(club_size*1.5)
        club2 = club2.resize((width2,int(club_size*1.5)))
    else:
        width2 = club_size
        club2 = club2.resize((club_size,height2))

    imgResult = Image.open(path+'video3(no clubs).png')
    imgResult.paste(club1, ((520-width1),(145 - height1)), mask= club1)
    imgResult.paste(club2, ((520-width2),(200 - height2)), mask= club2)
    #imgResult.paste(percentiles, (percentile_offset,percentile_separation), mask= percentiles)
    imgResult.save(path+"Video3.png")

    
    os.remove(path+"Video3(no clubs).png")
    os.remove(path+"svg.svg")
    os.remove(path+"svg.png")



print(os.listdir())


"""from wand.image import Image

def convert_svg_to_png(svg_path, png_path):
    with Image(filename=svg_path) as img:
        img.format = 'png'
        img.background_color = 'rgba(255, 255, 255, 0)'  # Set transparent background
        img.alpha_channel = 'remove'  # Remove any alpha channel artifacts
        img.save(filename=png_path)

# Example usage
svg_file = 'svg.svg'
png_file = 'example.png'
convert_svg_to_png(svg_file, png_file)"""

"""import threading
import subprocess

def open_terminal():
    subprocess.call(["wsl", "bash"])

# Create and start a thread to open the terminal
open_terminal()
terminal_thread = threading.Thread(target=open_terminal)
terminal_thread.start()
print(translate("script"))
terminal_thread.join()
"""

positions={"V1":{"background":"top","hook":"bottom"},
"V2":{"background":"middle","description":"bottom","position":False},
"V3":{"background":"middle"}}

#changes = input("This is the dictionary."+"\n"+ ''.join(['{} -> {}\n'.format(image, ''.join([' {}:{},'.format(element, positions[image][element]) for element in positions[image].keys()])) for image in positions.keys()])+ "Give me the changes: ")
#input(f"Change {' '.join(['{}:{}'.format(element, positions[image][element]) for image in positions.keys() for element in positions[image].keys()])}")
"""changes = input("This is the dictionary."+"\n"+ ''.join(['{} -> {}.\n'.format(image, ''.join([' {}:{},'.format(element, positions[image][element]) for element in positions[image].keys()])) for image in positions.keys()])+ "Give me the changes: ")
dictionary = changes.replace("."," ->  ").split(" ->  ")
for e in range(len(dictionary)//2):
    positions[dictionary[e*2]] = {pair.split(":")[0]: pair.split(":")[1] for pair in dictionary[e*2+1][:-1].split(",")}"""
