import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    print('')
    acct = input('Enter Twitter Account:')
    if (len(acct) < 1): break
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '50'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    locations_list = []
    
    if len(js['users']) > 0:
        for i in range(50):
            if js['users'][i]['location'] != "":
                locations_list.append(js['users'][i]['location'])

        map1 = folium.Map()
        for loc in locations_list:
            geolocator = Nominatim(user_agent="Task_3_main_Bubniak.py")
            reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)
            location = geolocator.geocode(loc)
            try:
                folium.Marker([location.latitude, location.longitude], popup=js['users'][locations_list.index(loc)]['screen_name']).add_to(map1)
            except AttributeError:
                continue
        map1.save('twitter_map.html')
        break
    else:
        print("This person doesn't have any friends :(")
        break
