import pandas as pd
import datetime as DT
import copy
from textblob import TextBlob

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

data = pd.read_csv('..\data.csv')

li = ['id']
li = [column for column in data.columns if 'snippet' in column or 'text' in column or 'title' in  column]

negative = ['fraud','panloloko','fraudulent','mapanlinlang','scam','scandal','crime','krimen','criminal','kriminal','investigation'
'convict','convicted','terror','malaking takot','terrorist','terorista','terrorism','lawsuit','tax_lien','tax lien','indictment',
'money laundering','arrested']

#calculate count of legal words and sentiment polarity
for i in data.index:
    for word in negative:
        data.loc[i, 'count of '+ word] = TextBlob(str(data.loc[i])).words.count(word, case_sensitive=False)
    data.loc[i,'polarity']=TextBlob(str(data.loc[i])).sentiment.polarity

