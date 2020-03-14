import pandas as pd
import matplotlib.pyplot as plt
from data import games

#print(games.head())

# 4. Select attendance
attendance = games.loc[(games['type']=='info') & (games['multi2']=='attendance'), ['year', 'multi3']].reset_index(drop=True)
#print(attendance.head(25))

# 5. Column labels
#attendance.rename(columns={'multi3':'attendance'}, inplace=True)
attendance.columns = ['year', 'attendance']
#print(attendance.info())

# 6. Convert to numeric
attendance.loc[:, 'attendance'] = pd.to_numeric(attendance.loc[:, 'attendance'])
#print(attendance.info())

# 7. Plot DataFrame
attendance.plot(x='year', y='attendance', figsize=(15, 7), kind='bar')
plt.xlabel('Year')
plt.ylabel('Attendance')
plt.axhline(y=attendance['attendance'].mean(), label='Mean', linestyle='--', color='green')
plt.show()
