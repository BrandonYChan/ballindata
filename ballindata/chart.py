from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
pd.set_option('display.max_columns', None)
import sqlite3, sqlalchemy 
import logging, os, sys 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname('functions.py'), 'C:\\Users\\bchan\\OneDrive\\Personal Projects\\BID_Django\\ballindata\\PY'))) 
import functions  

seasons = functions.generate_seasons(1973, 2024)

engine = sqlalchemy.create_engine('sqlite:///C:\\Users\\bchan\\OneDrive\\Personal Projects\\BID_Django\\ballindata\\DB\\ballbase.db') 
dfs = [] 

for i in range(len(seasons)):
    df = pd.read_sql('master_'+seasons[i], con=engine) 
    df['Season'] = str(2000) if seasons[i][5:7] == '00' else str(seasons[i][0:2] + seasons[i][5:7]) 
    dfs.append(df) 


master = (pd.concat(dfs, axis=0)
          .rename(columns={'TRB':'RPG', 'AST':'APG', 'PTS':'PPG'}) 
)

app = DjangoDash('chart') 

app.layout = html.Div(children=[
    html.Div(children=[dcc.RadioItems(options=['PPG', 'APG', 'RPG', '3P%', 'FG%', 'FT%', 'STL', 'BLK', 'TOV', 'PF', 'G', 'MP', 'DRtg', 'ORtg', 'WS', 'DWS'], value='PPG', id='controls', inline=True)], style={'text-align':'center', 'font-family':'calibri'}),
    html.Div(children=[dcc.Dropdown(master.Player.unique(), value='LeBron James', id='dropdown-selection')], style={'font-family':'calibri'}), 
    html.Div( children=[dcc.Graph(figure={}, id='graph-content')]) 
], style={'background-color':'rgb(228, 138, 12)'}) 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.callback(
    Output(component_id='graph-content', component_property='figure'),
    Input('controls', 'value'), Input('dropdown-selection', 'value')
)
def update_graph(stat, player, **kwargs): 
    player = master[master.Player==player] 
    fig = px.line(player, x='Season', y=stat, color_discrete_sequence=['orange'], markers=True).update_layout(
        template='plotly_dark', 
        plot_bgcolor='rgba(0, 0, 0, 0)', 
    )
    return fig 

if __name__ == '__main__':
    app.run_server(debug=True) 
