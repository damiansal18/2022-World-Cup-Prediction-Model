import pandas as pd
import pickle
from string import ascii_uppercase as alphabet

allTables = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup') 


tabledict= {}

for letter, i in zip(alphabet, range(13,69,7)):
    print(i)
    df = allTables[i]
    df.rename(columns={df.columns[1]: 'Team'}, inplace = True)
    df.pop('Qualification')
    tabledict[f'Group {letter}'] = df

print(tabledict.keys())

with open('tabledict','wb') as output:
    pickle.dump(tabledict, output)