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
    return response.json()['access_token']


def extract_games(token, limit=50, offset=0):
    """Extracts game data from the IGDB API with pagination."""
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = (
        f'fields aggregated_rating,aggregated_rating_count,'
        f'category,dlcs,first_release_date,'
        f'involved_companies,name,parent_game,'
        f'platforms,status,storyline,'
        f'summary,themes,updated_at;'
        f'limit {limit}; offset {offset};'
    )

    games = []
    while True:
        response = requests.post(IGDB_URL, headers=headers, data=data)
        if response.status_code == 429:
            print("Rate limit hit, sleeping for 1 second.")
            time.sleep(1)
            continue
        response.raise_for_status()
        result = response.json()
        if not result:  # No more results
            break
        games.extend(result)
        offset += limit

    return games


def extract_all_games():
    """Extracts all games using pagination."""
    token = get_igdb_token()
    games = []
    offset = 0
    limit = 150  # Maximum limit for a single IGDB API request

    while True:
        game_data = extract_games(token, limit=limit, offset=offset)
        if not game_data:
            break
        games.extend(game_data)
        offset += limit

    return games


def extract_all_companies():
    """Extracts all companies using pagination."""
    token = get_igdb_token()
    companies = []
    offset = 0
    limit = 150  # Maximum limit for a single IGDB API request

    while True:
        company_data = extract_company_data(token, limit=limit, offset=offset)
        if not company_data:
            break
        companies.extend(company_data)
        offset += limit

    return companies


def extract_company_data(token, limit=50, offset=0):
    """Extracts company data from the IGDB API with pagination."""
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = (
        f'fields name;'
    )

    companies = []
    while True:
        response = requests.post('https://api.igdb.com/v4/companies', headers=headers, data=data)
        if response.status_code == 429:
            print("Rate limit hit, sleeping for 1 second.")
            time.sleep(1)
            continue
        response.raise_for_status()
        result = response.json()
        if not result:  # No more results
            break
        companies.extend(result)
        offset += limit

    return companies

def extract_platforms():
    """Extract platform data from IGDB."""
    token = get_igdb_token()
    url = 'https://api.igdb.com/v4/platforms'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = 'fields name;'
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
    data = 'fields name;'
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def transform_data(games):
    """Performs data transformations on the game data."""
    if not games:
        print("No data to transform.")
        return pd.DataFrame()

    # Flatten the list of dictionaries into a DataFrame
    games_df = pd.json_normalize(games)
    return games_df

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

    file_name = f'PlatformData_{datetime.now().date()}_{datetime.now().strftime("%H_%M_%S")}.csv'
    print(f"Saving to {file_name}")
    data.to_csv(file_name, index=False)

def load_Companydata_to_csv(data: pd.DataFrame):
    """Loads the transformed data to a CSV file."""
    if data.empty:
        print("No data to save.")
        return

    file_name = f'CompanyData_{datetime.now().date()}_{datetime.now().strftime("%H_%M_%S")}.csv'
    print(f"Saving to {file_name}")
    data.to_csv(file_name, index=False)

def load_Themedata_to_csv(data: pd.DataFrame):
    """Loads the transformed data to a CSV file."""
    if data.empty:
        print("No data to save.")
        return

    file_name = f'ThemeData_{datetime.now().date()}_{datetime.now().strftime("%H_%M_%S")}.csv'
    print(f"Saving to {file_name}")
    data.to_csv(file_name, index=False)

async def extract_and_transform():
    """Combines extraction and transformation."""
    games = await extract_all_games()
    games_df = transform_data(games)
    return games_df


async def main():
    """Main function to orchestrate the extraction, transformation, and loading process."""

    # Extract and transform game data asynchronously
    #print("Extracting and transforming game data...")
    #games_df = await extract_and_transform()

    # Load game data to CSV if there is data
    #if not games_df.empty:
        #load_Gamedata_to_csv(games_df)

    # Extract and load platform data (regular function)
    print("Extracting platform data...")
    #platform_data = extract_platforms()
    #platform_df = pd.json_normalize(platform_data)
    #load_Platformdata_to_csv(platform_df)

    # Extract and load theme data (regular function)
    print("Extracting theme data...")
    #theme_data = extract_themes()
    #theme_df = pd.json_normalize(theme_data)
    #load_Themedata_to_csv(theme_df)

    # Extract and load company data asynchronously
    print("Extracting company data...")
    company_data = extract_all_companies()
    company_df = pd.json_normalize(company_data)
    load_Companydata_to_csv(company_df)

# Entry point to run async code
if __name__ == "__main__":
    try:
        # Use asyncio.run() to call the main async function
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")

