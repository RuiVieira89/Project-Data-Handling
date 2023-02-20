
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import PolynomialFeatures

class DataFit:
    # Fits and plots data
    # model is specified in predict 
    def __init__(self, df, X_pred, Model=LinearRegression(), run=False):

        self.model = Model
        self.df =df
        self.X_pred = X_pred

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
        
        # Create and train a linear regression model
        self.model.fit(self.X, self.y)
        
        # Use the model to predict the results for cycles 
        self.y_pred = self.model.predict(self.X_pred).T  # Transpose to swap rows and columns


    def plot(self):
        ### Plot the dispersion of the distribution
        font = {'size' : 22}
        matplotlib.rc('font', **font)

        try:
            self.ax.boxplot(self.y.T, positions=self.X.reshape(-1),
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


if __name__ == '__main__':


    def generate_random_data(lower_lim=0, upper_lim=20, size=(15, 5)):
        data = np.random.normal(size=size)
        columns = np.random.randint(lower_lim, upper_lim, size=size[1])
        df = pd.DataFrame(data, columns=columns)
        return df

    # create a sample DataFrame
    df = pd.DataFrame({
        0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        5: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
        10: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45],
        15: [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
        20: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    })

    X_pred = np.array([[40], [50], [60]])

    data = generate_random_data(0, 30, (20,7))

    #fit = DataFit(data, X_pred, run=True)


    models = [PolynomialFeatures(2), Lasso(), ElasticNet()]
    for model in models:
        try:
            y_pred = DataFit(data, X_pred, Model=model, run=True)
        except Exception as e:
            print(f'Error in {type(model).__name__}: {e}')



