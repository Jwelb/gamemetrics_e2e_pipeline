import requests

def main():
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
    response = requests.get(url)
    app_list = response.json()
    app_list = app_list['applist']['apps']
    list = []
    for app in app_list:
        appid = app['appid']
        list.append(appid)
    return list


main()