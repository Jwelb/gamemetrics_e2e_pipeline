import requests
import os
import pandas as pd
import asyncio
import aiohttp
from datetime import datetime

# IGDB API Credentials (set these in your environment variables)
client_id = os.getenv('Client_Id')
client_secret = os.getenv('Client_secret')

# URL for the IGDB API
IGDB_URL = 'https://api.igdb.com/v4/games'

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

async def extract_games(token, limit=50, offset=0):
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

    async with aiohttp.ClientSession() as session:
        async with session.post(IGDB_URL, headers=headers, data=data) as response:
            if response.status == 429:
                print("Rate limit hit, sleeping for 1 second.")
                await asyncio.sleep(1)
                return await extract_games(token, limit, offset)  # Retry after sleeping
            response.raise_for_status()
            return await response.json()

async def extract_all_games():
    """Extracts all games using pagination."""
    token = get_igdb_token()
    games = []
    offset = 0
    limit = 50  # Maximum limit for a single IGDB API request

    # Use a semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(4)

    async def fetch_games(offset):
        async with semaphore:
            game_data = await extract_games(token, limit=limit, offset=offset)
            return game_data

    while True:
        tasks = [fetch_games(offset) for _ in range(8)]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                games.extend(result)
            else:
                print("No more results to fetch.")
                return games

        offset += limit
        if len(results) < 8:  # If fewer results than requested, exit loop
            break

        await asyncio.sleep(0.25)  # Avoid exceeding request limits

    return games

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

if __name__ == "__main__":
    platforms = extract_platforms()
    themes = extract_themes()
    df_platforms = pd.DataFrame(platforms)
    df_themes = pd.DataFrame(themes)
    load_Platformdata_to_csv(df_platforms)
    load_Themedata_to_csv(df_themes)
    # Uncomment to run game extraction
    # games_df = asyncio.run(extract_and_transform())
    # print(f"Extracted {len(games_df)} rows.")
    # load_data_to_csv(games_df)
