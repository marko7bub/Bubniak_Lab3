import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

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
                        {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    headers = dict(connection.getheaders())
    friend_list = []
    try:
        for i in range(5):
            friend_list.append(js['users'][i]['name'])
    except IndexError:
        print("This person doesn't have any friends :(")
        break
    print('Congratulations! We created a .json file of 5 most recent friends of ' + acct + '.')
    print('Choose which friend you want to view:', friend_list[0], ',', friend_list[1], ',', friend_list[2], ',', friend_list[3], ',', friend_list[4])
    while True:
        name = input('Enter name: ')
        if name in friend_list:
            break
        else:
            print('Wrong name, enter the name from the list!')
    account_dict = js['users'][friend_list.index(name)]
    print('Great!')
    print('Now choose which information about the account you want to view by choosing one of the following keys:', account_dict.keys())
    while True:
        key = input('Choose a key: ')
        if key in account_dict.keys():
            break
        else:
            print('Wrong key, enter the key from the list!')
    print(account_dict[key])
    break
