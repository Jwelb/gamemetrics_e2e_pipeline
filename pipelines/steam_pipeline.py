# To explain this file is to iniate the pipeline with different functions. We will create these functions in the ETL. 
# ETL != Pipleine but rather we do all of our logic and data in the ETL file. 

# What we need to do is create functions that enable this
# 1. 

from etls.steam_etl import extract_game_by_id,get_app_ids,get_app_details,extract_all_games
import pandas as pd
def steam_pipeline():
    
    # Were gonna get all the ids.
    # Then were gonnna loop through all the ids were gonna check if the id is in 
    games = extract_all_games()
    games_df = pd.DataFrame(games)
    # Tranformation
    tranform_data()
    load_to_azure()
    
    
    