
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#from IPython.display import display, HTML


def gantt_chart(schedule_folder, show=False):

    # check if a folder is provided
    if schedule_folder != '':
        DIR_EXCEL_SCHEDULE = schedule_folder
    else:
        DIR_EXCEL_SCHEDULE = input('Input folder where the schedule excel is: ')

    df = pd.read_excel(os.path.join(DIR_EXCEL_SCHEDULE, 'schedule_gantt.xlsx'))

    df.dropna(how='all', inplace=True) # Drop empty lines
    # Replace missing duration with 1 (one hour) an change column type to integer
    df['Duration'] = df['Duration'].fillna(1).astype(np.int32) 
    # Replace missing category name with Other
    df['Category'] = df['Category'].fillna('Other') 
    # Replace missing start time with min date
    df['Start'] = df['Start'].fillna(min(df['Start'])) 
    # Helper column with task end date
    df['End'] = df['Start'] + df['Duration'] * pd.Timedelta(days=1) 

    fig, ax = plt.subplots(figsize = (20, 20))
    ax.axis('off')

    # Today line
    today = pd.Timestamp.today()
    # Number of tasks + 4 * number of groups + margins
    today_line_length = len(df) + len(df['Category'].unique()) * 4 
    #+ 6 (can use this to have more space below)
    # Draw vertical line on today's mark
    ax.vlines(today.timestamp(), ymin=-3, ymax=today_line_length, color='red', lw=2, zorder=-1) 
    ax.text(today, -3, today.date(), fontweight='bold')
    ax.text(today, today_line_length + 1, today.date(), fontweight='bold')

    # Quarters bars 
    q = pd.date_range(min(df['Start']), freq='QS',
    periods=(max(df['End']) - min(df['Start'])).days//91+1,
    normalize=False) #, inclusive="left")
    for i, quarter in enumerate(q):
        if (i<len(q)-1) and (i % 2 == 1): 
            ax.fill_between(
            (q[i].timestamp(),q[i+1].timestamp()), -5, 
            today_line_length+2.5, facecolor='tab:cyan', alpha = 0.2
            )
        quarter_label = 'Q'+str(quarter.quarter)+'-'+str(quarter.year)
        # Display today's date on top
        ax.text(quarter + pd.DateOffset(days=45), -4, quarter_label, ha='center') 
        # Dsiplay today's date in bottom
        #ax.text(quarter + pd.DateOffset(days=45), today_line_length+2, quarter_label, ha='center') 

    # fill 1st quarter
    if min(df['Start']) < q[0]:
        ax.fill_between(
        (min(df['Start']).timestamp(),q[0].timestamp()), -5, 
        today_line_length+2.5, facecolor='tab:cyan', alpha = 0.2)

    # Montly line 
    q = pd.date_range(min(df['Start']), freq='M', periods=(max(df['End']) - min(df['Start'])).days//30+1)
    for i, month in enumerate(q):
        if (i<len(q)-1):# and (i % 2 == 1): 
            ax.vlines((q[i].timestamp(),q[i+1].timestamp()), -5, today_line_length+2.5)
        month_label = str(month.month)+'-'+str(month.year)
        ax.text(month + pd.DateOffset(days=-15), today_line_length+2, month_label, ha='center')

    ax.invert_yaxis() # y axis starts at top and ends in bottom
    group_start_y = -1 # Where to start plotting first group 

    # Main loop, for each group draw the group summary and all the tasks
    # Don't sort, by default i would be sorted alphabetically
    for group in df.groupby('Category', sort=False): 
        group_name = group[0] # Group name
        df_g = group[1] # Group dataframe
        # Count of group members + 1 row margin
        group_size_y = len(df_g) + 1 
        # Soonest date in the group
        group_start_x = min(df_g['Start']).date() 
        # Latest date in group (max start date + duration)
        group_end_x = max(df_g['End']).date() 
        
        
        # Display group name and summary  
        # Group name
        ax.text(group_start_x, group_start_y, group_name, size='large', fontweight='bold') 
        # Group start and end date
        group_duration_str = str(group_start_x) + ' to ' + str(group_end_x) 
        # Group duration
        ax.text(group_start_x, group_start_y+1, group_duration_str)
        # Completion percentage
        ax.text(group_start_x, group_start_y+2, 
        str(int(len(df_g[~df_g['Completed'].isnull()])/len(df_g) *100)) + '% completed') 
        group_start_y += 3 # Where to start with tasks
        ax.hlines(group_start_y + group_size_y - 0.5, 
            xmin=min(df['Start']).timestamp(), xmax=max(df['End']).timestamp(), 
            color='tab:grey', alpha=0.5)
        
        # Display each task
        for i, task_name in enumerate(df_g['Name']):
            task = df_g.iloc[i]
            
            # Get bar color
            task_color = 'tab:grey' # Planned
            if task['End'] < today: task_color = 'tab:red' # Overdue
            if task['Completed'] < today: task_color = 'tab:green'  # Completed     
            # Draw bar
            ax.broken_barh([(task['Start'].timestamp(),task['Duration'])],(group_start_y+i,1), color=task_color) 
            ax.text(task['Start']+task['Duration'] * pd.DateOffset(days=1) + pd.DateOffset(days=2),
                group_start_y+i+0.6,task_name, va='center', fontsize='x-large') # bar label - task name
        
        # One row space between group end and start of another group 
        group_start_y += group_size_y + 1 

    plt.savefig(
        os.path.join(DIR_EXCEL_SCHEDULE, 
        'schedule_' + DIR_EXCEL_SCHEDULE.split("\\")[-1] + '_gantt.png'), 
        format='png') # Save chart to PNG

    if show:
        plt.show()

def main():
    
    #from utils.String_manipulation import WinFolder_path_to_PY
    PATH = r'C:\Users\vieir\OneDrive\Documentos\00_TEST'
    #WinFolder_path_to_PY(r'C:\Users\vieir\OneDrive\Documentos\00_TEST')
    gantt_chart(PATH)

if __name__ == "__main__":
    main()


# later, to make this shit run
""" 
myscript.bat:

ECHO ON
REM A batch script to execute a Python script
SET PATH=%PATH%;C:\Python27
python yourscript.py
PAUSE
"""
