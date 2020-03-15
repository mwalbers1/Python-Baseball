import pandas as pd
import matplotlib.pyplot as plt
from data import games

# "How have the number of strike outs changed over time?"

# 1. Select all plays
plays = games[games['type']=='play']
#print(plays.head())

# 2. Select all strike outs
strike_outs = plays[plays['event'].str.contains('K')]
#print(strike_outs.head())

# 3. Group by Year and Game
strike_outs = strike_outs.groupby(['year', 'game_id']).size()
#print(strike_outs.head())

# 4. Reset index
strike_outs = strike_outs.reset_index(name='strike_outs')
#print(strike_outs.head())

# 5. Apply an operation to multiple columns
strike_outs = strike_outs.loc[:, ['year', 'strike_outs']].apply(pd.to_numeric)
#print(strike_outs.head())

# 6. Change plot formatting
strike_outs.plot(x='year', y='strike_outs', kind='scatter').legend(['Strike Outs'])
plt.xlabel('Year')
plt.ylabel('Strike Outs')
plt.show()
