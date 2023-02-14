import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import numpy as np
import pandas as pd

# Set the number of samples and cycles
n_samples = 15
n_cycles = 20

# Generate random data for the available cycles
cycles = np.arange(0, n_cycles+1, 5)
results = np.random.normal(0, 1, size=len(cycles))

# Interpolate the results for all cycles
all_cycles = np.arange(0, n_cycles+1)
all_results = np.interp(all_cycles, cycles, results)

# Select the samples randomly
samples = np.random.choice(np.arange(n_cycles+1), size=n_samples, replace=False)

# Extract the data for the selected samples
data = pd.DataFrame({'sample': np.arange(1, n_samples+1),
                     'cycles': samples,
                     'results': all_results[samples]})



# Split the data into input and output variables
X = data['cycles'].values.reshape(-1, 1)
y = data['results'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Instantiate and fit a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the results for new cycles
X_new = [[25], [30]]
y_new = model.predict(X_new)

# Convert the input variable to a NumPy array
X_new = np.array(X_new)

# Predict the results for new cycles
y_new = model.predict(X_new)

# Evaluate the accuracy of the model
score = model.score(X_test, y_test)
mse = mean_squared_error(y_test, model.predict(X_test))

# Visualize the data and predictions
import matplotlib.pyplot as plt
import seaborn as sns

sns.scatterplot(x='cycles', y='results', data=data)
sns.lineplot(x=X_new.flatten(), y=y_new, color='red')
plt.show()
    