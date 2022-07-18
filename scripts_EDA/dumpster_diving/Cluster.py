
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import OPTICS
import numpy as np


class Cluster:

    def __init__(self, X):

        self.X = X

    def show_clusters(self):
        # Black removed and is used for noise instead.

        fig = plt.figure()

        ax = Axes3D(fig)

        unique_labels = set(self.labels)
        colors = [plt.cm.Spectral(each) for each in np.linspace(
            0, 1, len(unique_labels)
            )]

        marker_size = 60
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]
                marker_size = 6

            if self.X.size != 0:
                i = np.where(self.labels == k)
                ax.scatter(self.X[i, 0], self.X[i, 1], self.X[i, 2],
                           s=marker_size, c=tuple(col),
                           marker="o", cmap=None, vmin=None, vmax=None,
                           alpha=1, linewidths=None, edgecolors=None)

            marker_size = 60

        plt.show()

    def cluster_OPTICS(self, plot=True):
        # like DBSCAN but calculates eps automatically

        db = OPTICS(min_samples=3, xi=0.05, min_cluster_size=0.05).fit(self.X)

        self.labels = db.labels_

        # Number of clusters in labels, ignoring noise if present.
        self.n_clusters_ = len(
            set(self.labels)) - (1 if -1 in self.labels else 0)
        self.n_noise_ = list(self.labels).count(-1)

        print(f'Clusters={self.n_clusters_} noise points={self.n_noise_}')

        if plot:
            self.show_clusters()

        return self.labels
