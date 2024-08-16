def generate_seasons(start, stop): 
        years = [y for y in range(start, stop)] 
        seasons = [str(y) + '_' + str(y+1)[2:] for y in years] 
        return seasons 
    