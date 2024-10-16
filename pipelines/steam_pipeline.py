# To explain this file is to iniate the pipeline with different functions. We will create these functions in the ETL. 
# ETL != Pipleine but rather we do all of our logic and data in the ETL file. 

# What we need to do is create functions that enable this
# 1. 

from etls.steam_etl import extract_games
import pandas as pd
def steam_pipeline():
    games = extract_games()

    # conver the list of games into a dataframe 
    games_df = pd.DataFrame(games)

    ## games_df = transform_games(games_df)

    ## load_games
