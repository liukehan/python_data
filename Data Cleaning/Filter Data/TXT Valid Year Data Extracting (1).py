
# coding: utf-8

# In[35]:


import os
import pandas
import codecs
import glob
import pandas as pd
import csv


# In[124]:


os.getcwd()
os.chdir('..\')


# In[ ]:


files = glob.glob('*.txt')    
    
for filename in files:  
    print(filename)  
    fopen=codecs.open(filename,'r',encoding='utf-8')  
    lines=[]  
    lines=fopen.readlines()  
    fopen.close()  
    print(len(lines))

    f = open('..\' + filename.split('.')[0] + '.csv', 'w', encoding='utf-8')
    writer = csv.writer(f, lineterminator = '\n')
    count = 0
    for line in lines:   
        if int(line.split('\t')[5]) >= 2017:
            writer.writerow(line.split('\t'))
            count += 1
    f.close()
    print(count)

