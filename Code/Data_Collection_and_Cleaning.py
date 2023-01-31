import pandas as pd
import numpy as np
import time

#Read in data
def getDraftClass():
    #Creat variables
    url_head = 'https://www.pro-football-reference.com/years/'
    years = [str(yr) for yr in range(2000, 2019)]
    Draft_DataFrame = pd.DataFrame(columns=['Rnd', 'Pick', 'Tm', 'Player', 'Pos', 'Year'])

    for yr in years:
        try:
            time.sleep(2)
            full_url = url_head + yr + '/draft.htm'
            df = pd.read_html(full_url)[0]
            df.columns = df.columns.get_level_values(0)
            df = df[['Unnamed: 0_level_0', 'Unnamed: 1_level_0', 'Unnamed: 2_level_0', 'Unnamed: 3_level_0', 'Unnamed: 4_level_0']]
            df = df.rename(columns={"Unnamed: 0_level_0": "Rnd", "Unnamed: 1_level_0": "Pick", "Unnamed: 2_level_0": "Tm", "Unnamed: 3_level_0": "Player", "Unnamed: 4_level_0": "Pos"})
            df = df[df.Rnd != 'Rnd']
            df['Player'] = df['Player'].map(lambda x: x.rstrip(' HOF'))
            df['Year'] = yr
            Draft_DataFrame = pd.concat([Draft_DataFrame, df], ignore_index=True)
        except ImportError:
            time.sleep(2)
    return Draft_DataFrame.to_csv('Draft_DataFrame.csv', index=False)


def listDraftedPlayers(pos, year):
    draftedPlayers = pd.read_csv("../Data/Draft_DataFrame.csv")
    draftedPlayers = draftedPlayers.loc[(draftedPlayers['Pos'] == pos) & (draftedPlayers['Year'] == year)]
    players = draftedPlayers['Player'].tolist()
    return players


def scrapeQB_Stats():
    url_head = 'https://www.pro-football-reference.com/years/'
    years = [str(yr) for yr in range(2000, 2019)]
    QB_DataFrame = pd.DataFrame(columns=['Rk', 'Player', 'Tm', 'Age', 'Pos', 'G', 'GS', 'QBrec', 'Cmp', 'Att',
                                         'Cmp%', 'Yds', 'TD', 'TD%', 'Int', 'Int%', '1D', 'Lng', 'Y/A', 'AY/A',
                                         'Y/C', 'Y/G', 'Rate', 'Sk', 'Yds.1', 'Sk%', 'NY/A', 'ANY/A', '4QC', 'GWD', 'Year'])
    for yr in years:
        players = listDraftedPlayers('QB', int(yr))
        for year in range(int(yr), int(yr)+4):
            try:
                time.sleep(2)
                full_url = url_head + str(year) + '/passing.htm'
                df = pd.read_html(full_url)[0]
                df['Player'] = df['Player'].map(lambda x: x.rstrip('*+'))
                df = df.loc[df['Player'].isin(players)]
                df['Year'] = str(year)
                if 'QBR' in df.columns:
                    df = df.drop('QBR', axis=1)
                QB_DataFrame = pd.concat([QB_DataFrame, df])
            except ImportError:
                time.sleep(2)
    QB_DataFrame['QBrec'] = QB_DataFrame['QBrec'].fillna('0-0-0')
    QB_DataFrame['Win'] = QB_DataFrame['QBrec'].str.split('-').str[0]
    QB_DataFrame['Loss'] = QB_DataFrame['QBrec'].str.split('-').str[1]
    QB_DataFrame['Tie'] = QB_DataFrame['QBrec'].str.split('-').str[2]
    QB_DataFrame = QB_DataFrame.drop('QBrec', axis=1)
    QB_DataFrame = QB_DataFrame.fillna('0')
    QB_DataFrame = QB_DataFrame.astype({'Rk': 'int', 'Player': 'object', 'Tm': 'object', 'Age': 'int', 'Pos': 'object', 'G': 'int', 'GS': 'int', 'Win': 'int', 'Loss': 'int', 'Tie': 'int',
                                        'Cmp': 'int', 'Att': 'int', 'Cmp%': 'float', 'Yds': 'int', 'TD': 'int', 'TD%': 'float', 'Int': 'int', 'Int%': 'float', '1D': 'int', 'Lng': 'int', 'Y/A': 'float', 'AY/A': 'float',
                                        'Y/C': 'float', 'Y/G': 'float', 'Rate': 'float', 'Sk': 'int', 'Yds.1': 'int', 'Sk%': 'float', 'NY/A': 'float', 'ANY/A': 'float', '4QC': 'int', 'GWD': 'int', 'Year': 'object'})
    agg_functions = {'Rk': 'mean', 'Tm': 'last', 'Age': 'last', 'Pos': 'last', 'G': 'sum', 'GS': 'sum', 'Win': 'sum', 'Loss': 'sum', 'Tie': 'sum',
                     'Cmp': 'sum', 'Att': 'sum', 'Cmp%': 'mean', 'Yds': 'sum', 'TD': 'sum', 'TD%': 'mean', 'Int': 'sum', 'Int%': 'mean', '1D': 'sum', 'Lng': 'mean', 'Y/A': 'mean', 'AY/A': 'mean',
                     'Y/C': 'mean', 'Y/G': 'mean', 'Rate': 'mean', 'Sk': 'sum', 'Yds.1': 'sum', 'Sk%': 'mean', 'NY/A': 'mean', 'ANY/A': 'mean', '4QC': 'sum', 'GWD': 'sum', 'Year': 'last'}
    QB_DataFrame = QB_DataFrame.groupby(QB_DataFrame['Player']).aggregate(agg_functions)
    return QB_DataFrame.to_csv('QB_DataFrame.csv', index=True)


def scrapeRB_Stats():
    url_head = 'https://www.pro-football-reference.com/years/'
    years = [str(yr) for yr in range(2000, 2019)]
    RB_DataFrame = pd.DataFrame(columns=['Rk', 'Player', 'Tm', 'Age', 'Pos', 
                                         'G', 'GS', 
                                         'Att', 'Yds', 'TD', '1D', 'Lng', 'Y/A', 'Y/G',
                                         'Fmb', 'Year'])
    for yr in years:
        players = listDraftedPlayers('RB', int(yr))
        for year in range(int(yr), int(yr)+4):
            try:
                time.sleep(2)
                full_url = url_head + str(year) + '/rushing.htm'
                df = pd.read_html(full_url)[0]
                df.columns = df.columns.get_level_values(1)
                df['Player'] = df['Player'].map(lambda x: x.rstrip('*+'))
                df = df.loc[df['Player'].isin(players)]
                df['Year'] = str(year)
                RB_DataFrame = pd.concat([RB_DataFrame, df])
            except ImportError:
                time.sleep(2)
    RB_DataFrame = RB_DataFrame.fillna('0')
    RB_DataFrame = RB_DataFrame.astype({'Rk': 'int', 'Player': 'object', 'Tm': 'object', 'Age': 'int', 'Pos': 'object',
                                        'G': 'int', 'GS': 'int',
                                        'Att': 'int', 'Yds': 'int', 'TD': 'int', '1D': 'int', 'Lng': 'int', 'Y/A': 'float', 'Y/G': 'float',
                                        'Fmb': 'int', 'Year': 'object'})
    agg_functions = {'Rk': 'mean', 'Tm': 'last', 'Age': 'last', 'Pos': 'last', 
                     'G': 'sum', 'GS': 'sum',
                     'Att': 'sum', 'Yds': 'sum', 'TD': 'sum', '1D': 'sum', 'Lng': 'mean', 'Y/A': 'mean', 'Y/G': 'mean', 
                     'Fmb': 'sum', 'Year': 'last'}
    RB_DataFrame = RB_DataFrame.groupby(RB_DataFrame['Player']).aggregate(agg_functions)
    return RB_DataFrame.to_csv('RB_DataFrame.csv', index=True)


def scrapeRB_Stats():
    url_head = 'https://www.pro-football-reference.com/years/'
    years = [str(yr) for yr in range(2000, 2019)]
    RB_DataFrame = pd.DataFrame(columns=['Rk', 'Player', 'Tm', 'Age', 'Pos', 
                                         'G', 'GS', 
                                         'Att', 'Yds', 'TD', '1D', 'Lng', 'Y/A', 'Y/G',
                                         'Fmb', 'Year'])
    for yr in years:
        players = listDraftedPlayers('RB', int(yr))
        for year in range(int(yr), int(yr)+4):
            try:
                time.sleep(2)
                full_url = url_head + str(year) + '/rushing.htm'
                df = pd.read_html(full_url)[0]
                df.columns = df.columns.get_level_values(1)
                df['Player'] = df['Player'].map(lambda x: x.rstrip('*+'))
                df = df.loc[df['Player'].isin(players)]
                df['Year'] = str(year)
                RB_DataFrame = pd.concat([RB_DataFrame, df])
            except ImportError:
                time.sleep(2)
    RB_DataFrame = RB_DataFrame.fillna('0')
    RB_DataFrame = RB_DataFrame.astype({'Rk': 'int', 'Player': 'object', 'Tm': 'object', 'Age': 'int', 'Pos': 'object',
                                        'G': 'int', 'GS': 'int',
                                        'Att': 'int', 'Yds': 'int', 'TD': 'int', '1D': 'int', 'Lng': 'int', 'Y/A': 'float', 'Y/G': 'float',
                                        'Fmb': 'int', 'Year': 'object'})
    agg_functions = {'Rk': 'mean', 'Tm': 'last', 'Age': 'last', 'Pos': 'last', 
                     'G': 'sum', 'GS': 'sum',
                     'Att': 'sum', 'Yds': 'sum', 'TD': 'sum', '1D': 'sum', 'Lng': 'mean', 'Y/A': 'mean', 'Y/G': 'mean', 
                     'Fmb': 'sum', 'Year': 'last'}
    RB_DataFrame = RB_DataFrame.groupby(RB_DataFrame['Player']).aggregate(agg_functions)
    return RB_DataFrame.to_csv('RB_DataFrame.csv', index=True)


def scrapeWR_Stats():
    url_head = 'https://www.pro-football-reference.com/years/'
    years = [str(yr) for yr in range(2000, 2019)]
    WR_DataFrame = pd.DataFrame(columns=['Rk', 'Player', 'Tm', 'Age', 'Pos', 
                                         'G', 'GS', 
                                         'Tgt', 'Rec', 'Ctch%', 'Yds', 'Y/R',
                                         'TD', '1D', 'Lng', 'Y/Tgt', 'R/G', 'Y/G',
                                         'Fmb', 'Year'])
    for yr in years:
        players = listDraftedPlayers('WR', int(yr))
        for year in range(int(yr), int(yr)+4):
            try:
                time.sleep(2)
                full_url = url_head + str(year) + '/receiving.htm'
                df = pd.read_html(full_url)[0]
                df['Player'] = df['Player'].map(lambda x: x.rstrip('*+'))
                df = df[df.Rk != 'Rk']
                df['Ctch%'] = df['Ctch%'].map(lambda x: x.rstrip("%"))
                df = df.loc[df['Player'].isin(players)]
                df['Year'] = str(year)
                WR_DataFrame = pd.concat([WR_DataFrame, df])
            except ImportError:
                time.sleep(2)
    WR_DataFrame = WR_DataFrame.fillna('0')
    WR_DataFrame = WR_DataFrame.astype({'Rk': 'int', 'Player': 'object', 'Tm': 'object', 'Age': 'int', 'Pos': 'object',
                                        'G': 'int', 'GS': 'int',
                                        'Tgt': 'int', 'Rec': 'int', 'Ctch%': 'float', 'Yds': 'int', 'Y/R': 'float',
                                        'TD': 'int', '1D': 'int', 'Lng': 'int', 'Y/Tgt': 'float', 'R/G': 'float', 'Y/G': 'float',
                                        'Fmb': 'int', 'Year': 'object'})
    agg_functions = {'Rk': 'mean', 'Tm': 'last', 'Age': 'last', 'Pos': 'last',
                     'G': 'sum', 'GS': 'sum',
                     'Tgt': 'sum', 'Rec': 'sum', 'Ctch%': 'mean', 'Yds': 'sum', 'Y/R': 'mean',
                     'TD': 'sum', '1D': 'sum', 'Lng': 'mean', 'Y/Tgt': 'mean', 'R/G': 'mean', 'Y/G': 'mean',
                     'Fmb': 'sum', 'Year': 'last'}
    WR_DataFrame = WR_DataFrame.groupby(WR_DataFrame['Player']).aggregate(agg_functions)
    return WR_DataFrame.to_csv('WR_DataFrame.csv', index=True)


def scrapeTE_Stats():
    url_head = 'https://www.pro-football-reference.com/years/'
    years = [str(yr) for yr in range(2000, 2019)]
    TE_DataFrame = pd.DataFrame(columns=['Rk', 'Player', 'Tm', 'Age', 'Pos', 
                                         'G', 'GS', 
                                         'Tgt', 'Rec', 'Ctch%', 'Yds', 'Y/R',
                                         'TD', '1D', 'Lng', 'Y/Tgt', 'R/G', 'Y/G',
                                         'Fmb', 'Year'])
    for yr in years:
        players = listDraftedPlayers('TE', int(yr))
        for year in range(int(yr), int(yr)+4):
            try:
                time.sleep(2)
                full_url = url_head + str(year) + '/receiving.htm'
                df = pd.read_html(full_url)[0]
                df['Player'] = df['Player'].map(lambda x: x.rstrip('*+'))
                df = df[df.Rk != 'Rk']
                df['Ctch%'] = df['Ctch%'].map(lambda x: x.rstrip("%"))
                df = df.loc[df['Player'].isin(players)]
                df['Year'] = str(year)
                TE_DataFrame = pd.concat([TE_DataFrame, df])
            except ImportError:
                time.sleep(2)
    TE_DataFrame = TE_DataFrame.fillna('0')
    TE_DataFrame = TE_DataFrame.astype({'Rk': 'int', 'Player': 'object', 'Tm': 'object', 'Age': 'int', 'Pos': 'object',
                                        'G': 'int', 'GS': 'int',
                                        'Tgt': 'int', 'Rec': 'int', 'Ctch%': 'float', 'Yds': 'int', 'Y/R': 'float',
                                        'TD': 'int', '1D': 'int', 'Lng': 'int', 'Y/Tgt': 'float', 'R/G': 'float', 'Y/G': 'float',
                                        'Fmb': 'int', 'Year': 'object'})
    agg_functions = {'Rk': 'mean', 'Tm': 'last', 'Age': 'last', 'Pos': 'last',
                     'G': 'sum', 'GS': 'sum',
                     'Tgt': 'sum', 'Rec': 'sum', 'Ctch%': 'mean', 'Yds': 'sum', 'Y/R': 'mean',
                     'TD': 'sum', '1D': 'sum', 'Lng': 'mean', 'Y/Tgt': 'mean', 'R/G': 'mean', 'Y/G': 'mean',
                     'Fmb': 'sum', 'Year': 'last'}
    TE_DataFrame = TE_DataFrame.groupby(TE_DataFrame['Player']).aggregate(agg_functions)
    return TE_DataFrame.to_csv('TE_DataFrame.csv', index=True)


def scrapeDE_Stats():
    url_head = 'https://www.pro-football-reference.com/years/'
    years = [str(yr) for yr in range(2000, 2019)]
    DE_DataFrame = pd.DataFrame(columns=['Rk', 'Player', 'Tm', 'Age', 'Pos', 
                                         'G', 'GS',
                                         'Intcpt', 'IntYds', 'IntTD', 'Lng', 'PD',
                                         'FF', 'Fmb', 'FR', 'FumYds', 'FumTD',
                                         'Sk', 'Comb', 'Solo', 'Ast', 'TFL',
                                         'QBHits', 'Sfty', 'Year'])
    for yr in years:
        players = listDraftedPlayers('DE', int(yr))
        for year in range(int(yr), int(yr)+4):
            try:
                time.sleep(2)
                full_url = url_head + str(year) + '/defense.htm'
                df = pd.read_html(full_url)[0]
                leftTemp = df[[('Unnamed: 0_level_0', 'Rk'), ('Unnamed: 1_level_0', 'Player'), ('Unnamed: 2_level_0', 'Tm'), ('Unnamed: 3_level_0', 'Age'), ('Unnamed: 4_level_0', 'Pos'),
                               ('Games', 'G'),('Games', 'GS'),
                               ('Def Interceptions', 'Int'), ('Def Interceptions', 'Yds'), ('Def Interceptions', 'TD'), ('Def Interceptions', 'Lng'), ('Def Interceptions', 'PD')]]
                leftTemp.columns = leftTemp.columns.get_level_values(1)
                rightTemp = df[[('Fumbles', 'FF'), ('Fumbles', 'Fmb'), ('Fumbles', 'FR'), ('Fumbles', 'Yds'), ('Fumbles', 'TD'), 
                                ('Unnamed: 17_level_0', 'Sk'), ('Tackles', 'Comb'), ('Tackles', 'Solo'), ('Tackles', 'Ast'), ('Tackles', 'TFL'), ('Tackles', 'QBHits'), ('Unnamed: 23_level_0', 'Sfty')]]
                rightTemp.columns = rightTemp.columns.get_level_values(1)
                leftTemp = leftTemp.rename(columns = {'Int': 'Intcpt', 'Yds': 'IntYds', 'TD': 'IntTD'})
                rightTemp = rightTemp.rename(columns = {'Yds': 'FumYds', 'TD': 'FumTD'})
                df = leftTemp.join(rightTemp)
                df['Player'] = df['Player'].map(lambda x: x.rstrip('*+'))
                df = df[df.Rk != 'Rk']
                df = df.loc[df['Player'].isin(players)]
                df['Year'] = str(year)
                DE_DataFrame = pd.concat([DE_DataFrame, df])
            except ImportError:
                time.sleep(2)
    DE_DataFrame = DE_DataFrame.fillna('0')
    DE_DataFrame = DE_DataFrame.astype({'Rk': 'int', 'Player': 'object', 'Tm': 'object', 'Age': 'int', 'Pos': 'object',
                                        'G': 'int', 'GS': 'int',
                                        'Intcpt': 'int', 'IntYds': 'int', 'IntTD': 'int', 'Lng': 'int', 'PD': 'int',
                                        'FF': 'int', 'Fmb': 'int', 'FR': 'int', 'FumYds': 'int', 'FumTD': 'int',
                                        'Sk': 'float', 'Comb': 'int', 'Solo': 'int', 'Ast': 'int', 'TFL': 'int',
                                        'QBHits': 'int', 'Sfty': 'int', 'Year': 'object'})
    agg_functions = {'Rk': 'mean', 'Tm': 'last', 'Age': 'last', 'Pos': 'last',
                     'G': 'sum', 'GS': 'sum',
                     'Intcpt': 'sum', 'IntYds': 'sum', 'IntTD': 'sum', 'Lng': 'mean', 'PD': 'sum',
                     'FF': 'sum', 'Fmb': 'sum', 'FR': 'sum', 'FumYds': 'sum', 'FumTD': 'sum',
                     'Sk': 'sum', 'Comb': 'sum', 'Solo': 'sum', 'Ast': 'sum', 'TFL': 'sum',
                     'QBHits': 'sum', 'Sfty': 'sum', 'Year': 'last'}
    DE_DataFrame = DE_DataFrame.groupby(DE_DataFrame['Player']).aggregate(agg_functions)
    return DE_DataFrame.to_csv('DE_DataFrame.csv', index=True)


def scrapeDB_Stats():
    url_head = 'https://www.pro-football-reference.com/years/'
    years = [str(yr) for yr in range(2000, 2019)]
    DB_DataFrame = pd.DataFrame(columns=['Rk', 'Player', 'Tm', 'Age', 'Pos', 
                                         'G', 'GS',
                                         'Intcpt', 'IntYds', 'IntTD', 'Lng', 'PD',
                                         'FF', 'Fmb', 'FR', 'FumYds', 'FumTD',
                                         'Sk', 'Comb', 'Solo', 'Ast', 'TFL',
                                         'QBHits', 'Sfty', 'Year'])
    for yr in years:
        players = listDraftedPlayers('DB', int(yr))
        for year in range(int(yr), int(yr)+4):
            try:
                time.sleep(2)
                full_url = url_head + str(year) + '/defense.htm'
                df = pd.read_html(full_url)[0]
                leftTemp = df[[('Unnamed: 0_level_0', 'Rk'), ('Unnamed: 1_level_0', 'Player'), ('Unnamed: 2_level_0', 'Tm'), ('Unnamed: 3_level_0', 'Age'), ('Unnamed: 4_level_0', 'Pos'),
                               ('Games', 'G'),('Games', 'GS'),
                               ('Def Interceptions', 'Int'), ('Def Interceptions', 'Yds'), ('Def Interceptions', 'TD'), ('Def Interceptions', 'Lng'), ('Def Interceptions', 'PD')]]
                leftTemp.columns = leftTemp.columns.get_level_values(1)
                rightTemp = df[[('Fumbles', 'FF'), ('Fumbles', 'Fmb'), ('Fumbles', 'FR'), ('Fumbles', 'Yds'), ('Fumbles', 'TD'), 
                                ('Unnamed: 17_level_0', 'Sk'), ('Tackles', 'Comb'), ('Tackles', 'Solo'), ('Tackles', 'Ast'), ('Tackles', 'TFL'), ('Tackles', 'QBHits'), ('Unnamed: 23_level_0', 'Sfty')]]
                rightTemp.columns = rightTemp.columns.get_level_values(1)
                leftTemp = leftTemp.rename(columns = {'Int': 'Intcpt', 'Yds': 'IntYds', 'TD': 'IntTD'})
                rightTemp = rightTemp.rename(columns = {'Yds': 'FumYds', 'TD': 'FumTD'})
                df = leftTemp.join(rightTemp)
                df['Player'] = df['Player'].map(lambda x: x.rstrip('*+'))
                df = df[df.Rk != 'Rk']
                df = df.loc[df['Player'].isin(players)]
                df['Year'] = str(year)
                DB_DataFrame = pd.concat([DB_DataFrame, df])
            except ImportError:
                time.sleep(2)
    DB_DataFrame = DB_DataFrame.fillna('0')
    DB_DataFrame = DB_DataFrame.astype({'Rk': 'int', 'Player': 'object', 'Tm': 'object', 'Age': 'int', 'Pos': 'object',
                                        'G': 'int', 'GS': 'int',
                                        'Intcpt': 'int', 'IntYds': 'int', 'IntTD': 'int', 'Lng': 'int', 'PD': 'int',
                                        'FF': 'int', 'Fmb': 'int', 'FR': 'int', 'FumYds': 'int', 'FumTD': 'int',
                                        'Sk': 'float', 'Comb': 'int', 'Solo': 'int', 'Ast': 'int', 'TFL': 'int',
                                        'QBHits': 'int', 'Sfty': 'int', 'Year': 'object'})
    agg_functions = {'Rk': 'mean', 'Tm': 'last', 'Age': 'last', 'Pos': 'last',
                     'G': 'sum', 'GS': 'sum',
                     'Intcpt': 'sum', 'IntYds': 'sum', 'IntTD': 'sum', 'Lng': 'mean', 'PD': 'sum',
                     'FF': 'sum', 'Fmb': 'sum', 'FR': 'sum', 'FumYds': 'sum', 'FumTD': 'sum',
                     'Sk': 'sum', 'Comb': 'sum', 'Solo': 'sum', 'Ast': 'sum', 'TFL': 'sum',
                     'QBHits': 'sum', 'Sfty': 'sum', 'Year': 'last'}
    DB_DataFrame = DB_DataFrame.groupby(DB_DataFrame['Player']).aggregate(agg_functions)
    return DB_DataFrame.to_csv('DB_DataFrame.csv', index=True)


def scrapeLB_Stats():
    url_head = 'https://www.pro-football-reference.com/years/'
    years = [str(yr) for yr in range(2000, 2019)]
    LB_DataFrame = pd.DataFrame(columns=['Rk', 'Player', 'Tm', 'Age', 'Pos', 
                                         'G', 'GS',
                                         'Intcpt', 'IntYds', 'IntTD', 'Lng', 'PD',
                                         'FF', 'Fmb', 'FR', 'FumYds', 'FumTD',
                                         'Sk', 'Comb', 'Solo', 'Ast', 'TFL',
                                         'QBHits', 'Sfty', 'Year'])
    for yr in years:
        players = listDraftedPlayers('DB', int(yr))
        for year in range(int(yr), int(yr)+4):
            try:
                time.sleep(2)
                full_url = url_head + str(year) + '/defense.htm'
                df = pd.read_html(full_url)[0]
                leftTemp = df[[('Unnamed: 0_level_0', 'Rk'), ('Unnamed: 1_level_0', 'Player'), ('Unnamed: 2_level_0', 'Tm'), ('Unnamed: 3_level_0', 'Age'), ('Unnamed: 4_level_0', 'Pos'),
                               ('Games', 'G'),('Games', 'GS'),
                               ('Def Interceptions', 'Int'), ('Def Interceptions', 'Yds'), ('Def Interceptions', 'TD'), ('Def Interceptions', 'Lng'), ('Def Interceptions', 'PD')]]
                leftTemp.columns = leftTemp.columns.get_level_values(1)
                rightTemp = df[[('Fumbles', 'FF'), ('Fumbles', 'Fmb'), ('Fumbles', 'FR'), ('Fumbles', 'Yds'), ('Fumbles', 'TD'), 
                                ('Unnamed: 17_level_0', 'Sk'), ('Tackles', 'Comb'), ('Tackles', 'Solo'), ('Tackles', 'Ast'), ('Tackles', 'TFL'), ('Tackles', 'QBHits'), ('Unnamed: 23_level_0', 'Sfty')]]
                rightTemp.columns = rightTemp.columns.get_level_values(1)
                leftTemp = leftTemp.rename(columns = {'Int': 'Intcpt', 'Yds': 'IntYds', 'TD': 'IntTD'})
                rightTemp = rightTemp.rename(columns = {'Yds': 'FumYds', 'TD': 'FumTD'})
                df = leftTemp.join(rightTemp)
                df['Player'] = df['Player'].map(lambda x: x.rstrip('*+'))
                df = df[df.Rk != 'Rk']
                df = df.loc[df['Player'].isin(players)]
                df['Year'] = str(year)
                LB_DataFrame = pd.concat([LB_DataFrame, df])
            except ImportError:
                time.sleep(2)
    LB_DataFrame = LB_DataFrame.fillna('0')
    LB_DataFrame = LB_DataFrame.astype({'Rk': 'int', 'Player': 'object', 'Tm': 'object', 'Age': 'int', 'Pos': 'object',
                                        'G': 'int', 'GS': 'int',
                                        'Intcpt': 'int', 'IntYds': 'int', 'IntTD': 'int', 'Lng': 'int', 'PD': 'int',
                                        'FF': 'int', 'Fmb': 'int', 'FR': 'int', 'FumYds': 'int', 'FumTD': 'int',
                                        'Sk': 'float', 'Comb': 'int', 'Solo': 'int', 'Ast': 'int', 'TFL': 'int',
                                        'QBHits': 'int', 'Sfty': 'int', 'Year': 'object'})
    agg_functions = {'Rk': 'mean', 'Tm': 'last', 'Age': 'last', 'Pos': 'last',
                     'G': 'sum', 'GS': 'sum',
                     'Intcpt': 'sum', 'IntYds': 'sum', 'IntTD': 'sum', 'Lng': 'mean', 'PD': 'sum',
                     'FF': 'sum', 'Fmb': 'sum', 'FR': 'sum', 'FumYds': 'sum', 'FumTD': 'sum',
                     'Sk': 'sum', 'Comb': 'sum', 'Solo': 'sum', 'Ast': 'sum', 'TFL': 'sum',
                     'QBHits': 'sum', 'Sfty': 'sum', 'Year': 'last'}
    LB_DataFrame = LB_DataFrame.groupby(LB_DataFrame['Player']).aggregate(agg_functions)
    return LB_DataFrame.to_csv('LB_DataFrame.csv', index=True)