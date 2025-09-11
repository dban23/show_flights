from dotenv import load_dotenv
import requests
import json
import os
from geopy.geocoders import Nominatim
import math


def addr_to_latlon():
    addr = input("Your current address: ")

    geolocator = Nominatim(user_agent="show_flight")
    location = geolocator.geocode(addr)

    lat = location.latitude
    lon = location.longitude

    #print(f"Latitude: {lat}\nLongitude: {lon}")
    return lat, lon


def define_square():
    lat, lon = addr_to_latlon()

    # I need to make a square of 2km x 2km around the current location
    # 1 km from some point transformed to longitute depends on the latitude
    latrad = math.radians(lat)
    lonkm = (111.32/2*math.cos(latrad))**-1

    minlat = lat - 0.00898*2
    maxlat = lat + 0.00898*2
    minlon = lon - lonkm
    maxlon = lon + lonkm

    return f"{minlat} {minlon} {maxlat} {maxlon}"


def get_flight():
    load_dotenv()
    apiKey = os.getenv("FLIGHTAWARE_API_KEY")
    apiUrl = "https://aeroapi.flightaware.com/aeroapi/flights/search"
    
    #minlat = 45.695
    #maxlat = 45.72093
    #minlon = 15.988
    #maxlon = 16.03191
    
    latlong = define_square()

    auth_header = {'x-apikey':apiKey}
    payload = {
       "query": f'-latlong "{latlong}"'
       #"query": '-latlong "45.68 15.8 45.9 16.1"'
    }

    response = requests.get(apiUrl, headers=auth_header, params=payload)
    code = response.status_code
    resp_json = response.json()
    
    flights = resp_json["flights"]
    #flights = json.dumps(flights_bef, indent=4, ensure_ascii=False)

    if code == 200:
        if flights == []:
            print("Can't detect any flights around.")
        else:
            for flight in flights:
                flight_number = flight["ident"]
                from_name = flight["origin"]["name"]
                from_city = flight["origin"]["city"]
                to = flight["destination"]["name"]
                to_city = flight["destination"]["city"]
                print(f"Flight number {flight_number} from {from_name}, {from_city} to {to}, {to_city}.")
    else:
        print(f"Error executing request: {code}")


get_flight()
