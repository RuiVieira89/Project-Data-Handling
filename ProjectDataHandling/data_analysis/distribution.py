import seaborn as sns
import matplotlib.pyplot as plt


def jointplot(data):
    
    
    sns.jointplot(data=data)

def pairplot(data):
    
    sns.pairplot(data=data)


def grid_plot_dist(data):
    
    g = sns.PairGrid(data)
    g.map_upper(sns.histplot)
    g.map_lower(sns.kdeplot, fill=True)
    g.map_diag(sns.histplot, kde=True)


def catplot(data, kind):
    # kind "violin" or "box"
    
    sns.catplot(data=data, kind=kind)



def relplot(data):

    sns.relplot(
        data=data, kind="line",
        errorbar="sd"
    )


