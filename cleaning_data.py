import pandas as pd

df_historical_data = pd.read_csv('worldcup_history_data.csv')
df_fixture = pd.read_csv('worldcup_fixtures.csv')
df_missing_data = pd.read_csv('world_cup_missing_data.csv')

df_fixture['home'] = df_fixture['home'].str.strip()
df_fixture['away'] = df_fixture['away'].str.strip()

df_missing_data.dropna(inplace=True) #drop null data

df_historical_data = pd.concat([df_historical_data,df_missing_data], ignore_index=True)
df_historical_data.drop_duplicates(inplace=True)
df_historical_data.sort_values('year', inplace=True)

#print(df_historical_data)

delete_index = df_historical_data[df_historical_data['home'].str.contains('Sweden') & df_historical_data['away'].str.contains('Austria')].index

df_historical_data.drop(index=delete_index, inplace=True)

df_historical_data['score'] = df_historical_data['score'].str.replace('[^\d–]', '',regex =True)
df_historical_data['home']= df_historical_data['home'].str.strip()
df_historical_data['away']= df_historical_data['away'].str.strip()

df_historical_data[['HomeGoals', 'AwayGoals']] = df_historical_data['score'].str.split('–', expand=True)
df_historical_data.drop('score', axis=1, inplace= True)

df_historical_data.rename(columns={'home':'HomeTeam','away':'AwayTeam','year': 'Year'},
inplace=True)

df_historical_data = df_historical_data.astype({'HomeGoals':int, 'AwayGoals':int,'Year':int})
df_historical_data['TotalGoals'] =df_historical_data['HomeGoals'] + df_historical_data['AwayGoals']

print(df_historical_data)

df_historical_data.to_csv('clean_worldcup_matches.csv', index =False)
df_fixture.to_csv('clean_worldcup_fixtures.csv', index=False)

years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
         2018]

for year in years:
    print(year, len(df_historical_data[df_historical_data['Year']==year]))

print(df_historical_data[df_historical_data['HomeTeam'].str.contains('Mexico')])
print(df_historical_data[df_historical_data['AwayTeam'].str.contains('Mexico')])