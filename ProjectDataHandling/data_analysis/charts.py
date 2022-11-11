
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.offline import init_notebook_mode
init_notebook_mode(connected = True)

import plotly.io as pio
pio.renderers.default = "browser"

def waterfall_chart(df, title=''):
    
    import sys
    f = open("waterfall_chart.html", 'w', encoding="utf-8")
    sys.stdout = f

    fig = go.Figure()

    fig.add_trace(go.Waterfall(x=df[df.columns[0]], 
                               y=df[df.columns[1]],
                               measure = df[df.columns[2]].tolist(),
                               base = 0,   #by default
                               #get dotted line as connector
                               connector = {"line":{"dash":"dot"}},
                               textposition = "outside",
                               text = df[df.columns[1]].tolist(),
                               orientation = "v",
                               decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
                               increasing = {"marker":{"color":"Teal", "line":{"color":"Aquamarine","width": 3}}},
                               totals = {"marker":{"color":"deep sky blue", "line":{"color":"blue", "width":3}}},
                               
                               ))

    fig.update_layout(title=title,
                    #layout_yaxis_range=[max(df[df.columns[1]]), min(df[df.columns[1]])],
                    #height = 600,
                    #width = 800
                    )

    #fig.layout.yaxis.range = [max(df[df.columns[1]])/10, min(df[df.columns[1]])/10]
    
    #plt.show()
    #Set y-limit
    #fig.update_yaxes(range = (max(df[df.columns[1]]), min(df.loc[df["measure"] == "total"][df.columns[1]])))
    #fig.update_yaxes(autorange="reversed")

    fig.show(renderer="svg")
    
    f.close()

    
