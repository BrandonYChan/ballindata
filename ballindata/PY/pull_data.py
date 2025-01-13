# Imports 
import requests 
from bs4 import BeautifulSoup
import html
import pandas as pd, numpy as np 
from io import StringIO
import math  
import sqlite3, sqlalchemy 
import re 

# Functions 
def clean_player(name): 
    i = name.find('*')   
    name = name[:i] if i > -1 else name 
    return name 

def load_soup(URL): 
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html') 

    return soup 

def select_team(group):
    value = group.head(1) 
    if 'Team' in value.columns:
        if len(group) > 1: 
            value['Team'] = "" 
            for i in range(1, len(group)):
                value['Team'] += group.iloc[i]['Team'] 
                value['Team'] += '-' if i < len(group)-1 else ''  
    else: 
        if len(group) > 1: 
            value['Tm'] = "" 
            for i in range(1, len(group)):
                value['Tm'] += group.iloc[i]['Tm'] 
                value['Tm'] += '-' if i < len(group)-1 else ''  
    return value 

def html_df(soup, key, value, remove_cols=['Rk'], drop_cols=True, drop_lvl=False): 
    stat_df = soup.find('table', attrs={key:value}) 
    stat_df = pd.read_html(StringIO(str(stat_df))) 
    stat_df = pd.DataFrame(stat_df[0]) 
    if drop_lvl: 
        stat_df.columns = stat_df.columns.droplevel() 
    stat_df = stat_df.groupby('Player').apply(lambda x: select_team(x)).reset_index(drop=True) 
    stat_df['Player'] = stat_df['Player'].apply(lambda x: clean_player(x)) 
    if drop_cols==True:  
        stat_df = stat_df.drop(remove_cols, axis=1) 

    return stat_df 

def combine_dfs(dfs):
    curr = None
    for name in dfs.keys():
        if curr is None: 
            curr = dfs[name]
        else:
            diff = dfs[name].columns.difference(curr.columns).tolist()
            diff.append('Player') 
            curr = pd.merge(curr, dfs[name].loc[:,diff], on = 'Player') 
    return curr  

def clean_if_dirty(master):
    filtered = master[master['Player']=='Player']
    pos = filtered.index
    master = master.drop(pos, axis=0) 
    master['Player'] = master['Player'].apply(lambda x: clean_player(x)) 
    master = master.dropna(axis=1, how='all')   
    if ('Tm' in master.columns) & ('Team' in master.columns): 
        master = master.drop('Tm', axis=1) 
         
    return master 

def mod_types_pct(master): 
    for col_name in master.columns: 
        if col_name not in ['Player', 'Team', 'Tm', 'Pos', 'Awards']:  
            master[col_name] = master[col_name].astype("float64")
        if col_name in ['FG%', '3P%', 'FT%', 'eFG%', 'TS%', '2P%']:
            master[col_name] *= 100 
    return master

def process_totals(totals, names): 
    if '3P' in totals.columns:  
        totals = totals.loc[:,['PTS', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'MP', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB']] 
    elif 'BLK' in totals.columns: 
        totals = totals.loc[:,['PTS', 'TRB', 'AST', 'STL', 'BLK', 'PF', 'MP', 'FG', 'FGA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB']] 
    elif 'TRB':
        totals = totals.loc[:,['PTS', 'TRB', 'AST', 'PF', 'FG', 'FGA', '2P', '2PA', 'FT', 'FTA']] 
    else: 
        totals = totals.loc[:,['PTS', 'AST', 'PF', 'FG', 'FGA', '2P', '2PA', 'FT', 'FTA']] 
    totals.columns = 'T' + totals.columns 
    totals['Player'] =  names 

    return totals 

def process_averages(master):
    if 'TOV' in master.columns: 
        new = master.rename(columns={'G':'GP', 'MP':'MPG', 'ORB':'ORPG', 'DRB':'DRPG', 'TRB':'RPG', 'AST':'APG', 'STL':'SPG', 'BLK':'BPG', 'TOV':'ToPG', 'PTS':'PPG'}, errors="raise")
    elif 'BLK' in master.columns: 
        new = master.rename(columns={'G':'GP', 'MP':'MPG', 'ORB':'ORPG', 'DRB':'DRPG', 'TRB':'RPG', 'AST':'APG', 'STL':'SPG', 'BLK':'BPG', 'PTS':'PPG'}, errors="raise") 
    elif 'TRB' in master.columns: 
        new = master.rename(columns={'G':'GP', 'TRB':'RPG', 'AST':'APG', 'PTS':'PPG'}, errors="raise") 
    else: 
        new = master.rename(columns={'G':'GP', 'AST':'APG','PTS':'PPG'}, errors="raise") 

    return new  

# Extract Data 
engine = sqlalchemy.create_engine('sqlite:///../../DB/ballbase.db') 

start_ssn = 2024     
stop_ssn = 2025                    

for season in range(start_ssn, stop_ssn): 
    
    URL_averages = 'https://www.basketball-reference.com/leagues/NBA_' + str(season+1) + '_per_game.html' 
    soup_averages = load_soup(URL_averages) 
    averages = html_df(soup_averages, 'id', 'per_game_stats', ['Rk'])  

    URL_totals = 'https://www.basketball-reference.com/leagues/NBA_' + str(season+1) + '_totals.html' 
    soup_totals = load_soup(URL_totals) 
    totals = html_df(soup_totals, 'id', 'totals_stats', ['Rk']) 
    totals = process_totals(totals, averages['Player'])   
    
    if season >= 1973: 
        URL_per100 = 'https://www.basketball-reference.com/leagues/NBA_' + str(season+1) + '_per_poss.html' 
        soup_per100 = load_soup(URL_per100) 
        try:
            per100 = html_df(soup_per100, 'id', 'per_poss', ['Rk', 'Unnamed: 29']) 
        except:
            per100 = html_df(soup_per100, 'id', 'per_poss', ['Rk']) 

    URL_advanced = 'https://www.basketball-reference.com/leagues/NBA_' + str(season+1) + '_advanced.html'  
    soup_advanced = load_soup(URL_advanced) 
    try: 
        advanced = html_df(soup_advanced, 'id', 'advanced', ['Rk', 'Unnamed: 19', 'Unnamed: 24'])  
    except:
        advanced = html_df(soup_advanced, 'id', 'advanced', ['Rk'])  

    if season >= 1973: 
        dfs = {"averages": averages, "totals": totals, "per100": per100, "advanced": advanced} 
    else: 
        dfs = {"averages": averages, "totals": totals, "advanced": advanced} 

    season_str = str(season) + '_' + str(season+1)[2:]
    master = combine_dfs(dfs) 
    master = clean_if_dirty(master) 
    master = mod_types_pct(master) 
    master = process_averages(master) 
    
    master.to_sql('master_'+season_str, con=engine, if_exists='replace', index=False) 
    
# Clean and Upload to Database 
engine = sqlalchemy.create_engine('sqlite:///../../DB/ballbase.db') 

start_ssn = 2024   
stop_ssn = 2025     

for season in range(start_ssn, stop_ssn):   
    season_str = str(season) + '_' + str(season+1)[2:] 
    master = pd.read_sql("master"+"_"+season_str, con=engine)  

    # Cleaning code here ... 
    master = master.sort_values(by='PPG', ascending=False)
            
    master.to_sql('master'+'_'+season_str, con = engine, if_exists = 'replace', index = False)  
        



