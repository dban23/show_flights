from dotenv import load_dotenv
import requests

# import json
import os
from geopy.geocoders import Nominatim
import math

load_dotenv()


class Flight_locator:
    def __init__(self, address):
        self.address = address

    def addr_to_latlon(self):
        # addr = input("Your current address: ")

        geolocator = Nominatim(user_agent="show_flight")
        location = geolocator.geocode(self.address)

        if location is None:
            return 999, 999

        lat = location.latitude
        lon = location.longitude

        # print(f"Latitude: {lat}\nLongitude: {lon}")
        return lat, lon

    def define_square(self):
        lat, lon = self.addr_to_latlon()

        if lat == 999 and lon == 999:
            return None

        # I need to make a square of 2km x 2km around the current location
        # 1 km from some point transformed to longitute depends on the latitude
        latrad = math.radians(lat)
        lonkm = (111.32 / 2 * math.cos(latrad)) ** -1

        minlat = lat - 0.00898 * 2
        maxlat = lat + 0.00898 * 2
        minlon = lon - lonkm
        maxlon = lon + lonkm

        return f"{minlat} {minlon} {maxlat} {maxlon}"

    def get_flight(self):
        apiKey = os.getenv("FLIGHTAWARE_API_KEY")
        apiUrl = "https://aeroapi.flightaware.com/aeroapi/flights/search"

        latlong = self.define_square()

        if latlong is None:
            return "Location not found."
        else:
            auth_header = {"x-apikey": apiKey}
            payload = {"query": f'-latlong "{latlong}"'}

            response = requests.get(apiUrl, headers=auth_header, params=payload)
            code = response.status_code
            resp_json = response.json()

            flights = resp_json["flights"]
            # flights = json.dumps(flights_bef, indent=4, ensure_ascii=False)

            if code == 200:
                if flights == []:
                    return "Can't detect any flights around."
                else:
                    output = ""
                    for flight in flights:
                        if flight["ident"] == "null":
                            flight_number = "Unknown"
                        else:
                            flight_number = flight["ident"]

                        if flight["origin"]["name"] == "null":
                            from_name = "Unknown"
                        else:
                            from_name = flight["origin"]["name"]

                        if flight["origin"]["city"] == "null":
                            from_city = "Unknown"
                        else:
                            from_city = flight["origin"]["city"]

                        if flight["destination"] == "null":
                            to = "Unknown"
                        else:
                            to = flight["destination"]["name"]

                        if flight["destination"] == "null":
                            to_city = "Unknown"
                        else:
                            to_city = flight["destination"]["city"]

                    output += f"Flight number: {flight_number}\nFrom: {from_name}, {
                        from_city
                    }\nTo: {to}, {to_city}."
                    return output
            else:
                return f"Error executing request: {code}"
