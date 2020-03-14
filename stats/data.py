import os
import glob
import pandas as pd

game_files = glob.glob(os.path.join(os.getcwd(), 'games', '*.EVE'))
game_files.sort()

# 6. Append Game Frames
game_frames = []
for game_file in game_files:
    game_frame = pd.read_csv(game_file, names=['type', 'multi2', 'multi3', 'multi4', 'multi5', 'multi6', 'event'])
    game_frames.append(game_frame)

# 7. Concatenate DataFrames
games = pd.concat(game_frames)
#print(games.head())

# 8. Clean values
#print(games.info())
games.loc[games['multi5']=='??', ['multi5']] = ''

#print(games.loc[games['multi5']=='??'].count()[0])

# 9. Extract identifiers
identifiers = games['multi2'].str.extract(r'(.LS(\d{4})\d{5})')
#print(identifiers.head(15))
#print()

# 10. Forward Fill identifiers
#print(games['multi2'].head(25))

identifiers = identifiers.fillna(method='ffill')
#print(identifiers)

# 11. Rename columns
identifiers.columns = ['game_id', 'year']
#print(identifiers.info())

# 12. Concatenate identifiers columns
games = pd.concat([games, identifiers], axis=1, sort=False)
#print(games.info())

# 13. Fill NaN values
games = games.fillna(' ')
#print(games.head(15))

# 14. Categorical event type
#print(set(games['type']))
#print(set(games['type']))
category_list = ['sub', 'start', 'data', 'id', 'play', 'com', 'info', 'version']

cat = pd.Categorical(games['type'], categories=category_list, ordered=False)
games['type'] = cat

#print(games.info())
#print(set(games['type']))

# 15. Print DataFrames
#print(games.head())
