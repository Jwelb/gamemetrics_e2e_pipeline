# To explain this file is to iniate the pipeline with different functions. We will create these functions in the ETL. 
# ETL != Pipleine but rather we do all of our logic and data in the ETL file. 

# What we need to do is create functions that enable this
# 1. 
import sys
import os
import pandas as pd
print(__file__)
print(sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../etls'))))

from game_etl import extract_platforms,extract_themes,extract_all_companies, extract_all_games, load_data_to_azure


def game_pipeline():
    """Main function to orchestrate the extraction, transformation, and loading process."""
    # Extract game data
    print("Extracting and transforming game data...")
    games = extract_all_games()
    games_df = pd.DataFrame(games)
    game_path = '/data/GameData.csv'
    games_df.to_csv(game_path)

    # Extract  platform data 
    print("Extracting platform data...")
    platform_data = extract_platforms()
    platform_df = pd.DataFrame(platform_data)
    platform_path = '/data/PlatformData.csv'
    platform_df.to_csv(platform_path)

    # Extract theme data 
    print("Extracting theme data...")
    theme_data = extract_themes()
    theme_df = pd.DataFrame(theme_data)
    theme_path = '/data/ThemeData.csv'
    theme_df.to_csv(theme_path)

    # Extract  company data
    print("Extracting company data...")
    company_data = extract_all_companies()
    company_df = pd.DataFrame(company_data)
    company_path = '/data/CompanyData.csv'
    company_df.to_csv(company_path)


def load():
    game_path = '/data/GameData.csv'
    platform_path = '/data/PlatformData.csv'
    theme_path = '/data/ThemeData.csv'
    company_path = '/data/CompanyData.csv'

    games_df = pd.read_csv(game_path)
    platform_df = pd.read_csv(platform_path)
    theme_df = pd.read_csv(theme_path)
    company_df = pd.read_csv(company_path)
    # load all the data into azure
    load_data_to_azure(games_df,game_path)
    load_data_to_azure(platform_df,platform_path)
    load_data_to_azure(theme_df,theme_path)
    load_data_to_azure(company_df,company_path)
    
    
    
    
    