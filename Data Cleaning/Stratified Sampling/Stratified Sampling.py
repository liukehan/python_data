import pandas as pd

data = pd.read_csv('..\data.csv')
gbr = data.groupby("property_id")['Address Result Type'].count()
target = pd.DataFrame(gbr).sort_values(by = 'Address Result Type', axis = 0, ascending = False)
target.columns = ['num']

def StratifiedSampling(group, typicalFracDict):
    name = group.name
    frac = typicalFracDict[name]
    return group.sample(frac = frac)

StratifiedFracDict = {}
for property in target.iloc[:2404].index:
    StratifiedFracDict[property] = 0.8
for property in target.iloc[2404:].index:
    StratifiedFracDict[property] = 1

print(len(StratifiedFracDict))

result = data.groupby('property_id', group_keys = False).apply(StratifiedSampling, StratifiedFracDict)
result.to_csv('results.csv')
target.to_csv('target.csv')

