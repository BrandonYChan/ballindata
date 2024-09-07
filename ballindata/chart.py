from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.graph_objects as go 
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
pd.set_option('display.max_columns', None)
import sqlite3, sqlalchemy 
import logging, os, sys 
from django.conf import settings 

engine = sqlalchemy.create_engine(f"sqlite:///{os.path.join(settings.BASE_DIR, 'ballindata/DB/ballbase.db')}") 
master = pd.read_sql('master_plt', con=engine) 

app = DjangoDash('chart') 

app.layout = html.Div(children=[
    html.Div(children=[dcc.RadioItems(options=['PPG', 'APG', 'RPG', '3P%', 'FG%', 'FT%', 'SPG', 'BPG', 'ToPG', 'PF', 'GP', 'MPG', 'DRtg', 'ORtg', 'WS', 'DWS', 'OWS', 'FGA', '3PA', '2PA'], value='PPG', id='controls', inline=True)], style={'text-align':'center', 'font-family':'calibri'}),
    html.Div(children=[dcc.Dropdown(master.Player.unique(), value='LeBron James', id='dropdown-selection')], style={'font-family':'calibri'}), 
    html.Div( children=[dcc.Graph(figure={}, id='graph-content')]) 
], style={'background-color':'rgb(228, 138, 12)'}) 

@app.callback(
    Output(component_id='graph-content', component_property='figure'),
    Input('controls', 'value'), Input('dropdown-selection', 'value')
)
def update_graph(stat, player_name, **kwargs): 
    player = master[master.Player==player_name] 
    lg_avg = master.groupby('Season')[stat].mean().reset_index() 
    lg_avg = lg_avg[(lg_avg['Season']>=player.Season.iloc[0]) & (lg_avg['Season']<=player.Season.iloc[len(player.Season)-1])]
    fig = go.Figure() 
    fig.add_trace(go.Scatter(
        x = player['Season'], 
        y = player[stat], 
        mode = 'lines+markers', 
        name = player_name, 
        line = dict(color='orange'),  
        fillcolor='rgba(0, 0, 0, 0)',        
    ))
    fig.add_trace(go.Scatter(
        x = lg_avg['Season'], 
        y = lg_avg[stat], 
        mode = 'lines+markers', 
        name = 'League Average',  
        line = dict(color='grey') 
    ))
    fig.update_layout(template = 'plotly_dark')
    fig.update_layout(showlegend=True) 
    return fig 

if __name__ == '__main__':
    app.run_server(debug=True) 
