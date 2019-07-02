
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data = pd.read_csv('D:\Clients\Attune\jan 2019 project\output\whitepages_337k.csv')


# In[ ]:


gbr = data.groupby("property_id")['Address Result Type'].count()
target=pd.DataFrame(gbr).sort_values(by = 'Address Result Type', axis = 0, ascending = False)
target.columns=['num']


# In[25]:


def StratifiedSampling(group, typicalFracDict):
    name = group.name
    frac = typicalFracDict[name]
    return group.sample(frac = frac)


# In[59]:


# create sample dictionary
StratifiedFracDict = {}
for property in target.iloc[:2404].index:
    StratifiedFracDict[property] = 0.8
for property in target.iloc[2404:].index:
    StratifiedFracDict[property] = 1


# In[60]:


len(StratifiedFracDict)


# In[61]:


result = data.groupby('property_id', group_keys = False).apply(StratifiedSampling, StratifiedFracDict)


# In[66]:


result.to_csv('D:\Clients\Attune\jan 2019 project\output\whitepages_290k.csv')


# In[68]:


target.to_csv('D:\Clients\Attune\jan 2019 project\output\sorted_buildings.csv')

