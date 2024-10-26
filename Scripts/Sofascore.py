import requests
import json
import pandas as pd
from unidecode import unidecode

class Sofascore:
    
    ############################################################################
    def __init__(self):
        self.requests_headers = {
            'authority': 'api.sofascore.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'if-none-match': 'W/"4bebed6144"',
            'origin': 'https://www.sofascore.com',
            'referer': 'https://www.sofascore.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '+ \
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 '+ \
                'Safari/537.36',
            }
        
        self.league_stats_fields = [
            'goals', 'yellowCards', 'redCards', 'groundDuelsWon',
            'groundDuelsWonPercentage', 'aerialDuelsWon', 
            'aerialDuelsWonPercentage', 'successfulDribbles',
            'successfulDribblesPercentage', 'tackles', 'assists',
            'accuratePassesPercentage', 'totalDuelsWon', 
            'totalDuelsWonPercentage', 'minutesPlayed', 'wasFouled', 'fouls',
            'dispossessed', 'possesionLost', 'appearances', 'started', 'saves',
            'cleanSheets', 'savedShotsFromInsideTheBox', 
            'savedShotsFromOutsideTheBox', 'goalsConcededInsideTheBox',
            'goalsConcededOutsideTheBox', 'highClaims', 'successfulRunsOut',
            'punches', 'runsOut', 'accurateFinalThirdPasses', 
            'bigChancesCreated', 'accuratePasses', 'keyPasses', 
            'accurateCrosses', 'accurateCrossesPercentage', 'accurateLongBalls',
            'accurateLongBallsPercentage', 'interceptions', 'clearances',
            'dribbledPast', 'bigChancesMissed', 'totalShots', 'shotsOnTarget',
            'blockedShots', 'goalConversionPercentage', 'hitWoodwork', 
            'offsides', 'expectedGoals', 'errorLeadToGoal', 'errorLeadToShot',
            'passToAssist'
        ]
        self.concatenated_fields = "%2C".join(self.league_stats_fields)
    
    ############################################################################
    def get_source_comp_info(self, year, league, source):
        """ Checks to make sure that the given league season is a valid season for 
        the scraper and returns the source_comp_info dict for use in the modules.
        
        Args
        ----
        year : int
            Calendar year that the season ends in (e.g. 2023 for the 2022/23 season)
        league : str
            League. Look in shared_functions.py for the available leagues for each\
            module.
        source : str
            The scraper to be checked (e.g. "FBRef", "Transfermarkt, etc.). These\
            are the ScraperFC modules.
        Returns
        -------
        souce_comp_info: dict
            Dict containing all of the competition info for all of the sources. Used
            for different things in every module
        """
        # Dict of data sources and leagues for each source
        source_comp_info = {
            "All": {},
            "FBRef": {
                # Each competition gets its first valid year (from the competition seasons history page on fbref), the url
                # to the season history page, and the "finder" which is used to find the season and match links in HTML
                #################################
                # Men"s club international cups #
                #################################
                "Copa Libertadores": {
                    "first valid year": 2014,
                    "url": "https://fbref.com/en/comps/14/history/Copa-Libertadores-Seasons",
                    "finder": ["Copa-Libertadores"],
                },
                "Champions League": {
                    "first valid year": 1991,
                    "url": "https://fbref.com/en/comps/8/history/Champions-League-Seasons",
                    "finder": ["European-Cup", "Champions-League"],
                },
                "Europa League": {
                    "first valid year": 1991,
                    "url": "https://fbref.com/en/comps/19/history/Europa-League-Seasons",
                    "finder": ["UEFA-Cup", "Europa-League"],
                },
                "Europa Conference League": {
                    "first valid year": 2022,
                    "url": "https://fbref.com/en/comps/882/history/Europa-Conference-League-Seasons",
                    "finder": ["Europa-Conference-League"],
                },
                ####################################
                # Men"s national team competitions #
                ####################################
                "World Cup": {
                    "first valid year": 1930,
                    "url": "https://fbref.com/en/comps/1/history/World-Cup-Seasons",
                    "finder": ["World-Cup"],
                },
                "Copa America": {
                    "first valid year": 2015,
                    "url": "https://fbref.com/en/comps/685/history/Copa-America-Seasons",
                    "finder": ["Copa-America"],
                },
                "Euros": {
                    "first valid year": 2000,
                    "url": "https://fbref.com/en/comps/676/history/European-Championship-Seasons",
                    "finder": ["UEFA-Euro", "European-Championship"],
                },
                ###############
                # Men"s big 5 #
                ###############
                "Big 5 combined": {
                    "first valid year": 1996,
                    "url": "https://fbref.com/en/comps/Big5/history/Big-5-European-Leagues-Seasons",
                    "finder": ["Big-5-European-Leagues"],
                },
                "EPL": {
                    "first valid year": 1993,
                    "url": "https://fbref.com/en/comps/9/history/Premier-League-Seasons",
                    "finder": ["Premier-League"],
                },
                "Ligue 1": {
                    "first valid year": 1996,
                    "url": "https://fbref.com/en/comps/13/history/Ligue-1-Seasons",
                    "finder": ["Ligue-1", "Division-1"],
                },
                "Bundesliga": {
                    "first valid year": 1989,
                    "url": "https://fbref.com/en/comps/20/history/Bundesliga-Seasons",
                    "finder": ["Bundesliga"],
                },
                "Serie A": {
                    "first valid year": 1989,
                    "url": "https://fbref.com/en/comps/11/history/Serie-A-Seasons",
                    "finder": ["Serie-A"],
                },
                "La Liga": {
                    "first valid year": 1989,
                    "url": "https://fbref.com/en/comps/12/history/La-Liga-Seasons",
                    "finder": ["La-Liga"],
                },
                #####################################
                # Men"s domestic leagues - 1st tier #
                #####################################
                "MLS": {
                    "first valid year": 1996,
                    "url": "https://fbref.com/en/comps/22/history/Major-League-Soccer-Seasons",
                    "finder": ["Major-League-Soccer"],
                },
                "Brazilian Serie A": {
                    "first valid year": 2014,
                    "url": "https://fbref.com/en/comps/24/history/Serie-A-Seasons",
                    "finder": ["Serie-A"],
                },
                "Eredivisie": {
                    "first valid year": 2001,
                    "url": "https://fbref.com/en/comps/23/history/Eredivisie-Seasons",
                    "finder": ["Eredivisie"],
                },
                "Liga MX": {
                    "first valid year": 2004,
                    "url": "https://fbref.com/en/comps/31/history/Liga-MX-Seasons",
                    "finder": ["Primera-Division", "Liga-MX"],
                },
                "Primeira Liga": {
                    "first valid year": 2001,
                    "url": "https://fbref.com/en/comps/32/history/Primeira-Liga-Seasons",
                    "finder": ["Primeira-Liga"],
                },
                "Jupiler Pro League": {
                    "first valid year": 2004,
                    "url": 'https://fbref.com/en/comps/37/history/Belgian-Pro-League-Seasons',
                    "finder": ["Belgian-Pro-League"],
                },
                "Argentina Liga Profesional": {
                    "first valid year": 2014,
                    "url": 'https://fbref.com/en/comps/21/history/Primera-Division-Seasons',
                    "finder": ['Primera-Division'],
                },
                ####################################
                # Men"s domestic league - 2nd tier #
                ####################################
                "EFL Championship": {
                    "first valid year": 2002,
                    "url": "https://fbref.com/en/comps/10/history/Championship-Seasons",
                    "finder": ["First-Division", "Championship"],
                },
                "La Liga 2": {
                    "first valid year": 2002,
                    "url": 'https://fbref.com/en/comps/17/history/Segunda-Division-Seasons',
                    "finder": ["Segunda-Division"],
                },
                "2. Bundesliga": {
                    "first valid year": 2004,
                    "url": 'https://fbref.com/en/comps/33/history/2-Bundesliga-Seasons',
                    "finder": ['2-Bundesliga'],
                },
                "Ligue 2": {
                    "first valid year": 2010,
                    "url": 'https://fbref.com/en/comps/60/history/Ligue-2-Seasons',
                    "finder": ["Ligue-2"],
                },
                "Serie B": {
                    "first valid year": 2002,
                    "url": 'https://fbref.com/en/comps/18/history/Serie-B-Seasons',
                    "finder": ["Serie-B"],
                },
                ##############################################
                # Men"s domestic league - 3rd tier and lower #
                ##############################################
                #######################
                # Men"s domestic cups #
                #######################
                #########################################
                # Women"s internation club competitions #
                #########################################
                "Women Champions League": {
                    "first valid year": 2015,
                    "url": "https://fbref.com/en/comps/181/history/Champions-League-Seasons",
                    "finder": ["Champions-League"],
                },
                ######################################
                # Women"s national team competitions #
                ######################################
                "Womens World Cup": {
                    "first valid year": 1991,
                    "url": "https://fbref.com/en/comps/106/history/Womens-World-Cup-Seasons",
                    "finder": ["Womens-World-Cup"],
                },
                "Womens Euros": {
                    "first valid year": 2001,
                    "url": "https://fbref.com/en/comps/162/history/UEFA-Womens-Euro-Seasons",
                    "finder": ["UEFA-Womens-Euro"],
                },
                ############################
                # Women"s domestic leagues #
                ############################
                "NWSL": {
                    "first valid year": 2013,
                    "url": "https://fbref.com/en/comps/182/history/NWSL-Seasons",
                    "finder": ["NWSL"],
                },
                "A-League Women": {
                    "first valid year": 2019,
                    "url": "https://fbref.com/en/comps/196/history/A-League-Women-Seasons",
                    "finder": ["A-League-Women", "W-League"],
                },
                "WSL": {
                    "first valid year": 2017,
                    "url": "https://fbref.com/en/comps/189/history/Womens-Super-League-Seasons",
                    "finder": ["Womens-Super-League"],
                },
                "D1 Feminine": {
                    "first valid year": 2018,
                    "url": "https://fbref.com/en/comps/193/history/Division-1-Feminine-Seasons",
                    "finder": ["Division-1-Feminine"],
                },
                "Womens Bundesliga": {
                    "first valid year": 2017,
                    "url": "https://fbref.com/en/comps/183/history/Frauen-Bundesliga-Seasons",
                    "finder": ["Frauen-Bundesliga"],
                },
                "Womens Serie A": {
                    "first valid year": 2019,
                    "url": "https://fbref.com/en/comps/208/history/Serie-A-Seasons",
                    "finder": ["Serie-A"],
                },
                "Liga F": {
                    "first valid year": 2023,
                    "url": "https://fbref.com/en/comps/230/history/Liga-F-Seasons",
                    "finder": ["Liga-F"],
                },
                #########################
                # Women"s domestic cups #
                #########################
                "NWSL Challenge Cup": {
                    "first valid year": 2020,
                    "url": "https://fbref.com/en/comps/881/history/NWSL-Challenge-Cup-Seasons",
                    "finder": ["NWSL-Challenge-Cup"],
                },
                "NWSL Fall Series": {
                    "first valid year": 2020,
                    "url": "https://fbref.com/en/comps/884/history/NWSL-Fall-Series-Seasons",
                    "finder": ["NWSL-Fall-Series"],
                },
            },
            "Understat": {
                "EPL": {"first valid year": 2015,},
                "La Liga": {"first valid year": 2015,},
                "Bundesliga":  {"first valid year": 2015,},
                "Serie A":  {"first valid year": 2015,},
                "Ligue 1":  {"first valid year": 2015,},
                "RFPL":  {"first valid year": 2015,},
            },
            "FiveThirtyEight": {
                "EPL":  {"first valid year": 2017,},
                "La Liga":  {"first valid year": 2017,},
                "Bundesliga":  {"first valid year": 2017,},
                "Serie A":  {"first valid year": 2017,},
                "Ligue 1":  {"first valid year": 2017,},
            },
            "Capology": {
                "Bundesliga":  {"first valid year": 2014,},
                "2.Bundesliga":  {"first valid year": 2020,},
                "EPL":  {"first valid year": 2014,},
                "EFL Championship":  {"first valid year": 2014,},
                "Serie A":  {"first valid year": 2010,},
                "Serie B":  {"first valid year": 2020,},
                "La Liga":  {"first valid year": 2014,},
                "La Liga 2":  {"first valid year": 2020,},
                "Ligue 1":  {"first valid year": 2014,},
                "Ligue 2":  {"first valid year": 2020,},
                "Eredivisie":  {"first valid year": 2014,},
                "Primeira Liga":  {"first valid year": 2014,},
                "Scottish PL":  {"first valid year": 2020,},
                "Super Lig":  {"first valid year": 2014,},
                "Belgian 1st Division":  {"first valid year": 2014,},
            },
            "Transfermarkt": {
                "EPL":  {"first valid year": 1993,},
                "EFL Championship": {"first valid year": 2005,},
                "EFL1": {"first valid year": 2005,},
                "EFL2": {"first valid year": 2005,},
                "Bundesliga": {"first valid year": 1964,},
                "2.Bundesliga": {"first valid year": 1982,},
                "Serie A": {"first valid year": 1930,},
                "Serie B": {"first valid year": 1930,},
                "La Liga": {"first valid year": 1929,},
                "La Liga 2": {"first valid year": 1929,},
                "Ligue 1": {"first valid year": 1970,},
                "Ligue 2": {"first valid year": 1993,},
                "Eredivisie": {"first valid year": 1955,},
                "Scottish PL": {"first valid year": 2004,},
                "Super Lig": {"first valid year": 1960,},
                "Jupiler Pro League": {"first valid year": 1987,},
                "Liga Nos": {"first valid year": 1994,},
                "Russian Premier League": {"first valid year": 2011,},
                "Brasileirao": {"first valid year": 2001,},
                "Argentina Liga Profesional": {"first valid year": 2015,},
                "MLS": {"first valid year": 1996,},
            },
            "Oddsportal": {
                "EPL": {
                    "url": "https://www.oddsportal.com/football/england/premier-league",
                    "first valid year": 2004,
                    "finder": "premier-league",
                },
                "EFL Championship": {
                    "url": "https://www.oddsportal.com/football/england/championship",
                    "first valid year": 2004,
                    "finder": "championship",
                },
                "EFL League 1": {
                    "url": "https://www.oddsportal.com/football/england/league-one",
                    "first valid year": 2004,
                    "finder": "league-one",
                },
                "EFL League 2": {
                    "url": "https://www.oddsportal.com/football/england/league-two",
                    "first valid year": 2004,
                    "finder": "league-two",
                },
                "La Liga": {
                    "url": "https://www.oddsportal.com/football/spain/laliga",
                    "first valid year": 2004,
                    "finder": "laliga",
                },
            },
            "Sofascore": {
                # European continental club comps
                "Champions League": {
                    "id": 7,
                    "seasons": {
                        "03/04": 12, "04/05": 13, "05/06": 14, "06/07": 15, 
                        "07/08": 603, "08/09": 1664, "09/10": 1825, "10/11": 2764, 
                        "11/12": 3402, "12/13": 4788, "13/14": 6359, "14/15": 8226, 
                        "15/16": 10390, "16/17": 11773, "17/18": 13415, 
                        "18/19": 17351, "19/20": 23766, "20/21": 29267, 
                        "21/22": 36886, "22/23": 41897, "23/24": 52162,
                    },
                },
                "Europa League": {
                    "id": 679,
                    "seasons": {
                        "09/10": 2155, "10/11": 2765, "11/12": 3403, "12/13": 4790, 
                        "13/14": 6361, "14/15": 8228, "15/16": 10391, "16/17": 11774, 
                        "17/18": 13416, "18/19": 17352, "19/20": 23755, 
                        "20/21": 29343, "21/22": 37725, "22/23": 44509, 
                        "23/24": 53654,
                    },
                },
                "Europa Conference League": {
                    "id": 17015,
                    "seasons": {
                        "21/22": 37074, "22/23": 42224, "23/24": 52327,
                    },
                },
                # European domestic leagues
                "EPL": {
                    "id": 17,
                    "seasons": {
                        "93/94": 25680, "94/95": 29167, "95/96": 25681, 
                        "96/97": 25682, "97/98": 51, "98/99": 50, "99/00": 49, 
                        "00/01": 48, "01/02": 47, "02/03": 46, "03/04": 1, 
                        "04/05": 2, "05/06": 3, "06/07": 4, "07/08": 581, 
                        "08/09": 1544, "09/10": 2139, "10/11": 2746, "11/12": 3391,
                        "12/13": 4710, "13/14": 6311, "14/15": 8186, "15/16": 10356,
                        "16/17": 11733, "17/18": 13380, "18/19": 17359, 
                        "19/20": 23776, "20/21": 29415, "21/22": 37036, 
                        "22/23": 41886, "23/24": 52186,
                    },
                },
                "La Liga": {
                    "id": 8,
                    "seasons": {
                        "93/94": 25687, "94/95": 25688,  "95/96": 25690, 
                        "96/97": 25689, "97/98": 75, "98/99": 74, "99/00": 73, 
                        "00/01": 72, "01/02": 71, "02/03": 70, "03/04": 99, 
                        "04/05": 100, "05/06": 101, "06/07": 102, "07/08": 669, 
                        "08/09": 1587, "09/10": 2252, "10/11": 2896, "11/12": 3502,
                        "12/13": 4959, "13/14": 6559, "14/15": 8578, "15/16": 10495,
                        "16/17": 11906, "17/18": 13662, "18/19": 18020,
                        "19/20": 24127, "20/21": 32501, "21/22": 37223, 
                        "22/23": 42409, "23/24": 52376, "24/25": 61643,
                    },
                },
                "Bundesliga": {
                    "id": 35,
                    "seasons": {
                        "92/93": 13088, "97/98": 107, "98/99": 106, "99/00": 105, 
                        "00/01": 104, "01/02": 103, "02/03": 90, "03/04": 91, 
                        "04/05": 92, "05/06": 93, "06/07": 94,  "07/08": 525, 
                        "08/09": 1557, "09/10": 2188, "10/11": 2811, "11/12": 3405,
                        "12/13": 4792, "13/14": 6303, "14/15": 8238, "15/16": 10419,
                        "16/17": 11818, "17/18": 13477, "18/19": 17597, 
                        "19/20": 23538, "20/21": 28210, "21/22": 37166, 
                        "22/23": 42268, "23/24": 52608,
                    },
                },
                "Serie A": {
                    "id": 23,
                    "seasons": {
                        "97/98": 85, "98/99": 84, "99/00": 83, "00/01": 82, 
                        "01/02": 81, "02/03": 80, "03/04": 95, "04/05": 96, 
                        "05/06": 97, "06/07": 98, "07/08": 712, "08/09": 1552, 
                        "09/10": 2324, "10/11": 2930, "11/12": 3639, "12/13": 5145, 
                        "13/14": 6797, "14/15": 8618, "15/16": 10596, "16/17": 11966, 
                        "17/18": 13768, "18/19": 17932, "19/20": 24644, 
                        "20/21": 32523, "21/22": 37475, "22/23": 42415, 
                        "23/24": 52760,
                    },
                },
                "Ligue 1": {
                    "id": 34,
                    "seasons": {
                        "97/98": 65, "98/99": 64, "99/00": 63, "00/01": 62, 
                        "01/02": 61, "02/03": 60, "03/04": 59, "04/05": 58, 
                        "05/06": 57, "06/07": 56, "07/08": 534, "08/09": 1542, 
                        "09/10": 2120, "10/11": 2719, "11/12": 3380, "12/13": 4616, 
                        "13/14": 6271, "14/15": 8122, "15/16": 10373, "16/17": 11648, 
                        "17/18": 13384, "18/19": 17279, "19/20": 23872, 
                        "20/21": 28222, "21/22": 37167, "22/23": 42273, 
                        "23/24": 52571,
                    },
                },
                # South America
                "Argentina Liga Profesional": {
                    "id": 155,
                    "seasons": {
                        "08/09": 1636, "09/10": 2323, "10/11": 2887, "11/12": 3613,
                        "12/13": 5103, "13/14": 6455, "2014": 8338, "2015": 9651,
                        "2016": 11237, "16/17": 12117, "17/18": 13950, 
                        "18/19": 18113, "19/20": 24239, "2021": 37231, "2022": 41884,
                        "2023": 47647, 
                    },
                },
                "Argentina Copa de la Liga Profesional": {
                    "id": 13475,
                    "seasons": {
                        "2019": 23108, "2020": 34618, "2021": 35486, "2022": 40377,
                        "2023": 47644,
                    },
                },
                # USA
                "MLS": {},
                "USL Championship": {
                    "id": 13363,
                    "seasons": {
                        "2016": 11611, "2017": 12895, "2018": 16187, "2019": 22636,
                        "2020": 27058, "2021": 36157, "2022": 40364, "2023": 48258,
                    },
                },
                "USL1": {
                    "id": 13362,
                    "seasons": {
                        "2019": 22635, "2020": 26862, "2021": 36019, "2022": 40280, 
                        "2023": 48265,
                    },
                },
                "USL2": {
                    "id": 13546,
                    "seasons": {
                        "2019": 23299, "2021": 36421, "2022": 40556, "2023": 49265,
                    },
                },
                # Men's international comps
                "World Cup": {
                    "id": 16,
                    "seasons": {
                        "1930": 40712, "1934": 17559, "1938": 17560, "1950": 40714,
                        "1954": 17561, "1958": 17562, "1962": 17563, "1966": 17564,
                        "1970": 17565, "1974": 17566, "1978": 17567, "1982": 17568,
                        "1986": 17569, "1990": 17570, "1994": 17571, "1998": 1151,
                        "2002": 2636, "2006": 16, "2010": 2531, "2014": 7528,
                        "2018": 15586, "2022": 41087,
                    },
                },
                "Euros": {
                    "id": 1,
                    "seasons": {
                        "1972": 27050, "1976": 27049, "1980": 27046, "1984": 27048,
                        "1988": 27051, "1992": 27052, "1996": 27053, "2000": 358,
                        "2004": 356, "2008": 1162, "2012": 4136, "2016": 11098,
                        "2021": 26542,
                    },
                },
                "Gold Cup": {
                    "id": 140,
                    "seasons": {
                        "2009": 2088, "2011": 3302, "2015": 10238, "2017": 13258,
                        "2019": 23156, "2021": 36683, "2023": 50492,
                    },
                },
                # Women's international comps
                "Women's World Cup": {
                    "id": 290,
                    "seasons": {
                        "2011": 3144, "2015": 9602, "2019": 19902, "2023": 46930,
                    },
                },
            },
        }
        return source_comp_info
    ############################################################################
    def get_positions(self, selected_positions):
        """Returns a string for the parameter filters of the scrape_league_stats() request.

        Args:
            selected_positions (list): List of the positions available to filter on the SofaScore UI

        Returns:
            dict: Goalies, Defenders, Midfielders and Forwards and their translation for the parameter of the request
        """
        positions = {
            'Goalkeepers': 'G',
            'Defenders': 'D',
            'Midfielders': 'M',
            'Forwards': 'F'
        }
        abbreviations = [positions[position] for position in selected_positions]
        return '~'.join(abbreviations)
    
    ############################################################################
    def get_match_id(self, match_url):
        """Get match id from a Sofascore match url

        Args:
            match_url (string): Full link to a SofaScore match

        Returns:
            string: Match id for a SofaScore match. Used in Urls
        """
        # this can also be found in the 'id' key of the dict returned from 
        # get_match_data(), if the format of the match url ever changes
        match_id = match_url.split('#')[-1]
        
        return match_id.split(":")[1]
    
    ############################################################################
    def get_player_ids(self, match_url):
        """Get the player ids for a Sofascore match

        Args:
            match_url (string): Full link to a SofaScore match

        Returns:
            dict: Name and ids of every player in the match
                Key: Name
                Value: Id
        """
        match_id = self.get_match_id(match_url)

        response = requests.get(
            f'https://api.sofascore.com/api/v1/event/{match_id}/lineups', 
            headers=self.requests_headers
        )

        teams = ['home', 'away']
        player_ids = {}
        for team in teams:
            data = response.json()[team]['players']

            for item in data:
                player_data = item['player']
                player_ids[player_data['name']] = player_data['id']

        return player_ids
    
    ############################################################################
    def get_match_data(self, match_url):
        """Get match general data

        Args:
            match_url (string): Full link to a SofaScore match

        Returns:
            dict: Generic data about a match
        """

        match_id = self.get_match_id(match_url)

        response = requests.get(f'https://api.sofascore.com/api/v1/event/{match_id}', headers=self.requests_headers)
        data = response.json()['event']
        return data
    
    ############################################################################
    def get_team_names(self, match_url):
        """Get the team names for the home and away teams

        Args:
            match_url (string): Full link to a SofaScore match

        Returns:
            strings: Name of home and away team.
        """

        data = self.get_match_data(match_url)

        home_team = data['homeTeam']['name']
        away_team = data['awayTeam']['name']

        return home_team, away_team
    
    ############################################################################
    def scrape_league_stats(
        self, year, league, accumulation='total', 
        selected_positions=['Goalkeepers', 'Defenders', 'Midfielders', 'Forwards']
    ):
        """ Get every player statistic that can be asked in league pages on 
        SofaScore.

        Args:
            tournament (string): Name of the competition
            season (string): Season selected
            accumulation (str, optional): Value of the filter accumulation. Can 
                be "per90", "perMatch", or "total". Defaults to 'total'.
            selected_positions (list, optional): Value of the filter positions. 
                Defaults to ['Goalkeepers', 'Defenders', 'Midfielders', 
                'Forwards'].

        Returns:
            DataFrame: DataFrame with each row corresponding to a player and 
                the columns are the fields defined on get_league_stats_fields()
        """
        source_comp_info = self.get_source_comp_info(year, league, "Sofascore")
        
        positions = self.get_positions(selected_positions)
        league_id = source_comp_info['Sofascore'][league]['id']
        season_id = source_comp_info['Sofascore'][league]['seasons'][year]

        offset = 0
        df = pd.DataFrame()
        for i in range(0,100):
            request_url = f'https://api.sofascore.com/api/v1' +\
                f'/unique-tournament/{league_id}/season/{season_id}/statistics'+\
                f'?limit=100&order=-rating&offset={offset}'+\
                f'&accumulation={accumulation}' +\
                f'&fields={self.concatenated_fields}'+\
                f'&filters=position.in.{positions}'
            response = requests.get(request_url, headers=self.requests_headers)
            new_df = pd.DataFrame(response.json()['results'])
            new_df['player'] = new_df.player.apply(pd.Series)['name']
            new_df['team'] = new_df.team.apply(pd.Series)['name']
            df = pd.concat([df, new_df])
            
            if response.json().get('page') == response.json().get('pages'):
                print('End of the pages')
                break
            offset += 100
        
        return df

    ############################################################################
    def match_momentum(self, match_url):
        """Get the match momentum values

        Args:
            match_url (str): Full link to a SofaScore match

        Returns:
            fig, ax: Plot of match momentum and fig/axes for further customization
        """
        match_id = self.get_match_id(match_url)
        response = requests.get(
            f'https://api.sofascore.com/api/v1/event/{match_id}/graph', 
            headers=self.requests_headers
        )
        match_momentum_df = pd.DataFrame(response.json()['graphPoints'])

        return match_momentum_df

    ############################################################################
    def get_general_match_stats(self, match_url):
        """Get general match statistics (possession, passes, duels) by teams.

        Args:
            match_url (str): Full link to a SofaScore match

        Returns:
            DataFrame: Each row is a general statistic and the columns show the 
                values for home and away Teams.
        """
        match_id = self.get_match_id(match_url)

        response = requests.get(
            f'https://api.sofascore.com/api/v1/event/{match_id}/statistics', 
            headers=self.requests_headers
        )

        df = pd.DataFrame()
        for i in range(len(response.json()['statistics'][0]['groups'])):
            df_valores = pd.DataFrame(response.json()['statistics'][0]['groups'][i]['statisticsItems'])
            df = pd.concat([df,df_valores])
        df = df[['name', 'home', 'homeValue', 'homeTotal','away', 'awayValue', 'awayTotal']]
        return df
    
    ############################################################################
    def get_match_goals(self, match_url):
        match_id = self.get_match_id(match_url)

        response = requests.get(
            f'https://api.sofascore.com/api/v1/event/{match_id}/incidents', 
            headers=self.requests_headers
        )
        goals = []
        for incident in response.json()["incidents"]:
            if incident["incidentType"] == 'goal':
                goals += [[incident['time']+incident.get('addedTime', 0),unidecode(incident.get('player', {}).get('name', 'none')),unidecode(incident.get('assist1', {}).get('name', 'none')),incident['isHome']]]
        return goals
    ############################################################################
    def get_players_match_stats(self, match_url):
        """Returns match data for each player.

        Args:
            match_url (str): Full link to a SofaScore match

        Returns:
            DataFrames: A DataFrame for home and away teams with each row being 
                a player and in each columns a different statistic or data of 
                the player
        """

        match_id = self.get_match_id(match_url)
        home_name, away_name = self.get_team_names(match_url)
        
        response = requests.get(
            f'https://api.sofascore.com/api/v1/event/{match_id}/lineups', 
            headers=self.requests_headers
        )
        
        names = {'home': home_name, 'away': away_name}
        dataframes = {}
        for team in names.keys():
            data = pd.DataFrame(response.json()[team]['players'])
            columns_list = [
                data['player'].apply(pd.Series), data['shirtNumber'], 
                data['jerseyNumber'], data['position'], data['substitute'], 
                data['statistics'].apply(pd.Series, dtype=object), 
                data['captain']
            ]
            df = pd.concat(columns_list, axis=1)
            df['team'] = names[team]
            dataframes[team] = df
        
        return dataframes['home'], dataframes['away']
    
    ############################################################################
    def get_players_average_positions(self, match_url):
        """Return player averages positions for each team

        Args:
            match_url (str): Full link to a SofaScore match

        Returns:
            DataFrame: Each row is a player and columns averageX and averageY 
                denote their average position on the match.
        """
        match_id = self.get_match_id(match_url)
        home_name, away_name = self.get_team_names(match_url)

        response = requests.get(
            f'https://api.sofascore.com/api/v1/event/{match_id}/average-positions', 
            headers=self.requests_headers
        )

        names = {'home': home_name, 'away': away_name}
        dataframes = {}
        for team in names.keys():
            data = pd.DataFrame(response.json()[team])
            df = pd.concat(
                [data['player'].apply(pd.Series), data.drop(columns=['player'])],
                axis=1
            )
            df['team'] = names[team]
            dataframes[team] = df
            
        return dataframes['home'], dataframes['away']
    
    ############################################################################
    def get_player_heatmap(self, match_url, player):
        """ Get the x-y coordinates to create a player heatmap. Use Seaborn's
        `kdeplot()` to create the heatmap image.

        Args:
            match_url (str): Full link to a SofaScore match
            player (str): Name of the player (must be the SofaScore one). Use
                Sofascore.get_player_ids()

        Returns:
            DataFrame: Pandas dataframe with x-y coordinates for the player
        """
        match_id = self.get_match_id(match_url)

        player_ids = self.get_player_ids(match_url)
        player_id = player_ids[player]

        response = requests.get(
            f'https://api.sofascore.com/api/v1/event/{match_id}/player/{player_id}/heatmap', 
            headers=self.requests_headers
        )
        heatmap = pd.DataFrame(response.json()['heatmap'])
        
        return heatmap

Sofascore().scrape_league_stats( year ='24/25',league = "La Liga", selected_positions=['Forwards']).to_csv("data.csv")