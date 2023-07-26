
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score


class PolynomialRegression:
    def __init__(self, degree=2):
        self.degree = degree
        self.poly_features = PolynomialFeatures(degree=self.degree)
        self.regression_models = []
        self.mean_squared_errors = []
        self.r_squared_values = []
        self.predictions = []
        self.coefs = []
        self.prediction_cycle_time = None
    
    def fit(self, measured_cycle_time, measured_data):
        np.random.seed(42)
        self.prediction_cycle_time = np.random.uniform(21, 30, size=5)

        X_poly = self.poly_features.fit_transform(
            measured_cycle_time.reshape(len(measured_cycle_time), -1))
        X_predict = self.prediction_cycle_time.reshape(
            len(self.prediction_cycle_time), -1)
        
        for i in range(measured_data.shape[0]):
            y = measured_data[i]
            
            model = LinearRegression()
            model.fit(X_poly, y)
            
            self.coefs.append(model.coef_)
            y_mse = model.predict(X_poly)
            self.predictions.append(
                model.predict(self.poly_features.fit_transform(X_predict)))
            
            mse = mean_squared_error(y, y_mse)
            self.mean_squared_errors.append(mse)
            
            r_squared = r2_score(y, y_mse, multioutput='variance_weighted')
            self.r_squared_values.append(r_squared)
            
            self.regression_models.append(model)

    def plot_results(self, measured_cycle_time, measured_data):
        plt.rcParams.update({'font.size': 20})

        plt.boxplot(measured_data, positions=measured_cycle_time,
                    showfliers=False, patch_artist=True,
                    boxprops=dict(facecolor='skyblue'))

        predictions_plot = np.asarray(self.predictions)

        for i, pred_data in enumerate(predictions_plot):
            confidence_interval = 1.96 * np.std(pred_data)
            lower_bound = pred_data - confidence_interval
            upper_bound = pred_data + confidence_interval
            plt.fill_between(self.poly_features.transform(
                self.prediction_cycle_time.reshape(-1, 1))[:, 1], 
                lower_bound, upper_bound, color='green', alpha=0.1)

        plt.boxplot(predictions_plot, 
                    positions=self.poly_features.transform(
            self.prediction_cycle_time.reshape(-1, 1))[:, 1])


        def format_x_ticks(x, pos):
            return f"{x:.1f}"

        plt.gca().xaxis.set_major_formatter(FuncFormatter(format_x_ticks))
        plt.ylim(bottom=0)

    def stat_info(self):

        for i in range(len(self.regression_models)):
            print(f"Curve {i+1} Fitting Equation: {self.coefs[i]}")
            print(f"Curve {i+1} Mean Squared Error: {self.mean_squared_errors[i]:.2f}")
            print(f"Curve {i+1} R squared: {self.r_squared_values[i]:.2f}")

            print()




class DataFit:
    # Fits and plots data
    # model is specified in predict 
    def __init__(self, df, X_pred, Model=LinearRegression(), poly=[False, 2], run=False):
        # poly=[False, 2] is poly fit? , 2 is exp degree ax**2 + bx + c 

        self.model = Model
        self.df =df
        self.X_pred = X_pred
        self.poly = poly

        fig, self.ax = plt.subplots()

        if run:
            self.quick_run()
    
    def predict(self):
        self.X = [self.df.columns[0]]
        for i in range(1, len(self.df.columns)):
            self.X = np.vstack((self.X, self.df.columns[i]))

        #X = np.array([[0], [5], [10], [15], [20]])
        # Create a 2D array of the sample results
        self.y = self.df.to_numpy().T
        
        if self.poly[0]:
            # Create polynomial features
            poly_features = PolynomialFeatures(degree=self.poly[1])
            self.X = poly_features.fit_transform(self.X)
            self.X_pred = poly_features.fit_transform(self.X_pred)

        # Create and train a linear regression model
        self.model.fit(self.X, self.y)
        
        # Use the model to predict the results for cycles 
        self.y_pred = self.model.predict(self.X_pred).T  # Transpose to swap rows and columns


    def plot(self):
        ### Plot the dispersion of the distribution
        font = {'size' : 22}
        matplotlib.rc('font', **font)

        self.X = np.array(self.df.columns)

        try:
            self.ax.boxplot(self.y, positions=self.X.reshape(-1),
                    patch_artist=True,
                    boxprops={"facecolor": "C0", "edgecolor": "white", "linewidth": 0.5})
        except:
            self.ax.scatter(self.X, self.y, marker='o', color='Black', s=50)


        ## plot predicted
        try:
            #pos = np.tile(X_pred.T, (y.shape[1], 1))
            self.ax.boxplot(self.y_pred, positions=self.X_pred.T[0])
        except:
            self.ax.scatter(np.tile(self.X_pred.T, (self.y.shape[1], 1)), 
                    self.y_pred, marker='o', color='Black', s=50)
            
        self.ax.set_xlabel('Cycles')
        self.ax.set_ylabel('Sample Results')
        self.ax.set_title(f'Dispersion of Sample Results -- {type(self.model).__name__}')
        self.ax.set_xticks(self.X.reshape(-1).tolist() + self.X_pred.reshape(-1).tolist())
        self.ax.grid(True, axis='y')

    def plot_trend_lines(self):

        x = np.arange(min(self.X) - 1,max(self.X_pred) + 1)
        for i in range(len(x)):
            prediction = self.model.predict([[i]])[0]
            for j in range(len(prediction)):
                self.ax.scatter(np.array([[x[i]]]), prediction[j],
                        marker='o', color='Red', s=1)
    
    def quick_run(self):

        try:
            self.predict()
            self.plot()
            self.plot_trend_lines()
            plt.show()
        except Exception as e:
            print(f'Error in {type(self.model).__name__}: {e}')


class ExponentialPolyfit():

    def __init__(self):
        self.a = None
        self.b = None

    def fit(self, x, y):

        p = np.zeros([len(y[0,:]), 2])

        for i in range(len(y[0,:])):
            p[i] = np.polyfit(x.flatten(), np.log(y[:,i]), 1)
        
        self.a = np.exp(p[:,0])
        self.b = p[:,0]

    def predict(self, X_pred):

        return self.a * np.exp(self.b * X_pred)


if __name__ == "__main__":

    np.random.seed(42)

    measured_cycle_time = np.random.uniform(0, 20, size=20)
    measured_data = np.random.uniform(14, 18, size=(15, 20))

    poly_regression = PolynomialRegression(degree=2)
    poly_regression.fit(measured_cycle_time, measured_data)
    poly_regression.plot_results(measured_cycle_time, measured_data)
    poly_regression.stat_info()


'''
Prompt for the curve fitting 

Please create a Python class that will fit data and make a visualization. 
The class will have data as input the first step is to convert the input data into the correct data type in the init method.
The method must be able to allow polynomial, exponential, logarithmic 

###########################################################

Hello! 
I want to create a python class for time-series Forecasting.
The idea is to create a class that is as re-usable as possible with several parameters and functions that can:
- receive and convert data to be used in methods
The class should be able to use 1D (only one series present), 2D (several series of the same variable), and 3D (several series of several variables) data.
In the case of 3D data it must forecast and plot for each variable.

- use that data for predictions
The forecast must include statistical indicators such as p-values, confidence interval, correlation coefficient and any other that might be useful.
The parameters of the statistical indicators must be tunable.
The forecast must include statistical indicators such as p-values, confidence interval, correlation coefficient and any other that might be useful.
The parameters of the statistical indicators must be tunable.

- plot the data and predictions
For 1D data simply show the scatter plot of the input data and predictions 
The statistical indicators must be displayed on the plot.
The labels on the data must be used on the plot to label the axis.

It must be possible to use only certain methods of the class as required.



To understand how the class might be used consider this case:
A material test was performed: rubber degradation in acid using n samples.
The tensile strength was measured in some time points during the test.
We have data for n samples during t cycles.
Using this information I want to predict the material tensile strength if the test was done for longer (t + 1, t + 2, ...).

The idea is that the class should be able to forecast and plot this case.
But should be able to handle the case where n=1, that is, one sample.
And also handle a case with several experiments with several samples (3D data structure).

###########################################################

A material test was performed: rubber degradation in acid using n samples.
The tensile strength was measured in some time points during the test.
We have data for n samples during t cycles.
Using this information I want to predict the material tensile strength if the test was done for longer (t + 1, t + 2, ...).
I want to forecast and plot predictions.


'''