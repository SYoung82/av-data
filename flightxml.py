import requests
import apisecrets as API

KEY = API.API_PASSWORD
USERNAME = API.API_USERNAME
URI = API.API_URI


def get_airport_wx(airport_code):
    payload = {
        'airport_code': airport_code,
        'howMany': '1',
        'offset': '0'
    }
    print(payload)
    response = requests.get(URI + "WeatherConditions", params=payload, auth=(USERNAME, KEY))
    print(response.text)

    if response.status_code == 200:
        return response.json()
    else:
        return "There was an error retrieving the data from the server. {}".format(response.status_code)


def get_enroute_aircraft(airport_code):
    payload = {
        'airport_code': airport_code,
        'type': 'enroute'
    }

    if response.status_code == 200:
        return response.json()
    else:
        return "There was an error retrieving the data from the server. {}".format(response.status_code)