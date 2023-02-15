
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet


def predict_cycles(df, X_pred, Model=LinearRegression()):
    # Create a 2D array of the cycle numbers
    X = [df.columns[0]]
    for i in range(1, len(df.columns)):
        X = np.vstack((X, df.columns[i]))

    #X = np.array([[0], [5], [10], [15], [20]])
    # Create a 2D array of the sample results
    y = df.to_numpy().T
    
    # Create and train a linear regression model
    model = Model
    model.fit(X, y)
    
    # Use the model to predict the results for cycles 25 and 30
    y_pred = model.predict(X_pred).T  # Transpose to swap rows and columns
    
    ### Plot the dispersion of the distribution
    font = {'size' : 22}
    matplotlib.rc('font', **font)

    fig, ax = plt.subplots()

    try:
        ax.boxplot(y.T, positions=X.reshape(-1),
                   patch_artist=True,
                   boxprops={"facecolor": "C0", "edgecolor": "white", "linewidth": 0.5})
    except:
        ax.scatter(X, y, marker='o', color='Black', s=50)


    ## plot predicted
    try:
        pos = np.tile(X_pred.T, (y.shape[1], 1))
        ax.boxplot(y_pred, positions=pos[0])
    except:
        ax.scatter(np.tile(X_pred.T, (y.shape[1], 1)), 
                   y_pred, marker='o', color='Black', s=50)
        
    ax.set_xlabel('Cycles')
    ax.set_ylabel('Sample Results')
    ax.set_title(f'Dispersion of Sample Results -- {type(model).__name__}')
    ax.set_xticks(X.reshape(-1).tolist() + X_pred.reshape(-1).tolist())
    ax.grid(True, axis='y')
    plt.show()
    
    return y_pred


if __name__ == '__main__':
    

    # create a sample DataFrame
    df = pd.DataFrame({
        0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        5: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
        10: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45],
        15: [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
        20: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    })

    X_pred = np.array([[25], [30]])

    models = [LinearRegression(), Lasso(), ElasticNet()]
    for model in models:
        y_pred = predict_cycles(df, X_pred, Model=model)



