import numpy as np, pandas as pd 
pd.set_option('display.max_columns', None)
import sqlite3, sqlalchemy, os, sys  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname('functions.py'), '..', '..', 'PY')))
import functions 

seasons = functions.generate_seasons(1974, 1984)

engine = sqlalchemy.create_engine("sqlite:///C:\\Users\\bchan\\OneDrive\\Personal Projects\\BID_Django\\ballindata\\DB\\ballbase.db")

for season in seasons:
    engine = sqlalchemy.create_engine("sqlite:///../../DB/ballbase.db")
    
    master = pd.read_sql("master_"+season, con=engine).fillna(0).drop("Tm", axis=1)
    master.columns 
    averages = master[['Player', 'Pos', 'Age', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'MP', 'FGA', 'FG%', '3PA', '3P%', 'FTA', 'FT%', 'PF']] 
    totals = master.loc[:, ['Player', 'TPTS', 'TSTL',
        'TTOV', 'TTRB', 'T2P', 'T2PA', 'T3PA', 'TAST', 'TBLK', 'TDRB',
        'TFG', 'TFGA', 'TFT', 'TFTA', 'TMP', 'TORB', 'TPF']]
    advanced = master.loc[:, ['Player', 'DRtg', 'ORtg',
        '3PAr', 'AST%', 'BLK%', 'BPM', 'DBPM', 'DRB%', 'DWS', 'FTr', 'OBPM',
        'ORB%', 'OWS', 'PER', 'STL%', 'TOV%', 'TRB%', 'TS%', 'USG%', 'VORP',
        'WS', 'WS/48']] 


    contents = [averages, totals, advanced] 
    # Create HTML table version 
    for i in range(len(contents)):
        contents[i] = contents[i].to_html(table_id="table", classes = "table table-hover table-stripped table-bordered table-striped", index=False)

    # Create page content 
    for i in range(len(contents)):
        contents[i] = f"""
        {{%extends 'TableBase.html'%}}
        {{% block table %}} 
        
        {contents[i]}
        {{% endblock %}}
    """
    def write_to_file(path, content): 
        file = open(path, "w", encoding="utf-8") 
        file.write(content) 
        file.close 


    file_names=[f"Averages_{season}.html", f"Totals_{season}.html", f"Advanced_{season}.html"] 

    for i in range(len(contents)): 
        path = f"../../templates/Tables/{file_names[i]}" 
        write_to_file(path, contents[i]) 
        