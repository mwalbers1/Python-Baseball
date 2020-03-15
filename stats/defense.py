import pandas as pd
import matplotlib.pyplot as plt
from frames import games, info, events

# In this module we will answer the question: 'What is the DER by league since 1978?'
# Note: 'DER' stands for 'Defensive Efficiency Ratio', and is used as a metric to gauge team defense.

# 2. Query function
plays = games.query('type=="play" & event!="NP"')
#print(plays.head(10))

# 3. column labels
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']
#print(plays.head())

# 4 Shift DataFrame
pa = plays.loc[plays['player'].shift() != plays['player'], ['year', 'game_id', 'inning', 'team', 'player']]
#print(pa.head())

# 5. group plate appearances
pa = pa.groupby(['year', 'game_id', 'team']).size().reset_index(name='PA')
#print(pa.head())

# 6. Set the index
events = events.set_index(['year', 'game_id', 'team', 'event_type'])
#print(events.head())

# 7. Unstack the DataFrame
events = events.unstack().fillna(0).reset_index()
#print(events.head(10))

# 8. Manager column labels
events.columns = events.columns.droplevel()
events.columns = ['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE', 'SO']
events = events.rename_axis(None, axis='columns')
#print(events.head())

# 9. Merge - plate appearances
events_plus_pa = pd.merge(events, pa, how='outer', left_on=['year', 'game_id', 'team'], right_on=['year', 'game_id', 'team'])
#print(events_plus_pa.head())

# 10. Merge - team
#print(info.head())
defense = pd.merge(events_plus_pa, info)
#print(defense.head())

# 11. Calculate DER
defense.loc[:, 'DER'] = 1 - ((defense['H']+defense['ROE'])/(defense['PA'] - defense['BB'] - defense['SO'] - defense['HBP'] - defense['HR']))
defense.loc[:, 'year'] = pd.to_numeric(defense.loc[:,'year'])
#print(defense.head())

# 12. Reshape with pivot
der = defense.loc[defense['year'] >= 1978, ['year', 'defense', 'DER']]
der = der.pivot(index='year', columns='defense', values='DER')
print(der.head(25))

# 13. Plot formatting - xticks
der.plot(x_compat='True', xticks=range(1978, 2018, 4), rot=45)
plt.show()
