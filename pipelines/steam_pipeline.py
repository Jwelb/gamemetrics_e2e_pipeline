# To explain this file is to iniate the pipeline with different functions. We will create these functions in the ETL. 
# ETL != Pipleine but rather we do all of our logic and data in the ETL file. 

# What we need to do is create functions that enable this
# 1. 
import sys
import os
import pandas as pd
print(__file__)
print(sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../etls'))))

from game_etl import extract_gamesdf,load_GameData_to_csv,extract_platforms,extract_themes,extract_all_companies,load_GameData_to_csv,load_Platformdata_to_csv,load_Themedata_to_csv,load_CompanyData_to_csv

def game_pipeline():
    """Main function to orchestrate the extraction, transformation, and loading process."""

    # Extract and transform game data asynchronously
    print("Extracting and transforming game data...")
    games_df = extract_gamesdf()
    load_Gamedata_to_csv(games_df)
    # Load game data to CSV if there is data
    #if not games_df.empty:
        #load_Gamedata_to_csv(games_df)

    # Extract and load platform data (regular function)
    print("Extracting platform data...")
    platform_data = extract_platforms()
    platform_df = pd.DataFrame(platform_data)
    load_Platformdata_to_csv(platform_df)

    # Extract and load theme data (regular function)
    print("Extracting theme data...")
    theme_data = extract_themes()
    theme_df = pd.DataFrame(theme_data)
    load_Themedata_to_csv(theme_df)

    # Extract and load company data asynchronously
    print("Extracting company data...")
    company_data = extract_all_companies()
    load_Companydata_to_csv(company_df)
    
    
    
    
    