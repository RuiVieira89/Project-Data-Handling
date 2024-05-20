import numpy as np
import pandas as pd


def generate_random_data(lower_lim=1, upper_lim=20, size=(15, 5)):
    data = np.random.normal(size=size)
    columns = np.random.randint(lower_lim, upper_lim, size=size[1])
    df = pd.DataFrame(data, columns=columns)
    return df

