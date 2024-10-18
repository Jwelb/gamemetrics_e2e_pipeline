import requests
import json
import time
import os
import pandas as pd

PROCESSED_IDS_FILE = 'processed_ids.json'

# These load and save functions are to pass this file into xcom to use with other tasks in airflow. 
def load_processed_data():
    if os.path.exists(PROCESSED_IDS_FILE):
        with open(PROCESSED_IDS_FILE, 'r') as f:
            return set(json.load(f))  # Use set for faster lookups
    return set()
    
def save_processed_data(processed_ids):
    with open(PROCESSED_IDS_FILE, 'w') as f:
        json.dump(list(processed_ids), f)



def get_app_ids():
    """Fetches the list of all Steam apps."""
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
    response = requests.get(url)
    app_list = response.json()
    return app_list['applist']['apps']

# This gets the app details based on the specified app_id and returns json. 
def get_app_details(app_id):
    """Fetches details for a specific app using its app ID."""
    url = f'http://store.steampowered.com/api/appdetails?appids={app_id}'
    response = requests.get(url)
    return response.json()


# When calling the store api it must be within 200 per 5 minutes I have calculated it and it would do 57600 requests per day. 
# This is a function that recieves the id as a parameter and Returns a extracted data frame from API
def extract_game_by_id(id):
        # This creates a processed_data variable to make sure that each id hasnt been processed before. 
        processed_data = load_processed_data()
        if id in processed_data:
            return
        # If it hasnt been processed than do this!
        else:
            print(f"Fetching details for app ID: {id}...")

            app_details = get_app_details(id)

            # Check if the response is valid and if it was successful
            if app_details is None or str(id) not in app_details or not app_details[str(id)]['success']:
                print(f"Failed to get details for app ID: {id}")
                # return None if its bad data
                return None
            # Getting data 
            data = app_details[str(id)]['data']
            type = data.get('type', 'N/A')
            required_age = data.get('required_age', 'N/A')
            is_free = data.get('is_free', 'N/A')
            title = data.get('name', 'N/A')
            release_date = data.get('release_date', {}).get('date', 'N/A')
            final_price = data.get('price_overview', {}).get('final_formatted', 'Free')
            discount_percentage = data.get('price_overview', {}).get('discount_percent', '0')
            genre = ', '.join(data.get('genres', [{}])[0].get('description', 'N/A') for _ in data.get('genres', []))
            developer = ', '.join(data.get('developers', 'N/A'))
            publisher = ', '.join(data.get('publishers', 'N/A'))
            description = data.get('short_description', 'N/A')
            platforms = data.get('platforms', 'N/A')
            # Collect all data into a dictionary
            game_data = {
                'id': id,
                'type' : type,
                'required_age': required_age,
                'is_free': is_free,
                'title': title,
                'release_date': release_date,
                'price': final_price,
                'discount_percentage': discount_percentage,
                'genre': genre,
                'developer': developer,
                'publisher': publisher,
                'description': description,
                'platforms' : platforms,
            }
            print(f"Collected data for {title}.")
            # adding it to the processed ids
            processed_data.add(id)
            # saving the file of processed ids
            save_processed_data(processed_data)
            return game_data


# WIP
def extract_all_games():
    list = get_app_ids()
    games = []
    if not list:
        return games
    for id in list:
        games.append(extract_game_by_id(id))
        list.remove(id)