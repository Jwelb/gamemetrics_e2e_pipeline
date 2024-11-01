import requests
import os
import pandas as pd
import asyncio
import aiohttp
import time
from datetime import datetime

# IGDB API Credentials (set these in your environment variables)
client_id = os.getenv('Client_Id')
client_secret = os.getenv('Client_secret')

# URL for the IGDB API
IGDB_URL = 'https://api.igdb.com/v4/games'
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Good
def get_igdb_token():
    """Authenticate with IGDB and retrieve the access token."""
    auth_url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(auth_url, params=params)
    response.raise_for_status()
    print(response.json()['access_token'])
    return response.json()['access_token']

# Good
def extract_games(token, limit, offset):
    """Extracts game data from the IGDB API with pagination."""
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    # Remove story line [DONE]
    data = (
        f'fields aggregated_rating,aggregated_rating_count,'
        f'category,dlcs,first_release_date,'
        f'involved_companies,name,parent_game,'
        f'platforms,status'
        f'themes,updated_at;'
        f'limit {limit}; offset {offset};'
    ) 
    games = []
    
    response = requests.post(IGDB_URL, headers=headers, data=data)
    if response.status_code == 429:
        print("Rate limit hit, sleeping for 1 second.")
        time.sleep(1)
    response.raise_for_status()
    data = response.json()
    print("Adding games..")
    for item in data:
        game_data = {
        "id": item.get("id", "N/A"),
        "aggregated_rating": item.get("aggregated_rating", "N/A"),
        "aggregated_rating_count": item.get("aggregated_rating_count", "N/A"),
        "category": item.get("category", "N/A"),
        "dlcs": item.get("dlcs", "N/A"),
        "first_release_date": item.get("first_release_date", "N/A"),
        "involved_companies": item.get("involved_companies", "N/A"),
        "name": item.get("name", "N/A"),
        "parent_game": item.get("parent_game", "N/A"),
        "platforms": item.get("platforms", "N/A"),
        "status": item.get("status", "N/A"),
        "themes": item.get("themes", "N/A"),
        "updated_at": item.get("updated_at", "N/A"),
        }
        games.append(game_data)
    offset += limit

    return games

# Good
def extract_all_games():
    """Extracts all games using pagination."""
    token = get_igdb_token()
    games = []
    offset = 0
    limit = 500 # Maximum limit for a single IGDB API request
    total_game_data = 0
    while True:
        game_data = extract_games(token, limit=limit, offset=offset)
        total_game_data += len(game_data)
        if not game_data:
            print("No more games found, ending extraction....")
            break
        games.extend(game_data)
        offset += limit
        print(f"Fetched {len(game_data)} companies. Total so far: {total_game_data}")


    return games

# BINGOOOO EXACTLY RIGHT
def extract_all_companies():
    """Extracts all companies using pagination."""
    token = get_igdb_token()
    companies = []
    offset = 0
    limit = 500  # Maximum limit for a single IGDB API request

    while True:
        company_data = extract_company_data(token, limit=limit, offset=offset)
        if not company_data:
            print("No more companies found, ending extraction...")
            break
        companies.extend(company_data)
        offset += limit
        print(f"Fetched {len(company_data)} companies. Total so far: {len(company_data)}")

    return companies


# BINGOOOOO EXACTLY RIGHT
def extract_company_data(token, limit, offset):
    """Extracts company data from the IGDB API with pagination."""
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = (
        f'fields name; limit {limit}; offset {offset};'
    )

    companies = []
    response = requests.post('https://api.igdb.com/v4/companies', headers=headers, data=data)
    if response.status_code == 429:
        print("Rate limit hit, sleeping for 1 second.")
        time.sleep(1)
    response.raise_for_status()
    result = response.json()
    print("adding company...")
    companies.extend(result)

    return companies

# Good
def extract_platforms():
    """Extract platform data from IGDB."""
    token = get_igdb_token()
    url = 'https://api.igdb.com/v4/platforms'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = 'fields name; limit 500;'
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

def extract_themes():
    """Extract theme data from IGDB."""
    token = get_igdb_token()
    url = 'https://api.igdb.com/v4/themes'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = 'fields name; limit 500;'
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

# All these loading functions will need to be configured to one function to load in Azure Storage container. Reference the added_functions.py
def load_Gamedata_to_csv(data: pd.DataFrame):
    """Loads the transformed data to a CSV file."""
    if data.empty:
        print("No data to save.")
        return

    file_name = f'GameData.csv'
    print(f"Saving to {file_name}")
    data.to_csv(file_name, index=False)

def load_Platformdata_to_csv(data: pd.DataFrame):
    """Loads the transformed data to a CSV file."""
    if data.empty:
        print("No data to save.")
        return

    file_name = f'PlatformData.csv'
    print(f"Saving to {file_name}")
    data.to_csv(file_name, index=False)

def load_Companydata_to_csv(data: pd.DataFrame):
    """Loads the transformed data to a CSV file."""
    if data.empty:
        print("No data to save.")
        return

    file_name = f'CompanyData.csv'
    print(f"Saving to {file_name}")
    data.to_csv(file_name, index=False)

def load_Themedata_to_csv(data: pd.DataFrame):
    """Loads the transformed data to a CSV file."""
    if data.empty:
        print("No data to save.")
        return

    file_name = f'ThemeData_.csv'
    print(f"Saving to {file_name}")
    data.to_csv(file_name, index=False)

def extract_gamesdf():
    """Combines extraction and transformation."""
    games = extract_all_games()
    games_df = pd.DataFrame(games)
    return games_df


def main():
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
    company_df = pd.json_normalize(company_data)
    load_Companydata_to_csv(company_df)

# Entry point to run async code
if __name__ == "__main__":
    try:
        # Use asyncio.run() to call the main async function
        main()
    except Exception as e:
        print(f"An error occurred: {e}")

