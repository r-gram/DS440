import pandas as pd
import numpy as np

Draft_Salary = pd.read_csv("../Data/DraftandSalaries_DataFrame.csv")
CapByYear = pd.read_csv("../Data/SalaryCapByYear.csv")

#Read each player row by row
Draft_Salary = Draft_Salary.dropna(subset=['ConLenR', 'ConLen'], how='all')
Draft_Salary = Draft_Salary.astype({'ConSal': 'float'})
Draft_Salary = Draft_Salary.fillna(0.0)
Draft_Salary['PPY'] = Draft_Salary['ConSal'] / Draft_Salary['ConLen']
salary = list(Draft_Salary['PPY'])
CapDict = dict(zip(CapByYear.Year, CapByYear.Cap))
capCol = []
i = 0

for year, conlen, ppy in zip(Draft_Salary['Year'], Draft_Salary['ConLen'], Draft_Salary['PPY']):
    years = [yr for yr in range(int(year+4), int(year+conlen+4))]
    percCap = 0
    for yr in years:
    	if yr < 2021:
    	    percCap += salary[i] / CapDict[yr]
    if conlen != 0:
    	percCap = percCap / conlen
    capCol.append(percCap)
    i += 1

Draft_Salary['%Cap'] = capCol

Draft_Salary.to_csv('DraftandSalaries_DataFrame.csv', index=True)

    #Get year drafted, post rookie contract length, post rookie contract price
    #Divide contract price by contract length to get salary/yr
    #Find year drafted in CapByYear and get cap and get the next (l) years' cap
    #Get %OfCap for each year found using salary/yr
    #get average %OfCap
