
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class Gantt_Schedule:
    
    def __init__(self, TARGET_PATH, data):
        
        self.TARGET_PATH = TARGET_PATH
        if data is None:
            try:
                self.dir = os.path.join(TARGET_PATH, 'make_schedule_from_excel.xlsx')
                self.df = pd.read_excel(self.dir)
            except Exception as e:
                print('File make_schedule_from_excel.xlsx not found: {e}')
        else:
            self.df = data
            
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
    
    def plot(self, major_time_delta):
        
        from matplotlib.patches import Patch
        fig, self.ax = plt.subplots(1, figsize=(16,8))
        # bars
        self.ax.barh(self.df.Task, self.df.current_num, left=self.df.start_num, color=self.df.color)
        self.ax.barh(self.df.Task, self.df.days_start_to_end, left=self.df.start_num, color=self.df.color, alpha=0.5)
        # texts
        for idx, row in self.df.iterrows():
            # completion status
            self.ax.text(row.end_num+0.1, idx, 
                    f"{int(row.Completion*100)}%", 
                    va='center', alpha=0.8)
            # Task ID
            self.ax.text(row.start_num+0.1, idx,
                    f"{row.Task}", 
                    va='center', alpha=0.8,
                    backgroundcolor='white')
            
        ##### LEGENDS #####
        #c_dict = {'MKT':'#E64646', 'FIN':'#E69646', 'ENG':'#34D05C', 'PROD':'#34D0C3', 'IT':'#3475D0'}
        legend_elements = [Patch(facecolor=self.c_dict[i], label=i)  for i in self.c_dict]
        plt.legend(handles=legend_elements)
        ##### TICKS #####
        xticks = np.arange(0, self.df.end_num.max()+1, major_time_delta)
        xticks_labels = pd.date_range(self.proj_start, end=self.df.End.max()).strftime("%d/%m/%y")
        xticks_minor = np.arange(0, self.df.end_num.max()+1, major_time_delta)
        self.ax.set_xticks(xticks)
        self.ax.set_xticks(xticks_minor, minor=True)
        self.ax.set_xticklabels(xticks_labels[::major_time_delta])
        self.ax.tick_params(axis='x', rotation=90)
      
    def gridlines(self, period, major_time_delta):
                
        # grid lines
        self.ax.set_axisbelow(True)
        self.ax.xaxis.grid(color='gray', linestyle='dashed', alpha=0.2, which='both')

        # ticks top
        # create a new axis with the same y
        ax_top = self.ax.twiny()

        # align x axis
        self.ax.set_xlim(0, self.df.end_num.max())
        ax_top.set_xlim(0, self.df.end_num.max())

        # top ticks (markings)
        xticks_top_minor = np.arange(0, self.df.end_num.max()+1, major_time_delta)
        ax_top.set_xticks(xticks_top_minor, minor=True)
        # top ticks (label)
        xticks_top_major = np.arange(major_time_delta/2, self.df.end_num.max()+1, major_time_delta)
        ax_top.set_xticks(xticks_top_major, minor=False)
        # period labels
        xticks_top_labels = [f"{period} {i}" for i in np.arange(1, len(xticks_top_major)+1, 1)]
        ax_top.set_xticklabels(xticks_top_labels, ha='center', minor=False)
        
        # hide major tick (we only want the label)
        ax_top.tick_params(which='major', color='w')
        # increase minor ticks (to marks the periods start and end)
        ax_top.tick_params(which='minor', length=major_time_delta, color='k')

        # remove spines
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['left'].set_position(('outward', 10))
        self.ax.spines['top'].set_visible(False)

        ax_top.spines['right'].set_visible(False)
        ax_top.spines['left'].set_visible(False)
        ax_top.spines['top'].set_visible(False)
        
    def today_line(self):
        # Today line
        today_to_ref_dt = pd.Timestamp.today() - self.df['Start'][0]
        today_line_length = len(self.df)
        # Draw vertical line on today's mark
        self.ax.vlines(today_to_ref_dt.days, 
                       ymin=-1, ymax=today_line_length, 
                       color='red', lw=2, zorder=-1) 
        self.ax.text(today_to_ref_dt.days, -1, 
                     pd.Timestamp.today().date(), fontweight='bold')
        self.ax.text(today_to_ref_dt.days, today_line_length, 
                     pd.Timestamp.today().date(), fontweight='bold')
    
        
    def ouput(self, show=False):

        plt.savefig(
            os.path.join(self.TARGET_PATH, 
            'schedule_' + self.TARGET_PATH.split("\\")[-1] + '_gantt.png'), 
            format='png') # Save chart to PNG

        if show:
            plt.show(block=False)

def main():
    
    #from utils.String_manipulation import WinFolder_path_to_PY
    PATH = r'C:\Users\vieir\OneDrive\Documentos\00_TEST'
    #WinFolder_path_to_PY(r'C:\Users\vieir\OneDrive\Documentos\00_TEST')

    gantt = Gantt_Schedule(PATH)
    gantt.plot(7)
    gantt.gridlines('Month',30)
    gantt.today_line()
    gantt.ouput(show=True)

if __name__ == "__main__":
    main()
