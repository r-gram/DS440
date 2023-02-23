import pandas as pd
'''
qbDF = pd.read_csv("../Data/QBMerged_Dataframe.csv")
percCAP = pd.read_csv("../Data/PercentOfCap_DataFrame.csv")

percCAP = percCAP.drop(['Unnamed: 0'], axis=1)
qbDF = qbDF.drop(['Year'], axis=1)
feeder = pd.merge(qbDF, percCAP,  how='left', left_on=['Player'], right_on = ['Player'])

feeder = feeder.drop(['Tm_x', 'Pos_x', 'Tm_y', 'Pos_y'], axis=1)

feeder = feeder.astype({'Rk': 'float', 'Age': 'float', 'G': 'float', 'GS': 'float', 'Win': 'float', 'Loss': 'float', 'Tie': 'float',
                        'Cmp': 'float', 'Att': 'float', 'Cmp%': 'float', 'Yds': 'float', 'TD': 'float', 'TD%': 'float', 'Int': 'float', 'Int%': 'float', '1D': 'float', 'Lng': 'float',
                        'Y/A': 'float', 'AY/A': 'float', 'Y/C': 'float', 'Y/G': 'float', 'Rate': 'float', 'Sk': 'float', 'Yds.1': 'float', 'Sk%': 'float', 'NY/A': 'float',
                        'ANY/A': 'float', '4QC': 'float', 'GWD': 'float', 'Lng_R': 'float', 'Fmb': 'float', 'Att_R': 'float', 'Yds_R': 'float', 'TD_R': 'float',
                        '1D_R': 'float', 'Y/A_R': 'float', 'Y/G_R': 'float', 'Rnd': 'float', 'Pick': 'float', 'Year': 'float', 'ConLenR': 'float',
                        'ConSalR': 'float', 'ConLen': 'float', 'ConSal': 'float', 'FTag': 'float', 'PPY': 'float', '%Cap': 'float'})

feeder = feeder.round(4)
feeder.to_csv('feeder.csv', index=False)
'''

feeder = pd.read_csv("../Code/feeder.csv")
feeder = feeder.astype({'Rk': 'float', 'Age': 'float', 'G': 'float', 'GS': 'float', 'Win': 'float', 'Loss': 'float', 'Tie': 'float',
                        'Cmp': 'float', 'Att': 'float', 'Cmp%': 'float', 'Yds': 'float', 'TD': 'float', 'TD%': 'float', 'Int': 'float', 'Int%': 'float', '1D': 'float', 'Lng': 'float',
                        'Y/A': 'float', 'AY/A': 'float', 'Y/C': 'float', 'Y/G': 'float', 'Rate': 'float', 'Sk': 'float', 'Yds.1': 'float', 'Sk%': 'float', 'NY/A': 'float',
                        'ANY/A': 'float', '4QC': 'float', 'GWD': 'float', 'Lng_R': 'float', 'Fmb': 'float', 'Att_R': 'float', 'Yds_R': 'float', 'TD_R': 'float',
                        '1D_R': 'float', 'Y/A_R': 'float', 'Y/G_R': 'float', 'Rnd': 'float', 'Pick': 'float', 'Year': 'float', 'ConLenR': 'float',
                        'ConSalR': 'float', 'ConLen': 'float', 'ConSal': 'float', 'FTag': 'float', 'PPY': 'float', '%Cap': 'float'})

feeder.to_csv('feeder.csv', index=False)