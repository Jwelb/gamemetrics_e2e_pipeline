import requests
import json
import time

def get_app_list():
    """Fetches the list of all Steam apps."""
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
    response = requests.get(url)
    app_list = response.json()
    return app_list['applist']['apps']

def get_app_details(app_id):
    """Fetches details for a specific app using its app ID."""
    url = f'http://store.steampowered.com/api/appdetails?appids={app_id}'
    response = requests.get(url)
    return response.json()

def main():
    # Step 1: Get the list of apps
    print("Fetching app list...")
    apps = get_app_list()
    
    # Prepare a list to hold the collected game data
    all_games_data = []

    # Example: Get details for each app
    for app in apps:
        app_id = app['appid']
        print(f"Fetching details for app ID: {app_id}...")
        
        app_details = get_app_details(app_id)

        # Check if the response is valid and if it was successful
        if app_details is None or str(app_id) not in app_details or not app_details[str(app_id)]['success']:
            print(f"Failed to get details for app ID: {app_id}")
            continue  # Skip to the next app

        # Proceed to extract game data since the response is valid
        data = app_details[str(app_id)]['data']
        title = data.get('name', 'N/A')
        release_date = data.get('release_date', {}).get('date', 'N/A')
        price = data.get('price_overview', {}).get('final_formatted', 'Free')
        genre = ', '.join(data.get('genres', [{}])[0].get('description', 'N/A') for _ in data.get('genres', []))
        developer = ', '.join(data.get('developers', 'N/A'))
        publisher = ', '.join(data.get('publishers', 'N/A'))
        description = data.get('short_description', 'N/A')
        
        # Collect all data into a dictionary
        game_data = {
            'id': app_id,
            'title': title,
            'release_date': release_date,
            'price': price,
            'genre': genre,
            'developer': developer,
            'publisher': publisher,
            'description': description
        }

        all_games_data.append(game_data)
        print(f"Collected data for {title}.")

        # Respect the API rate limit; add delay to avoid hitting the server too hard
        time.sleep(0.1)  # 100ms delay (adjust as needed)

    # Save or print all game data
    with open('steam_games_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_games_data, f, ensure_ascii=False, indent=4)
    
    print("Data collection complete! Saved to steam_games_data.json")

if __name__ == "__main__":
    main()