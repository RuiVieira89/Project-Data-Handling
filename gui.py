import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

import numpy as np
import pandas as pd
import ydata_profiling 

import webbrowser
import xlwings as xw

import matplotlib.pyplot as plt
import seaborn as sns

from visualizationTools.charts import PairGridCorr_plot, distributions, waterfall_chart
from visualizationTools.Correlation import correlation_table
from visualizationTools.processAnalysis import ProcessCapability

from ProjectDataHandling.data_analysis.curve_fitting import PolynomialRegression
from ProjectDataHandling.project_management.timelines.make_schedule_from_excel import Gantt_Schedule

# dubious utility
from ProjectDataHandling.project_management.KPI_calc.Finance import Cost_ratios



class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI App")
        
        # Create a tabbed layout
        self.tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab5 = ttk.Frame(self.tab_control)  # Seaborn tab
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab4 = ttk.Frame(self.tab_control)


        self.tab_control.add(self.tab1, text="Data Analysis")
        self.tab_control.add(self.tab4, text="Data Visualization")
        self.tab_control.add(self.tab5, text="Seaborn (Visualization)")  # Seaborn tab
        self.tab_control.add(self.tab3, text="Project Management")
        self.tab_control.add(self.tab2, text="KPI")
        self.tab_control.pack(expand=1, fill="both")
        
        # Data Analysis tab
        self.data_analysis_buttons()

        # data visualization tab
        self.data_visualization_buttons()

        # Seaborn tab
        self.seaborn_visualization_buttons()
        
        # Project Management tab
        self.project_management_buttons()
        
        # KPI tab
        self.kpi_buttons()
    
    def data_analysis_buttons(self):
        # Buttons for Data Analysis tab
        tk.Button(self.tab1, text="Pair Grid plot", command=self.PairGridCorr_plot).pack()
        tk.Button(self.tab1, text="Polynomial Regression", command=self.PolynomialRegression).pack()
        tk.Button(self.tab1, text="Correlation table", command=self.correlation_table).pack()
        tk.Button(self.tab1, text="Process Capability", command=self.ProcessCapability).pack()
        tk.Button(self.tab1, text="EDA Exploratory Data Analysis", command=self.EDA).pack()

    def data_visualization_buttons(self):

        tk.Button(self.tab4, text="Distribution", command=self.distributions).pack()
        tk.Button(self.tab4, text="Waterfall chart", command=self.waterfall_chart).pack()

    # Functions for Seaborn tab
    def seaborn_visualization_buttons(self):
        # Buttons for Seaborn tab
        tk.Button(self.tab5, text="Pairplot", command=self.seaborn_pairplot).pack()
        tk.Button(self.tab5, text="Histogram", command=self.seaborn_histogram).pack()
        tk.Button(self.tab5, text="Boxplot", command=self.seaborn_boxplot).pack()
        tk.Button(self.tab5, text="Heatmap", command=self.seaborn_heatmap).pack()
        tk.Button(self.tab5, text="Scatterplot", command=self.seaborn_scatterplot).pack()
        tk.Button(self.tab5, text="Lineplot", command=self.seaborn_lineplot).pack()
        tk.Button(self.tab5, text="Barplot", command=self.seaborn_barplot).pack()
        tk.Button(self.tab5, text="Violinplot", command=self.seaborn_violinplot).pack()
        tk.Button(self.tab5, text="Swarmplot", command=self.seaborn_swarmplot).pack()
        tk.Button(self.tab5, text="Jointplot", command=self.seaborn_jointplot).pack()
        tk.Button(self.tab5, text="PairGrid", command=self.seaborn_pairgrid).pack()
        tk.Button(self.tab5, text="FacetGrid", command=self.seaborn_facetgrid).pack()
        tk.Button(self.tab5, text="Countplot", command=self.seaborn_countplot).pack()
        # Add more Seaborn visualizations as needed


    def project_management_buttons(self):
        # Button for Project Management tab
        tk.Button(self.tab3, text="Gantt Schedule", command=self.Gantt_Schedule).pack()

    def kpi_buttons(self):
        # Button for KPI tab
        tk.Button(self.tab2, text="Cost Ratios", command=self.open_cost_ratios_popup).pack()

    # Functions for Data Analysis tab
    def PairGridCorr_plot(self):
        # Implement the functionality for Pair Grid plot
        df = xw.load(index=False)
        pair = PairGridCorr_plot(df).plot()
        plt.show()
    
    def distributions(self):
        # Implement the functionality for Distribution
        data = xw.load(index=False)
        dist = distributions().plot_distribution(data)
    
    def waterfall_chart(self):
        # Implement the functionality for Waterfall chart
        wf = waterfall_chart(run=True)
    
    def PolynomialRegression(self):
        data = xw.load(index=False)
        # Implement the functionality for Polynomial Regression
        measured_cycle_time = np.asarray(data.columns)
        measured_data = data.values

        input_str = simpledialog.askstring("Enter Array", "Enter a comma-separated list of values to predict:")
        
        try:
            # Split the input string into individual values and convert them to floats
            array = [float(value.strip()) for value in input_str.split(",")]
        except ValueError:
            array = None
            print("Invalid input. Please enter a valid comma-separated list of numeric values.")
            #return None

        degree = simpledialog.askfloat("Poly degree", "Enter Poly degree (ex:. 2):")
        
        prediction_cycle_time = np.asarray(array)

        poly_regression = PolynomialRegression(degree=int(degree))
        poly_regression.fit(measured_cycle_time, measured_data, prediction_cycle_time)
        poly_regression.plot_results(measured_cycle_time, measured_data)
        poly_regression.stat_info()
        plt.show()


    def correlation_table(self):
        # Implement the functionality for Correlation table
        data = xw.load(index=False)
        correlation_table(data)
        plt.show()
    
    def ProcessCapability(self):
        # Implement the functionality for Process Capability
        data = xw.load(index=False)

        spec_lower = simpledialog.askfloat("Limits", "LOWER sepecification:")
        spec_upper = simpledialog.askfloat("Limits", "UPPER specification:")

        pc = ProcessCapability(data, spec_upper, spec_lower)

        plt.show()

    ''' === SEABORN STUFF === '''
    def seaborn_pairplot(self):
        # Generate a sample pairplot (replace with your data)
        data = xw.load(index=False)
        sns.pairplot(data)
        plt.show()
    
    def seaborn_histogram(self):
        # Generate a sample histogram (replace with your data)
        data = xw.load(index=False)
        sns.histplot(data)
        plt.show()

    
    def seaborn_boxplot(self):
        # Generate a sample boxplot (replace with your data)
        data = xw.load(index=False)
        sns.boxplot(data=data)
        plt.show()

    def seaborn_heatmap(self):
        # Generate a sample heatmap (replace with your data)
        data = xw.load(index=False)
        sns.heatmap(data, annot=True)
        plt.show()
    
    def seaborn_scatterplot(self):
        # Generate a sample scatterplot (replace with your data)
        data = xw.load(index=False)
        sns.scatterplot(data=data)
        plt.show()
    
    def seaborn_lineplot(self):
        # Generate a sample lineplot (replace with your data)
        data = xw.load(index=False)
        sns.lineplot(data=data)
        plt.show()

    def seaborn_barplot(self):
        # Generate a sample barplot (replace with your data)
        data = xw.load(index=False)
        sns.barplot(data=data)
        plt.show()

    def seaborn_violinplot(self):
        # Generate a sample violinplot (replace with your data)
        data = xw.load(index=False)
        sns.violinplot(data=data)
        plt.show()

    def seaborn_swarmplot(self):
        # Generate a sample swarmplot (replace with your data)
        data = xw.load(index=False)
        sns.swarmplot(data=data)
        plt.show()

    def seaborn_jointplot(self):
        # Generate a sample jointplot (replace with your data)
        data = xw.load(index=False)
        sns.jointplot(data=data)
        plt.show()

    def seaborn_pairgrid(self):
        # Generate a sample pairgrid (replace with your data)
        data = xw.load(index=False)
        g = sns.PairGrid(data)
        g.map_diag(sns.histplot)
        g.map_offdiag(sns.scatterplot)
        plt.show()

    def seaborn_facetgrid(self):
        # Generate a sample facetgrid (replace with your data)
        data = xw.load(index=False)
        g = sns.FacetGrid(data)
        g.map(sns.scatterplot)
        plt.show()

    def seaborn_countplot(self):
        # Generate a sample countplot (replace with your data)
        data = xw.load(index=False)
        sns.countplot(data=data)
        plt.show()
        
    ''' === SEABORN STUFF END === '''

    def EDA(self):
        df = xw.load(index=False)
        # Generate the ProfileReport
        profile = ydata_profiling.ProfileReport(df)
        # Save the report as an HTML file
        output_file = "profile_report.html"
        profile.to_file(output_file)
        # Open the report in the default web browser
        webbrowser.open(output_file)
    
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
        cost = Cost_ratios()
        cost.CIM(local_cost, overseas_cost)
        cost.CIL(local_cost, overseas_cost, overseas_logistics_cost, local_logistics_cost)
    
    # Functions for KPI tab
    def Gantt_Schedule(self):
        # Implement the functionality for Gantt Schedule
        gant = Gantt_Schedule().get_gantt_chart()

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