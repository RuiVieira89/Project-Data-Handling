
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def predict_cycles(df):
    # Create a 2D array of the cycle numbers
    X = np.array([[0], [5], [10], [15], [20]])
    # Create a 2D array of the sample results
    y = df.to_numpy().T
    
    # Create and train a linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Use the model to predict the results for cycles 25 and 30
    X_pred = np.array([[25], [30]])
    y_pred = model.predict(X_pred).T  # Transpose to swap rows and columns
    
    # Plot the dispersion of the distribution
    fig, ax = plt.subplots()
    ax.boxplot(y.T, positions=X.reshape(-1))
    # [[X_pred[0][0], X_pred[1][0]]]
    # np.tile(a, (15, 1))
    ax.scatter(np.tile([X_pred[0][0], X_pred[1][0]], (15, 1)), 
    y_pred, marker='o', color='Black', s=50)
    ax.set_xlabel('Cycles')
    ax.set_ylabel('Sample Results')
    ax.set_title('Dispersion of Sample Results')
    ax.set_xticks(X.reshape(-1).tolist() + X_pred.reshape(-1).tolist())
    ax.grid(True, axis='y')
    plt.show()
    
    return y_pred


# create a sample DataFrame
df = pd.DataFrame({
    0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    5: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
    10: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45],
    15: [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
    20: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
})

print(df)
print()

# call the predict_and_plot_cycles function
y_pred = predict_cycles(df)

print(y_pred)