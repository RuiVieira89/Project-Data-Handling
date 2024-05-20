
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from datetime import datetime, timedelta
import random


def generate_random_dataframe(num_columns: int, length: int) -> pd.DataFrame:
    """
    Generates a Pandas DataFrame with random dates in the first column and random numbers in the remaining columns.

    Parameters:
    num_columns (int): Number of columns in the DataFrame.
    length (int): Number of rows in the DataFrame.

    Returns:
    pd.DataFrame: DataFrame with random dates and random numbers.
    """
    # Function to generate a random date between start_date and end_date
    def generate_random_date(start_date: str, end_date: str) -> datetime:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = end - start
        random_days = random.randint(0, delta.days)
        return start + timedelta(days=random_days)

    # Generate random dates for the first column
    random_dates = [generate_random_date('2017-01-01', '2024-12-31') for _ in range(length)]
    
    # Generate random numbers for the remaining columns
    random_data = np.random.rand(length, num_columns - 1)
    
    # Combine dates and random data
    data = np.column_stack((random_dates, random_data))
    
    # Create column names with 'Date' as the first column and 'Column_1', 'Column_2', ..., 'Column_n-1' for the others
    column_names = ['Date'] + [f'Column_{i+1}' for i in range(num_columns - 1)]
    
    # Create DataFrame using pandas
    df = pd.DataFrame(data, columns=column_names)
    
    # Ensure the 'Date' column is of datetime type and others are float
    df['Date'] = pd.to_datetime(df['Date'])
    for col in df.columns[1:]:
        df[col] = df[col].astype(float)
    
    return df



class Plot_subplots_time:

    def __init__(self):
        pass

    def plot_violin(self, data, plot_var, xx_time, upper_pounds, lower_bounds, period='M'):
        pass

    def plot_(self):
        pass



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class TimelineDataPlotter:
    def __init__(self, num_subplots=2):
        self.fig, self.axes = plt.subplots(num_subplots)
        self.num_subplots = num_subplots
        self.current_subplot = 0  # Keep track of the current subplot index

    def _get_subplot(self):
        # Get the current subplot and increment the index for the next plot
        ax = self.axes[self.current_subplot]
        self.current_subplot += 1
        return ax

    def plot_boxplot(self, data, plot_var, xx_time, upper_bounds, lower_bounds, period='M'):
        """
        Plots a box plot for the specified variable against time grouped by the given period.

        Parameters:
        - data: DataFrame containing the data
        - plot_var: The variable to be plotted on the y-axis
        - xx_time: The time variable to be plotted on the x-axis
        - upper_bounds: The upper bound for the y-axis
        - lower_bounds: The lower bound for the y-axis
        - period: The period for grouping the data (e.g., 'M' for month, 'Q' for quarter, etc.)
        """

        ax = self._get_subplot()

        # Convert the xx_time column to datetime if it's not already
        data[xx_time] = pd.to_datetime(data[xx_time])

        # Grouping the data by the specified period
        data['period'] = data[xx_time].dt.to_period(period)
        grouped = data.groupby('period')[plot_var]

        # Extracting the unique periods and corresponding data
        periods = list(grouped.groups.keys())
        data_to_plot = [grouped.get_group(period).dropna().values for period in periods if len(grouped.get_group(period).dropna().values) > 1]

        # Ensure there is data to plot
        if not data_to_plot:
            print("No data available for the specified period.")
            return

        # Creating the boxplot
        ax.boxplot(data_to_plot, patch_artist=True)

        # Adding the upper and lower bounds as horizontal lines
        upper_bound = float(data[upper_bounds].iloc[0])
        lower_bound = float(data[lower_bounds].iloc[0])
        ax.hlines(upper_bound, xmin=0.5, xmax=len(data_to_plot) + 0.5, color='blue', linestyle='--')
        ax.hlines(lower_bound, xmin=0.5, xmax=len(data_to_plot) + 0.5, color='blue', linestyle='--')

        # Setting the x-axis labels
        ax.set_xticks(np.arange(1, len(data_to_plot) + 1))
        ax.set_xticklabels([str(period) for period in periods if len(grouped.get_group(period).dropna().values) > 1], rotation=45)

        # Setting the labels and title
        ax.set_xlabel(xx_time)
        ax.set_ylabel(plot_var)
        ax.set_title(f'Boxplot of {plot_var} over {xx_time} grouped by {period}')

        # Setting y-axis limits
        y_range = upper_bound - lower_bound
        ax.set_ylim(lower_bound - 0.1 * y_range, upper_bound + 0.1 * y_range)

        # Displaying the plot
        plt.tight_layout()
        #plt.show()

    def plot_violin(self, data, plot_var, xx_time, upper_bounds, lower_bounds, period='M'):
        """
        Plots a violin plot for the specified variable against time grouped by the given period.

        Parameters:
        - data: DataFrame containing the data
        - plot_var: The variable to be plotted on the y-axis
        - xx_time: The time variable to be plotted on the x-axis
        - upper_bounds: The upper bound for the y-axis
        - lower_bounds: The lower bound for the y-axis
        - period: The period for grouping the data (e.g., 'M' for month, 'Q' for quarter, etc.)
        """

        ax = self._get_subplot()

        # Convert the xx_time column to datetime if it's not already
        data[xx_time] = pd.to_datetime(data[xx_time])

        # Grouping the data by the specified period
        data['period'] = data[xx_time].dt.to_period(period)
        grouped = data.groupby('period')[plot_var]

        # Extracting the unique periods and corresponding data
        periods = list(grouped.groups.keys())
        data_to_plot = [grouped.get_group(period).dropna().values for period in periods if len(grouped.get_group(period).dropna().values) > 1]

        # Ensure there is data to plot
        if not data_to_plot:
            print("No data available for the specified period.")
            return

        # Creating the violin plot
        parts = ax.violinplot(data_to_plot, showmeans=False, showmedians=True)

        # Adding the upper and lower bounds as horizontal lines
        upper_bound = float(data[upper_bounds].iloc[0])
        lower_bound = float(data[lower_bounds].iloc[0])
        ax.hlines(upper_bound, xmin=0.5, xmax=len(data_to_plot) + 0.5, color='blue', linestyle='--')
        ax.hlines(lower_bound, xmin=0.5, xmax=len(data_to_plot) + 0.5, color='blue', linestyle='--')

        # Setting the x-axis labels
        ax.set_xticks(np.arange(1, len(data_to_plot) + 1))
        ax.set_xticklabels([str(period) for period in periods if len(grouped.get_group(period).dropna().values) > 1], rotation=45)

        # Setting the labels and title
        ax.set_xlabel(xx_time)
        ax.set_ylabel(plot_var)
        ax.set_title(f'Violinplot of {plot_var} over {xx_time} grouped by {period}')

        # Setting y-axis limits
        y_range = upper_bound - lower_bound
        ax.set_ylim(lower_bound - 0.1 * y_range, upper_bound + 0.1 * y_range)

        # Displaying the plot

# Example usage:
data = generate_random_dataframe(4, 100)
plotter = TimelineDataPlotter(num_subplots=3)
plotter.plot_boxplot(data, data.columns[1], data.columns[0], data.columns[2], data.columns[3], period='M')
plotter.plot_violin(data, data.columns[1], data.columns[0], data.columns[2], data.columns[3], period='M')
plotter.plot_violin(data, data.columns[1], data.columns[0], data.columns[2], data.columns[3], period='M')

plt.show


def plot_boxplot(data, plot_var, xx_time, upper_bounds, lower_bounds, period='M'):
    """
    Plots a box plot for the specified variable against time grouped by the given period.

    Parameters:
    - data: DataFrame containing the data
    - plot_var: The variable to be plotted on the y-axis
    - xx_time: The time variable to be plotted on the x-axis
    - upper_bounds: The upper bound for the y-axis
    - lower_bounds: The lower bound for the y-axis
    - period: The period for grouping the data (e.g., 'M' for month, 'Q' for quarter, etc.)
    """

    # Convert the xx_time column to datetime if it's not already
    data[xx_time] = pd.to_datetime(data[xx_time])

    # Grouping the data by the specified period
    data['period'] = data[xx_time].dt.to_period(period)
    grouped = data.groupby('period')[plot_var]

    # Extracting the unique periods and corresponding data
    periods = list(grouped.groups.keys())
    data_to_plot = [grouped.get_group(period).dropna().values for period in periods if len(grouped.get_group(period).dropna().values) > 1]

    # Ensure there is data to plot
    if not data_to_plot:
        print("No data available for the specified period.")
        return

    # Creating the figure and axis
    fig, ax = plt.subplots()

    # Creating the boxplot
    ax.boxplot(data_to_plot, patch_artist=True)

    # Customizing the boxplot
    colors = ['#D43F3A'] * len(data_to_plot)
    for patch, color in zip(ax.artists, colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('black')
        patch.set_alpha(0.7)

    # Adding the upper and lower bounds as horizontal lines
    upper_bound = float(data[upper_bounds].iloc[0])
    lower_bound = float(data[lower_bounds].iloc[0])
    ax.hlines(upper_bound, xmin=0.5, xmax=len(data_to_plot) + 0.5, color='blue', linestyle='--')
    ax.hlines(lower_bound, xmin=0.5, xmax=len(data_to_plot) + 0.5, color='blue', linestyle='--')

    # Setting the x-axis labels
    ax.set_xticks(np.arange(1, len(data_to_plot) + 1))
    ax.set_xticklabels([str(period) for period in periods if len(grouped.get_group(period).dropna().values) > 1], rotation=45)

    # Setting the labels and title
    ax.set_xlabel(xx_time)
    ax.set_ylabel(plot_var)
    ax.set_title(f'Boxplot of {plot_var} over {xx_time} grouped by {period}')

    # Setting y-axis limits
    y_range = upper_bound - lower_bound
    ax.set_ylim(lower_bound - 0.1 * y_range, upper_bound + 0.1 * y_range)

    # Displaying the plot
    plt.tight_layout()
    plt.show()


# Example usage:
df = generate_random_dataframe(5, 1000)

df[df.columns[2]] = df[df.columns[2]] + 0.2
df[df.columns[3]] = df[df.columns[3]] - 0.2

plot_boxplot(df, df.columns[1], df.columns[0], df.columns[2], df.columns[3])

# Example usage:
# df = pd.DataFrame({
#     'time': pd.date_range(start='2020-01-01', periods=100, freq='D'),
#     'value': np.random.randn(100),
#     'upper': [2.5] * 100,
#     'lower': [-2.5] * 100
# })
# plot_boxplot(df, 'value', 'time', 'upper', 'lower', period='M')


'''VIOLIN TBC'''

def plot_violin(data, plot_var, xx_time, upper_bounds, lower_bounds, period='M'):
    """
    Plots a violin plot for the specified variable against time grouped by the given period.

    Parameters:
    - data: DataFrame containing the data
    - plot_var: The variable to be plotted on the y-axis
    - xx_time: The time variable to be plotted on the x-axis
    - upper_bounds: The upper bound for the y-axis
    - lower_bounds: The lower bound for the y-axis
    - period: The period for grouping the data (e.g., 'M' for month, 'Q' for quarter, etc.)
    """

    # Convert the xx_time column to datetime if it's not already
    data[xx_time] = pd.to_datetime(data[xx_time])

    # Grouping the data by the specified period
    data['period'] = data[xx_time].dt.to_period(period)
    grouped = data.groupby('period')[plot_var]

    # Extracting the unique periods and corresponding data
    periods = list(grouped.groups.keys())
    data_to_plot = [grouped.get_group(period).dropna().values for period in periods if len(grouped.get_group(period).dropna().values) > 1]

    # Ensure there is data to plot
    if not data_to_plot:
        print("No data available for the specified period.")
        return

    # Flatten the data and create group labels
    flat_data = np.concatenate(data_to_plot)
    group_labels = np.concatenate([[i + 1] * len(data) for i, data in enumerate(data_to_plot)])

    # Creating the figure and axis
    fig, ax = plt.subplots()

    # Creating the violin plot using NumPy arrays
    data_grouped = [flat_data[group_labels == i + 1] for i in range(len(data_to_plot))]
    parts = ax.violinplot(data_grouped, showmeans=False, showmedians=True)

    # Customizing the violin plot
    for pc in parts['bodies']:
        pc.set_facecolor('#D43F3A')
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)

    # Adding the upper and lower bounds as horizontal lines
    upper_bound = float(data[upper_bounds].iloc[0])
    lower_bound = float(data[lower_bounds].iloc[0])
    ax.hlines(upper_bound, xmin=0.5, xmax=len(data_to_plot) + 0.5, color='blue', linestyle='--')
    ax.hlines(lower_bound, xmin=0.5, xmax=len(data_to_plot) + 0.5, color='blue', linestyle='--')

    # Setting the x-axis labels
    ax.set_xticks(np.arange(1, len(data_to_plot) + 1))
    ax.set_xticklabels([str(period) for period in periods if len(grouped.get_group(period).dropna().values) > 1], rotation=45)

    # Setting the labels and title
    ax.set_xlabel(xx_time)
    ax.set_ylabel(plot_var)
    ax.set_title(f'Violin plot of {plot_var} over {xx_time} grouped by {period}')

    # Setting y-axis limits
    y_range = upper_bound - lower_bound
    ax.set_ylim(lower_bound - 0.1 * y_range, upper_bound + 0.1 * y_range)

    # Displaying the plot
    plt.tight_layout()
    plt.show()

# Example usage:
length = 1000
df_violin = pd.DataFrame({
    'time': pd.date_range(start='2020-01-01', periods=length, freq='D'),
    'value': np.random.randn(length),
    'upper': [2.5] * length,
    'lower': [-2.5] * length
})
plot_violin(df_violin, 'value', 'time', 'upper', 'lower', period='M')



# Example usage:
# df = generate_random_dataframe(5, 10)
# print(df)

# Example usage:
df = generate_random_dataframe(5, 1000)

df[df.columns[2]] = df[df.columns[2]] + 0.2
df[df.columns[3]] = df[df.columns[3]] - 0.2

plot_violin(df, df.columns[1], df.columns[0], df.columns[2], df.columns[3])


'''

The issue likely stems from the data types in the DataFrame generated 
by your generate_random_dataframe function. Specifically, the 'Date' 
column might be interpreted as numpy.datetime64 objects and the random 
data as floats, but the function combines them into an object array. 
This can cause problems when plotting.

To ensure that the DataFrame has the correct data types, we can make 
some adjustments to the function. Let's explicitly handle the data types, 
particularly ensuring the 'Date' column is of type datetime64 and the 
numeric columns are of type float.
'''