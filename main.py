from dotenv import load_dotenv
import requests
import json
import os

def get_flight():
    load_dotenv()
    apiKey = os.getenv("FLIGHTAWARE_API_KEY")
    apiUrl = "https://aeroapi.flightaware.com/aeroapi/flights/search"
    
    auth_header = {'x-apikey':apiKey}
    payload = {
       "query": '-latlong "45.695 15.988 45.72093 16.03191"'
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
