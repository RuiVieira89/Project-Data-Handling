
import unittest
import matplotlib.pyplot as plt
import pandas as pd

from ProjectDataHandling.data_analysis.charts import waterfall_chart

class TestWaterfallChart(unittest.TestCase):
    def test_df_not_empty(self):
        df = pd.DataFrame({
            'data1': [1, 2, 3, 4, 5],
            'data2': ['abs', 'rel', 'rel', 'total', 'abs'],
            'data3': [10, 20, -10, 100, 30]
        })
        title = 'Test chart with non-empty dataframe'
        waterfall_chart(df, title)
        # check if a chart was plotted
        self.assertTrue(len(plt.get_fignums()) > 0)
        # clean up the chart
        plt.close()

    def test_df_empty(self):
        df = []
        title = 'Test chart with empty dataframe'
        waterfall_chart(df, title)
        # check if a chart was plotted
        self.assertTrue(len(plt.get_fignums()) > 0)
        # clean up the chart
        plt.close()

if __name__ == '__main__':
    unittest.main()
