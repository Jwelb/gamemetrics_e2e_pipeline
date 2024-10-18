# To explain this file is to iniate the pipeline with different functions. We will create these functions in the ETL. 
# ETL != Pipleine but rather we do all of our logic and data in the ETL file. 

# What we need to do is create functions that enable this
# 1. 
import sys
import os
import pandas as pd
print(__file__)
print(sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../etls'))))

from steam_etl import test,transform_data,load_data_to_csv

def steam_pipeline():
    
    # Were gonna get all the ids.
    # Then were gonnna loop through all the ids were gonna check if the id is in 
    games = test()
    games_df = pd.DataFrame(games)
    # Transforms the data 
    transformed_data = transform_data(games_df)
    load_data_to_csv(transformed_data)
    
    
    
    