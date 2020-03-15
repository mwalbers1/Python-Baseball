import pandas as pd
import matplotlib.pyplot as plt
from data import games

# 1. Select All plays
plays = games[games['type']=='play']
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']
#print(plays.head())

# 2. Select only hits
hits = plays.loc[plays['event'].str.contains('^(?:S(?!B)|D|T|HR)'), ['inning', 'event']]
#print(hits.head())

# 3. Convert column type
hits.loc[:, 'inning'] = pd.to_numeric(hits.loc[:, 'inning'])
#print(hits.info())

# 4.replace dictionary
replacements = {r'^S(.*)':'single',
                r'^D(.*)': 'double',
                r'^T(.*)': 'triple',
                r'^HR(.*)': 'hr'}
#print(replacements)

# 5. replace function
hit_type = hits['event'].replace(replacements, regex=True)
#print(hit_type.head())

# 6. Add a new column
hits = hits.assign(hit_type=hit_type)
#print(hits.head())

# 7. Group by inning and hit_type
hits = hits.groupby(['inning', 'hit_type']).size().reset_index(name='count')
#print(hits.head(10))

# 8. Convert hit type to categorical
hits['hit_type'] = pd.Categorical(hits['hit_type'], ['single', 'double', 'triple', 'hr'])
#print(hits.info())

# 9. sort values
hits = hits.sort_values(['inning', 'hit_type'])
#print(hits.head(25))

# 10. reshape with pivot
hits = hits.pivot(index='inning', columns='hit_type', values='count')
print(hits.head(25))

# 11. stacked bar Plot
hits.plot.bar(stacked=True)
plt.show()
