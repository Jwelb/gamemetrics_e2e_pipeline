import requests
import os
import pandas as pd
import time
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.constants import CLIENT_ID,SECRET,AZURE_STORAGE,AZURE_KEY
# URL for the IGDB API
IGDB_URL = 'https://api.igdb.com/v4/games'


def get_igdb_token():
    """Authenticate with IGDB and retrieve the access token."""
    auth_url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(auth_url, params=params)
    response.raise_for_status()
    return response.json()['access_token']


def extract_games(token, limit, offset):
    """Extracts game data from the IGDB API with pagination."""
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = (
        f'fields aggregated_rating,aggregated_rating_count,'
        f'category,dlcs,first_release_date,'
        f'involved_companies,name,parent_game,'
        f'platforms,status,'
        f'themes,updated_at;'
        f'limit {limit}; offset {offset};'
    )
    response = requests.post(IGDB_URL, headers=headers, data=data)
    if response.status_code == 429:
        print("Rate limit hit, sleeping for 1 second.")
        time.sleep(1)
    response.raise_for_status()
    games_data = response.json()
    print("Adding games..")

    return games_data

def extract_all_games():
    """Extracts all games using pagination."""
    token = get_igdb_token()
    games = []
    offset = 0
    limit = 500 # Maximum limit for a single IGDB API request
    while True:
        game_data = extract_games(token, limit=limit, offset=offset)
        if not game_data:
            print("No more games found, ending extraction....")
            break
        games.extend(game_data)
        offset += limit
        print(f"Fetched {len(game_data)} games. Total so far: {len(games)}")


    return games

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
        print(f"Fetched {len(company_data)} companies. Total so far: {len(companies)}")

    return companies

def extract_company_data(token, limit, offset):
    """Extracts company data from the IGDB API with pagination."""
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = (
        f'fields name; limit {limit}; offset {offset};'
    )

    response = requests.post('https://api.igdb.com/v4/companies', headers=headers, data=data)
    if response.status_code == 429:
        print("Rate limit hit, sleeping for 1 second.")
        time.sleep(1)
    response.raise_for_status()
    companies = response.json()
    print("adding company...")

    return companies

def extract_platforms():
    """Extract platform data from IGDB."""
    token = get_igdb_token()
    url = 'https://api.igdb.com/v4/platforms'
    headers = {
        'Client-ID': CLIENT_ID,
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
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = 'fields name; limit 500;'
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def load_data_to_azure(data: pd.DataFrame, filename: str):
    file_name = (f'{filename}'+ '.csv')
    azure_file_path= f'abfs://steamdata/data/{file_name}'
    data.to_csv(azure_file_path, storage_options={
        'account_name': AZURE_STORAGE,
        'account_key' : AZURE_KEY}, index=False
    )

