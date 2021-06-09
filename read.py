import sys
from urllib import request

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from random import random
from dash.dependencies import Input, Output
app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('Sensor data'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=2000,  # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    if len(sys.argv) == 1:
        ip = ""
    else:
        ip = sys.argv[1]
    req = request.Request(f"http://{ip}", method="GET")
    with request.urlopen(req) as f:
        r = f.read().decode('utf-8')
        data = list(map(lambda num: float(num) / 10., r.split(";")))
    df = pd.read_csv("data.csv")
    df = df.append({'temperature': data[0],
                    'humidity': data[1]}, ignore_index=True)
    df.to_csv('data.csv')
    df = pd.read_csv("data.csv")
    fig1 = plotly.graph_objs.Scatter(
        x=list(range(len(df.temperature))),
        y=df.temperature.tolist(),
        name='temperature',
        mode='lines+markers',
        yaxis='y1'
    )
    fig2 = plotly.graph_objs.Scatter(
        x=list(range(len(df.humidity))),
        y=df.humidity.tolist(),
        name='humidity',
        mode='lines+markers',
        yaxis='y2'
    )
    return {'data': [fig1, fig2],
            'layout': dict(
            plot_bgcolor='#FFF',
            showlegend=True,
            legend=dict(x=0, y=1.2),
            yaxis1=dict(
                side='left',
                linecolor='black',
                title='Temperature(℃)',
                ticks='inside',
            ),
        yaxis2=dict(overlaying='y1',
                    side='right',
                    linecolor='black',
                    anchor='x',
                    title='Humidity(%)',
                    ticks='inside',
                    ),
        hovermode='closest',
    )
    }


if __name__ == '__main__':
    df = pd.DataFrame({'temperature': [], 'humidity': []})
    df.to_csv("data.csv")
    app.run_server(debug=False)
