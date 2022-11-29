import pandas as pd
import pickle
from scipy.stats import poisson

dict_table = pickle.load(open('tabledict','rb'))
df_historical_data = pd.read_csv('clean_worldcup_matches.csv')
df_fixtures = pd.read_csv('clean_worldcup_fixtures.csv')

df_home = df_historical_data[['HomeTeam', 'HomeGoals','AwayGoals']]
df_away = df_historical_data[['AwayTeam', 'HomeGoals','AwayGoals']]

df_home = df_home.rename(columns={'HomeTeam': 'Team','HomeGoals': 'GoalsScored', 'AwayGoals': 'GoalsConceded'})
df_away = df_away.rename(columns={'AwayTeam': 'Team','HomeGoals': 'GoalsConceded', 'AwayGoals': 'GoalsScored'})

df_team_strength = pd.concat([df_home, df_away], ignore_index=True).groupby(['Team']).mean()
#print(df_team_strength)

def predict_points(home,away):
    if home in df_team_strength.index and away in df_team_strength.index:
        lamb_home = df_team_strength.at[home,'GoalsScored'] * df_team_strength.at[away,'GoalsConceded']
        lamb_away = df_team_strength.at[away,'GoalsScored'] * df_team_strength.at[home,'GoalsConceded']
        prob_home, prob_away, prob_draw = 0, 0, 0
        for x in range(0,11):
            for y in range(0,11):
                p = poisson.pmf(x,lamb_home) * poisson.pmf(y, lamb_away)
                if x == y:
                    prob_draw += p
                elif x > y:
                    prob_home += p
                else:
                    prob_away += p

        points_home = 3 * prob_home + prob_draw
        points_away = 3 * prob_away + prob_draw
        return(points_home,points_away)
    else:
        return (0,0)

print(predict_points('Brazil','Switzerland'))
print(predict_points('Portugal','Uruguay'))
print(predict_points('Netherlands','Qatar'))

#WorldCup Prediction


df_group_stage = df_fixtures[:48].copy()
df_round_of16 = df_fixtures[48:56].copy()
df_quarter_final = df_fixtures[56:60].copy()
df_semi_final = df_fixtures[60:62].copy()
df_final = df_fixtures[62:].copy()

#print(dict_table.keys())

for group in dict_table:
    teams_in_group = dict_table[group]['Team'].values 
    df_fixture_group = df_group_stage[df_group_stage['home'].isin(teams_in_group)]
    for index, row in df_fixture_group.iterrows():
        home, away = row['home'], row['away']
        points_home, points_away = predict_points(home, away)
#Error out with brackets in Pts column
        #dict_table[group].loc[dict_table[group]['Team'] == home, 'Pts'] + (points_home)
        #dict_table[group].loc[dict_table[group]['Team'] == away, 'Pts'] += (points_away)
    
    dict_table[group] = dict_table[group].sort_values('Pts', ascending=False).reset_index()
    dict_table[group] = dict_table[group][['Team','Pts']]
    dict_table[group] = dict_table[group].round(0)

print(df_round_of16)

for group in dict_table:
    group_winner = dict_table[group].loc[0,'Team']
    runners_up = dict_table[group].loc[1,'Team']
    df_round_of16.replace({f'Winners {group}':group_winner,
     f'Runners-up {group}':runners_up}, inplace= True)
df_round_of16['winner'] = '?'
print(df_round_of16)

def get_winner(df_fixture_update):
    for index, row in df_fixture_update.iterrows():
        home, away = row['home'], row['away']
        points_home, points_away = predict_points(home,away)
        if points_home > points_away:
            winner = home
        else:
            winner = away
        df_fixture_update.loc[index, 'winner'] = winner
    return df_fixture_update

print(get_winner(df_round_of16))

def update_table(df_round_1, df_round_2):
    for index, row in df_round_1.iterrows():
        winner = df_round_1.loc[index, 'winner']
        match = df_round_1.loc[index, 'score']
        df_round_2.replace({f'Winners {match}':winner}, inplace=True)
    df_round_2['winner'] = '?'
    return df_round_2

update_table(df_round_of16, df_quarter_final)

print(get_winner(df_quarter_final))

update_table(df_quarter_final, df_semi_final)

print(get_winner(df_semi_final))

update_table(df_semi_final, df_final)

print(get_winner(df_final))