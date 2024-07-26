from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
pd.set_option('display.max_columns', None)
import sqlite3, sqlalchemy 
import logging

engine = sqlalchemy.create_engine('sqlite:///C:\\Users\\bchan\\OneDrive\\Personal Projects\\BID_Django\\ballindata\\DB\\ballbase.db') 
seasons = ['2015_16', '2016_17', '2017_18', '2018_19', '2019_20', '2020_21', '2021_22', '2022_23', '2023_24']
dfs = [] 

for i in range(len(seasons)):
    df = pd.read_sql('master_'+seasons[i], con=engine) 
    df['Season'] = seasons[i].replace('_', '-')
    dfs.append(df) 


master = (pd.concat(dfs, axis=0)
          .rename(columns={'TRB':'RPG', 'AST':'APG', 'PTS':'PPG'}) 
)

app = DjangoDash('chart') 

app.layout = html.Div(children=[
    html.Div(children=[dcc.RadioItems(options=['PPG', 'APG', 'RPG', '3P%', 'FG%', 'FT%', 'STL', 'BLK', 'TOV', 'PF', 'G', 'MP', 'DRtg', 'ORtg', 'WS', 'DWS'], value='PPG', id='controls', inline=True)], style={'text-align':'center', 'font-family':'calibri'}), 
    html.Div(children=[dcc.Dropdown(master.Player.unique(), value='LeBron James', id='dropdown-selection')], style={'font-family':'calibri'}), 
    html.Div( children=[dcc.Graph(figure={}, id='graph-content')]) 
], style={'background-color':'rgb(255, 191, 14)'}) 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.callback(
    Output(component_id='graph-content', component_property='figure'),
    Input('controls', 'value'), Input('dropdown-selection', 'value')
)
def update_graph(stat, player, **kwargs): 
    player = master[master.Player==player] 
    fig = px.line(player, x='Season', y=stat, color_discrete_sequence=['orange'], markers=True)
    return fig 

if __name__ == '__main__':
    app.run_server(debug=True)