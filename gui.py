from visualizationTools.charts import PairGridCorr_plot, distributions, waterfall_chart
from visualizationTools.Correlation import correlation_table
from visualizationTools.processAnalysis import ProcessCapability

from ProjectDataHandling.data_analysis.curve_fitting import PolynomialRegression
from ProjectDataHandling.project_management.timelines.make_schedule_from_excel import Gantt_Schedule

# dubious utility
from ProjectDataHandling.project_management.KPI_calc.Finance import Cost_ratios

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI App")
        
        # Create a tabbed layout
        self.tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Data Analysis")
        self.tab_control.add(self.tab2, text="Project Management")
        self.tab_control.add(self.tab3, text="KPI")
        self.tab_control.pack(expand=1, fill="both")
        
        # Data Analysis tab
        self.data_analysis_buttons()
        
        # Project Management tab
        self.project_management_buttons()
        
        # KPI tab
        self.kpi_buttons()
    
    def data_analysis_buttons(self):
        # Buttons for Data Analysis tab
        tk.Button(self.tab1, text="Pair Grid plot", command=self.PairGridCorr_plot).pack()
        tk.Button(self.tab1, text="Distribution", command=self.distributions).pack()
        tk.Button(self.tab1, text="Waterfall chart", command=self.waterfall_chart).pack()
        tk.Button(self.tab1, text="Polynomial Regression", command=self.PolynomialRegression).pack()
        tk.Button(self.tab1, text="Correlation table", command=self.correlation_table).pack()
        tk.Button(self.tab1, text="Process Capability", command=self.ProcessCapability).pack()
        
    def project_management_buttons(self):
        # Button for Project Management tab
        tk.Button(self.tab2, text="Cost Ratios", command=self.open_cost_ratios_popup).pack()
        
    def kpi_buttons(self):
        # Button for KPI tab
        tk.Button(self.tab3, text="Gantt Schedule", command=self.Gantt_Schedule).pack()
        
    # Functions for Data Analysis tab
    def PairGridCorr_plot(self):
        # Implement the functionality for Pair Grid plot
        pass
    
    def distributions(self):
        # Implement the functionality for Distribution
        pass
    
    def waterfall_chart(self):
        # Implement the functionality for Waterfall chart
        pass
    
    def PolynomialRegression(self):
        # Implement the functionality for Polynomial Regression
        pass
    
    def correlation_table(self):
        # Implement the functionality for Correlation table
        pass
    
    def ProcessCapability(self):
        # Implement the functionality for Process Capability
        pass
    
    # Functions for Project Management tab
    def open_cost_ratios_popup(self):
        local_cost = simpledialog.askfloat("Cost Ratios", "Enter Local Cost:")
        overseas_cost = simpledialog.askfloat("Cost Ratios", "Enter Overseas Cost:")
        local_logistics_cost = simpledialog.askfloat("Cost Ratios", "Enter Local Logistics Cost:")
        overseas_logistics_cost = simpledialog.askfloat("Cost Ratios", "Enter Overseas Logistics Cost:")
        
        if local_cost is not None and overseas_cost is not None and local_logistics_cost is not None and overseas_logistics_cost is not None:
            self.Cost_ratios(local_cost, overseas_cost, local_logistics_cost, overseas_logistics_cost)
    
    def Cost_ratios(self, local_cost, overseas_cost, local_logistics_cost, overseas_logistics_cost):
        # Implement the functionality for Cost Ratios
        pass
    
    # Functions for KPI tab
    def Gantt_Schedule(self):
        # Implement the functionality for Gantt Schedule
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()


''''

I want to create a GUI class using python. 
The GUI will call some functions that I have prepared.
The GUI will have the following tabs: Data Analysis; Project Management; KPI.

Data analysis tab will have these buttons: "Pair Grif plot", that calls "PairGridCorr_plot" function; "Distribution", that calls "distributions" function; 
"Waterfall chart", that calls "waterfall_chart" function; "Polynomial Regression" that calls "PolynomialRegression" function; 
"Correlation table" that calls "correlation_table" function; "Process Capability" that calls the "ProcessCapability" function.

Project Management tab will have these buttons: "Cost Ratios" that calls the "Cost_ratios" function.
"Cost Ratios" buttons will trigger a popup window where you can input: Local cost; Overseas cost; Local logistics cost; Overseas logistics cost. 
These will be inputs for the "Cost_ratios" function. "Cost Ratios" pop up window must have an OK and cancel button. 
When the user press OK "Cost_ratios" function will run.

KPI tab will have these buttons: "Gantt Schedule" that calls the "Gantt_Schedule" function

'''