import pandas as pd 
import json
import sys
import time
import pyautogui
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
 
def combine_sofascore_data_2(info,int_stats, int_rating, int_stats2, int_rating2, league_rating, league_stats, league_rating2, league_stats2):
    with open('All_Atributes.json','r') as f:
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
  
