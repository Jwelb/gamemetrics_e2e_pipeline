import requests
import json
import time
import pandas as pd

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
        return game_data



def extract_all_games():
     list = get_app_ids()
     games = []
     if list is 0:
          return games
    for id in list:
        games.append(extract_game_by_id(id))
        list.remove(id)