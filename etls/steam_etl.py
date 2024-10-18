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


# Tested and Done!
def get_app_ids():
    """Fetches the list of all Steam apps."""
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
    response = requests.get(url)
    app_list = response.json()
    apps = app_list['applist']['apps']
    ids = []
    for app in apps:
        ids.append(app['appid'])
    return ids
        
        

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
            print(f'Processed {id} Already! Sorry Try another')
            return {}
        # If it hasnt been processed than do this!
        else:
            print(f"Fetching details for app ID: {id}...")

            app_details = get_app_details(id)

            # Check if the response is valid and if it was successful
            if app_details is None or str(id) not in app_details or not app_details[str(id)]['success']:
                print(f"Failed to get details for app ID: {id}")
                # return None if its bad data
                return {}
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

# extracts all games
def extract_all_games():
    list = get_app_ids()
    games = []
    for id in list:
        games.append(extract_game_by_id(id))
    return games

def transform_data(games_df: pd.DataFrame):
    original_shape = games_df.shape[0]
    games_df = games_df.dropna(how='all')
    dropped_rows = original_shape - games_df.shape[0]
    if dropped_rows > 0:
        print(f"Dropped {dropped_rows} rows due to failed or duplicate rows.")
    # do more transformations
    return games_df


# This function gets the parameter and just pushes the results to the azure storage account
# def load_to_azure():
    
def load_data_to_csv(data: pd.DataFrame):
    data.to_csv("TestExample1.csv")

def test():
    exampleList = [2129810, 2335800, 986010, 2097170, 3155230, 3213430, 3282810, 585420, 1948280, 3231920, 1116170, 3045050, 2255370, 941460, 1520470, 553780, 308600, 1459630, 2319940, 2139460, 2334700, 2399420, 2999030, 258550, 1851350, 3018090, 3271040, 2266650, 3198990, 2082570, 1892930, 3277500, 3061690, 322330, 3199170, 1273100, 3190970, 1771300, 2902720, 1138640, 2400840, 1208170, 2990080, 2980550, 2000890, 2587840, 2052040, 3270630, 3180930, 949230, 1128860, 1428090, 108600, 1999520, 3186690, 1121560, 1127660, 1185810, 1325730, 1503170, 1645220, 1790600, 1800860, 1803450, 1818450, 1962700, 1969650, 1997470, 2088250, 2103140, 2287960, 2407270, 2420660, 2421350, 2543180, 2585830, 2622000, 2708950, 3103040, 3123410, 3180170, 3226570, 3235910, 3256070, 3271530, 1049320, 499180, 581320, 787480, 991270, 1254320, 2654540, 3027940, 3037030, 3054770, 3059840, 3060080, 3101770, 3137120, 3138330, 3142540, 3163250, 3169100, 3170420, 3170430, 3206520, 3027620, 2633080, 1816140, 3141870, 1108740, 1135960, 1339340, 3108720, 3261060, 792200, 809090, 874450, 972200, 3288690, 2307350, 3192760, 451340, 3187730, 3088430, 218230, 294770, 39660, 774941, 589290, 2543510, 3263740, 1116390, 1200770, 1326030, 1603640, 2051010, 2108330, 2116120, 2184350, 2305760, 2395260, 2500160, 2529080, 2570210, 2576020, 2582560, 2716120, 2716820, 2719030, 2803360, 3207390, 538030, 1170950, 1217490, 1264171, 1270010, 1351370, 1392390, 1437840, 1474930, 1480050, 1513420, 1682600, 1832840, 1840800, 3012290, 3080030, 3226270, 2191410, 1653190, 3280460, 1211980, 1424230, 1584090, 1607250, 1786790, 1830190, 1905180, 1911610, 2015620, 2064650, 2075100, 2114740, 2236060, 2316930, 2341070, 2359660, 2401970, 2566880, 2645820, 2658770, 2751000, 2807150, 2990190, 3051280, 3080680, 3084620, 3156770, 3192310, 3217200, 3227820, 3231380, 3283090, 3292980, 1000050, 1213700, 1245560, 1272320, 1375630, 1418750, 1554770, 17510, 372080, 689760, 2399830, 3104680, 1282270, 2084360, 3050, 2488620, 416000, 2384580, 3023930, 3254600, 1324780, 1395520, 2635410, 3061810, 1592190, 3256520, 1696810, 2666580, 3190930, 714010, 2407830, 3173890, 3204560, 1845940, 2169200, 2315070, 2624670, 2875110, 2485550, 2678080, 2730540, 2678640, 3254100, 3248450, 1702010, 2863340, 2367610, 2605790, 3234420, 2386720, 238430, 407530, 2510960, 2819550, 3101950, 1371980, 3020620, 1452250, 2710980, 3249720, 2524700, 2796980, 2192020, 512900, 3268100, 2686820, 1154670, 3071520, 2725560, 3261860, 3057460, 3199180, 1359270, 285049]
    games = []
    for id in exampleList:
        # This in theory would save all the ids in the processed_ids file but also check if the id has already been processed
        games.append(extract_game_by_id(id))
    return games




extract_test= test()
extract_df = pd.DataFrame(extract_test)
transform_test = transform_data(extract_df)
print(transform_test)
load_data_to_csv(transform_test)