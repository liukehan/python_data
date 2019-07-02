
# coding: utf-8
import pandas as pd
from urllib import parse,request
import requests
import ast


#Define Flatten Json Function
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

folder = '..'
data = pd.read_csv(folder + 'input.csv')

#Run API
for i in range(len(data)):
    try:
        #can add more parametes if necessary
        url = 'url' + "%20".join(data['name'][i].split()) + '&country_code=us'
        req = requests.get(url=url)
        out = pd.DataFrame(flatten_json(req.json()), index = [data['client_id'][i]])
    except:
        out = pd.DataFrame({}, index = [data['client_id'][i]])
    if i == 100:
        final = out
    else:
        final = pd.concat([final, out])

final.dropna(axis = 1, thresh = 1, inplace = True)
final.to_csv('..')
