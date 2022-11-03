## TODO
# get labels automaticaly
# auto color owners
# cleanup the display

# Schedule():
#   color(pick_arg)
#   plot

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

df = pd.read_excel('schedule.xlsx')


# project start date
proj_start = df.Start.min()
# number of days from project start to task start
df['Start'] = (df.Start-proj_start).dt.days
# number of days from project start to end of tasks
df['Completed'] = (df.Completed-proj_start).dt.days
# days between start and end of each task
df['days_start_to_end'] = df.Completed - df.Start


# create a column with the color for each department
def color(row):
    c_dict = {'Plant':'#E64646', 'TME':'#E69646'}
    return c_dict[row['Category']]
df['color'] = df.apply(color, axis=1)


# days between start and current progression of each task
df['current_num'] = (df.days_start_to_end * df.Completion)
df = df.fillna(1)

fig, ax = plt.subplots(1, figsize=(16,6))
# bars
ax.barh(df.Name, df.current_num, left=df.Start, color=df.color)
ax.barh(df.Name, df.days_start_to_end, left=df.Start, color=df.color, alpha=0.5)
# texts
for idx, row in df.iterrows():
    ax.text(row.Completed+0.1, idx, 
            f"{int(row.Completion*100)}%", 
            va='center', alpha=0.8)
##### LEGENDS #####
c_dict = {'Plant':'#E64646', 'TME':'#E69646'}
legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
plt.legend(handles=legend_elements)
##### TICKS #####
xticks = np.arange(0, df.Completed.max()+1, 3)
xticks_labels = pd.date_range(proj_start, end=df.Completed.max()).strftime("%m/%d")
xticks_minor = np.arange(0, df.Completed.max()+1, 1)
ax.set_xticks(xticks)
ax.set_xticks(xticks_minor, minor=True)
ax.set_xticklabels(xticks_labels[::3])
plt.show()
