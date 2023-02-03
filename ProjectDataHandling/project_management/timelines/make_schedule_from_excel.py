
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

class Gantt_Schedule:
    
    def __init__(self, TARGET_PATH):
        
        self.TARGET_PATH = TARGET_PATH
        self.dir = os.path.join(TARGET_PATH, 'make_schedule_from_excel.xlsx')
        self.df = pd.read_excel(self.dir)
        self.c_dict = {} # color Dict
        
        # project start date
        self.proj_start = self.df.Start.min()
        # number of days from project start to task start
        self.df['start_num'] = (self.df.Start-self.proj_start).dt.days
        # number of days from project start to end of tasks
        self.df['end_num'] = (self.df.End-self.proj_start).dt.days
        # days between start and end of each task
        self.df['days_start_to_end'] = self.df.end_num - self.df.start_num
        
        
        # create a column with the color for each department
        self.df['color'] = self.df.apply(self.color, axis=1)
            
        # days between start and current progression of each task
        self.df['current_num'] = (self.df.days_start_to_end * self.df.Completion)
        
    def color(self, row):
        
        def rgb2hex(r,g,b):
            # Black is [0,0,0], and 
            # White is [255, 255, 255]; 
            # Gray is any [x,x,x]
            return "#{:02x}{:02x}{:02x}".format(r,g,b)

        def hex2rgb(hexcode):
            return tuple(map(ord,hexcode[1:].decode('hex')))
        
        if self.c_dict == {}:
            cmap = plt.cm.jet  # define the colormap
            n_elements = len(self.df['Department'].unique())
            for index, element in enumerate(self.df['Department'].unique()):
                bin_color = cmap(int( (cmap.N*(index+1))/(n_elements) ))[1:4]
                self.c_dict[element] = rgb2hex(
                    int(bin_color[0]*255), 
                    int(bin_color[1]*255), 
                    int(bin_color[2]*255))

                
        return self.c_dict[row['Department']]
    
    def plot(self):
        
        from matplotlib.patches import Patch
        fig, self.ax = plt.subplots(1, figsize=(16,8))
        # bars
        self.ax.barh(self.df.Task, self.df.current_num, left=self.df.Start, color=self.df.color)
        self.ax.barh(self.df.Task, self.df.days_start_to_end, left=self.df.Start, color=self.df.color, 
                     alpha=0.5)
        
        # texts
        for idx, row in self.df.iterrows():
            # completion status
            self.ax.text(mdates.date2num(row.End)+0.1, idx, 
                    f"{int(row.Completion*100)}%", 
                    va='center', alpha=0.8)
            # Task ID
            self.ax.text(mdates.date2num(row.Start)+0.1, idx,
                    f"{row.Task}", 
                    va='center', alpha=0.8,
                    backgroundcolor='white')
              
        ##### LEGENDS #####
        #c_dict = {'MKT':'#E64646', 'FIN':'#E69646', 'ENG':'#34D05C', 'PROD':'#34D0C3', 'IT':'#3475D0'}
        legend_elements = [Patch(facecolor=self.c_dict[i], label=i)  for i in self.c_dict]
        plt.legend(handles=legend_elements)

      
    def gridlines(self, period='Month'):
        
        # Set the x-axis to display major and minor time steps
        if period == 'Month':
            self.ax.xaxis.set_major_locator(mdates.MonthLocator())
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            self.ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        elif period == 'Year':
            self.ax.xaxis.set_major_locator(mdates.YearLocator())
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            self.ax.xaxis.set_minor_locator(mdates.MonthLocator()) #byweekday=mdates.MO))
        elif period == 'Day':
            self.ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))
            self.ax.xaxis.set_minor_locator(mdates.DayLocator()) #byweekday=mdates.MO))
        
        
        self.ax.grid(which='major', axis='x', linestyle='-', color='black', linewidth=1)
        self.ax.grid(which='minor', axis='x', linestyle='--', color='grey', linewidth=0.5)
        self.ax.xaxis.set_tick_params(rotation=90, labelsize=20)
        self.ax.autoscale()
        self.ax.set_xlim(left=self.df.Start.iloc[0], right=self.df.End.iloc[-1])
        
        plt.tight_layout()

        
    def today_line(self):
        # Today line
        today_line_length = len(self.df)
        # Draw vertical line on today's mark
        self.ax.vlines(pd.Timestamp.today(), 
                       ymin=-1, ymax=today_line_length, 
                       color='red', lw=2, zorder=-1) 
        self.ax.text(pd.Timestamp.today(), -1, 
                     pd.Timestamp.today().date(), fontweight='bold')
        self.ax.text(pd.Timestamp.today(), today_line_length, 
                     pd.Timestamp.today().date(), fontweight='bold')
    
        
    def ouput(self, show=False):

        plt.savefig(
            os.path.join(self.TARGET_PATH, 
            'schedule_' + self.TARGET_PATH.split("\\")[-1] + '_gantt.png'), 
            format='png') # Save chart to PNG

        if show:
            plt.show()
