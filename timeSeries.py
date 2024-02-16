import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_error

def create_dataframe(number_of_columns, number_of_rows, columns_name, rows_name=None, custom_function=None):
    # Create a dictionary to store data for each column
    data = {}
    for i, col in enumerate(columns_name):
        if custom_function:
            data[col] = np.random.rand(number_of_rows) + custom_function(i)
        else:
            data[col] = np.random.rand(number_of_rows)
    
    # Create a Pandas DataFrame
    df = pd.DataFrame(data, columns=columns_name)

    # Add row names if provided
    if rows_name:
        df.index = rows_name

    return df

# Example usage:
num_cols = 5
num_rows = 15
cols_names = ['INITIAL', '5', '10', '15', '20']
rows_names = ['Row1', 'Row2', 'Row3', 'Row4', 'Row5']

# Example custom function (you can replace this with your own function)
def custom_function(x):
    return -0.1*x**2 +14

# flatten loop
def easyFlatten(df, step=5):
    # step means how many to skip in enumerate i
    x = []
    y = []
    for i,ydata in enumerate(df):
        x += [i*step]*len(df[ydata])
        y.append(df[ydata].values)
    y = np.array(y).flatten()

    return [x, y]


''''CURVE FITTING'''

    
# Example usage:
num_cols = 5  # Including target variable
num_rows = 15
target_variable = 'Cycle25'
cols_names = ['Cycle0', 'Cycle5', 'Cycle10', 'Cycle15', 'Cycle20']
rows_names = [f'Timepoint{i}' for i in range(num_rows)]

# Generate data
np.random.seed(2)
df = create_dataframe(num_cols, num_rows, cols_names, None, custom_function)

#print(df)
#print(df.shape)


print('df describe:')
print(df.describe())
print()

from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_error

x_, y_ = easyFlatten(df, step=5)



# Sample data
x = np.array(x_)
y = np.array(y_)

# Performing quadratic fitting
coefficients = np.polyfit(x, y, 2)
a, b, c = coefficients

# Generating fitted curve
x_fit = np.linspace(min(x), max(x), 100)
y_fit = a * x_fit**2 + b * x_fit + c

y_pred_test = a * x**2 + b * x + c

def func(x, a, b, c):
    return a * x**2 + b * x + c

print(f'mean_absolute_percentage_error quadratic={mean_absolute_percentage_error(y, y_pred_test)}\n')
print(f'mean_squared_error quadratic={mean_squared_error(y, y_pred_test)}\n')

x_fit_pred = np.array([20, 25])
y_fit_pred = func(x_fit_pred, a, b, c)

labels = np.array([0, 5, 10, 15, 20])

z_value = 6 # 3 sigma
confidence_interval_pred = z_value * np.std(y_fit)
confidence_interval_samples = z_value * np.std(df).values

confidence_interval = np.array([*confidence_interval_samples, 
    confidence_interval_pred, 1.1*confidence_interval_pred])

lower_bound = func(np.array([*labels, *x_fit_pred[-2:]]), a, b, c) - confidence_interval
upper_bound = func(np.array([*labels, *x_fit_pred[-2:]]), a, b, c) + confidence_interval


# Plotting the original data and the fitted curve
#plt.scatter(x, y, label='Original Data')
plt.boxplot(df, positions=labels, labels=labels)

plt.plot(x_fit, y_fit, label='Quadratic Fit', color='red')
plt.plot(x_fit_pred, y_fit_pred, label='Quadratic Fit Prediction', color='blue')

plt.fill_between([*labels, *x_fit_pred[-2:]],
                 lower_bound, upper_bound, 
                 color='blue', alpha=0.1)

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.show()


plt.show()


