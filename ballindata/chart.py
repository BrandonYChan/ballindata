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
    html.Div(children=[dcc.RadioItems(options=['PPG', 'APG', 'RPG', '3P%', 'FG%', 'FT%', 'USG%', 'SPG', 'BPG', 'ToPG', 'PF', 'GP', 'MPG', 'DRtg', 'ORtg', 'WS', 'DWS', 'OWS', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 'BPM', 'OBPM', 'DBPM', 'VORP'], value='PPG', id='controls', inline=True)], style={'text-align':'center', 'font-family':'calibri'}),
    html.Div(children=[dcc.Dropdown(master.Player.unique(), value='LeBron James', id='dropdown-selection')], style={'font-family':'calibri'}), 
    html.Div(children=[dcc.Dropdown(master.Player.unique(), value='Kobe Bryant', id='dropdown-selection-2')], style={'font-family':'calibri'}), 
    html.Div( children=[dcc.Graph(figure={}, id='graph-content')]) 
], style={'background-color':'rgb(228, 138, 12)'}) 

@app.callback(
    Output(component_id='graph-content', component_property='figure'),
    [
     Input('controls', 'value'), 
     Input('dropdown-selection', 'value'),
     Input('dropdown-selection-2', 'value'), 
    ]
    
)
def update_graph(stat, p1, p2, **kwargs): 
    player1 = master[master.Player==p1] 
    player2 = master[master.Player==p2] 
    seasons = (pd.concat([player1['Season'], player2['Season']], axis=0)
               .astype('int64')
               .drop_duplicates()
               .sort_values() 
    )
    lg_avg = master.groupby('Season')[stat].mean().reset_index() 
    lg_avg = lg_avg[(lg_avg['Season']>=seasons.iloc[0].astype(str)) & (lg_avg['Season']<=seasons.iloc[len(seasons)-1].astype(str))] 
    fig = go.Figure() 
    fig.add_trace(go.Scatter(
        x = seasons, 
        y = lg_avg[stat], 
        mode = 'markers', 
        name = 'League Average',  
        line = dict(color='grey') 
    ))
    fig.add_trace(go.Scatter(
        x = player1['Season'], 
        y = player1[stat], 
        mode = 'lines+markers', 
        name = p1, 
        line = dict(color='orange'),  
        fillcolor='rgba(0, 0, 0, 0)',        
    ))
    fig.add_trace(go.Scatter(
        x = player2['Season'], 
        y = player2[stat], 
        mode = 'lines+markers', 
        name = p2, 
        line = dict(color='purple'),  
        fillcolor='rgba(0, 0, 0, 0)',        
    ))
    
    
    fig.update_layout(template = 'plotly_dark')
    fig.update_layout(showlegend=True) 
    return fig 

if __name__ == '__main__':
    app.run_server(debug=True) 
