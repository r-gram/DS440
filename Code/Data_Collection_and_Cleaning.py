import pandas as pd
import numpy as np
import time

#Read in data
'''
def draft_2017():
    draft2017DF = pd.read_csv("../Data/NFL_2017_Draft.csv")
    return draft2017DF
def salaries_2017():
    salaries2017DF = pd.read_csv("../Data/NFL_2017_Player_Salaries.csv")
    return salaries2017DF

#Get only player, team, and their salary
def clean_sal():
	temp = salaries_2017()
	salaries2017 = temp[['Player', 'Tm', 'Cap Hit']]
	return salaries2017

def rename_draft():
    temp = draft_2017()
    #Rename Columns
    #Rnd=Draft Round, Pick=Overall Pick, Tm=Team, Player, Pos=Position, 
    #Age, To=Stats up to, AP1=First team all-pro, PB=Pro Bowl, St=Number of years as starter, 
    #G=games played, Cmp=passes completed, Att=passes attempted, Yds=passing yards, TD=passing tds, 
    #Int=ints thrown, Att.1=rushing attempts, Yds.1=rushing yrds, TD.1=rushing tds, Rec=receptions,
    #Yds.2=rec yards, TD.2=rec tds, Solo=solo tackles, Int.1=defensive int, Sk=sacks, -9999=unique id
    draft2017 = temp.rename(columns={'Rnd': 'Rnd', 'Pick': 'Pick', 'Tm': 'Tm', 'Player': 'Player', 'Pos': 'Pos', 'Age': 'Age', 'To': 'To', 'AP1': 'AP1', 'PB': 'PB', 'St': 'St', 'G': 'G', 'Cmp': 'Cmp', 'Att': 'PassAtt', 'Yds': 'PassYds', 'TD': 'PassTD', 'Int': 'PassInt', 'Att.1': 'RushAtt', 'Yds.1': 'RushYds', 'TD.1': 'RushTD', 'Rec': 'Rec', 'Yds.2': 'RecYds', 'TD.2': 'RecTD', 'Solo': 'DefSolo', 'Int.1': 'DefInt', 'Sk': 'DefSk', '-9999': 'id'})
    return draft2017
def rename_salary():
    temp = clean_sal()
    salaries2017 = temp.rename(columns={'Cap Hit': 'BaseSal'})
    return salaries2017

def joinDraftAndSalaries():
    draft2017 = rename_draft()
    salaries2017 = rename_salary()
    #Get 2017 Draft class salaries
    joinLeft = pd.merge(left=draft2017, right=salaries2017, how='left', left_on=['Player', 'Tm'], right_on=['Player', 'Tm'])
    return joinLeft

def saveDaS():
    return joinDraftAndSalaries().to_csv('Draft&Salaries2017.csv', index=False)
    #Some Salaries were not complete so the missing values were manually added

#Get the id of drafted players
def getPlayerID(pos):
    df = rename_draft()
    players = df.loc[df['Pos'] == pos]
    player_ids = list(players['id'])
    return player_ids
'''

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