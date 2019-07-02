import pandas as pd
import spacy
nlp = spacy.load('en')

data = pd.read_csv('/Users/claraliu/Downloads/whitepages_337k.csv')
#initialize individual 
data['individual'] = 0

#step 1
#set non-commercial location to individual
data.loc[data['Location is Commercial'] == False, 'individual'] = 1

data['Name'].fillna("", inplace = True)
for i in data.loc[data['Location is Commercial'] == True, 'Name'].index:
    name = nlp(data.loc[i, 'Name'])
    for ent in name.ents:
        #step 2
        # use spacy to determine
        if ent.label_ == 'PERSON': 
            data.loc[i, 'individual'] = 1
        else:
            #step 3
            #if the second part of the name is one letter
            if len(name.split()) > 1:
                if len(name.split()[1]) == 1 and len(name.split()[0]) != 1 and name.split()[1].isalpha():
                    data.loc[i, 'individual'] = 1

def fi(x):
    if x != "":
        if x.split()[0] in ["Ms.", "Mr."]:
            return x.split()[1]
        else:
            return x.split()[0]
    else:
        return x
    
def la(x):
    if x != "":
        if x.split()[-1] in ["Jr.", "Sr.", "I", "II", "III", "IV", "V", "VI", "VII"]:
            return x.split()[-2]
        else:
            return x.split()[-1]
    else:
        return x

#create first name & last name
indi = data[data['individual'] == 1]
indi['First Name'] = indi['Name'].apply(fi)
indi['Last Name'] = indi['Name'].apply(la)

indi.to_csv('/Users/claraliu/Downloads/whitepages_336k_individual.csv', index = False)

