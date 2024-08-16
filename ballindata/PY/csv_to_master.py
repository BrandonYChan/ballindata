import pandas as pd, numpy as np 
pd.set_option('display.max_columns', None)
import sqlalchemy, sqlite3 

seasons = ["2007_08", "2008_09", "2009_10", "2010_11", "2011_12", "2012_13", "2013_14", "2014_15", "2015_16", "2016_17", "2017_18", "2018_19", "2019_20", "2020_21", "2021_22", "2022_23", "2023_24"]
engine = sqlalchemy.create_engine("sqlite:///C:\\Users\\bchan\\OneDrive\\Personal Projects\\BID_Django\\ballindata\\DB\\ballbase.db") 

for season in seasons:
    dir = f"../../static/CSV/{season}/" 

    names = ['pergame_'+season, 'advanced_'+season, 'per100_'+season, 'playbyplay_'+season, 'totals_'+season]  
    dfs = {} 

    invalid = ['-9999', 'Unnamed', 'Rk', 'Player-additional']

    for name in names:
        dfs[name] = pd.read_csv(dir+name+'.csv') 
        for inv in invalid:
            for col in dfs[name].columns:
                if inv in col or col in invalid:

                    dfs[name] = dfs[name].drop([col], axis=1)
                    
    dfs['totals_'+season] = dfs['totals_'+season].loc[:,['PTS', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'MP', 'FG', 'FGA', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB']] 
    dfs['totals_'+season].columns = 'T' + dfs['totals_'+season].columns 
    dfs['totals_'+season]['Player'] =  dfs['pergame_'+season]['Player']

    def combine_dfs(dfs, names):
        curr = None
        for name in names:
            if curr is None: 
                curr = dfs[name]
            else:
                diff = dfs[name].columns.difference(curr.columns).tolist()
                diff.append('Player') 
                curr = pd.merge(curr, dfs[name].loc[:,diff], on = 'Player') 
        return curr     

    master = combine_dfs(dfs, names) 

    for name in names:
        dfs[name].to_sql(name, con = engine, if_exists = 'replace', index = False)  
        
    master.to_sql('master_'+season, con=engine, if_exists='replace', index=False) 
    