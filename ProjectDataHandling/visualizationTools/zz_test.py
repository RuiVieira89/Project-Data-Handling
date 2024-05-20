
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Correlation import correlation_table
from charts import distributions
from charts import PairGridCorr_plot as PairGridPlot


DATA_PATH = r"C:\dev\data\Airbnb_Prices_in_European_Cities"

# get files 
import os

data_all = pd.DataFrame([])
for filename in os.listdir(DATA_PATH):
    file_dir = os.path.join(DATA_PATH, filename)
    if os.path.isfile(file_dir):
        # do something with the file
        data = pd.read_csv(file_dir).drop(
            columns=['Unnamed: 0', 'room_shared', 'room_private'])
        data['city'] = filename.replace('.csv', '')
        data_all = pd.concat([data_all, data], ignore_index=True)

print(data_all.head())
print(data_all.info())
print(data_all.describe(include='all'))

data_analysis = data_all.drop(columns=[
        #'city', 
        'host_is_superhost', 
        'biz', 'multi', 'attr_index',
        'rest_index', 'bedrooms', 
        'lng', 'lat', 'person_capacity',
        'room_type', 'cleanliness_rating', 
        'guest_satisfaction_overall'])

data_analysis_filter = data_analysis[
    (data_analysis['city'] == 'barcelona_weekends') | 
    (data_analysis['city'] == 'barcelona_weekdays')]




import pandas as pd
from sklearn.datasets import load_iris

# Load iris dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
cond = df[df.columns[-2]]

df['F'] = df[df.columns[-2]] < 3.5
 

dist = distributions().plot_distribution(df)

plt.show()

# Generate some random data
np.random.seed(42)
data = pd.DataFrame(np.random.randn(100, 5), columns=['A', 'B', 'C', 'D', 'E'])
data['F'] = 'B'

cond = data.drop(columns=['F']).sum(axis=1)

data['F'] = cond > 0


