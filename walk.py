import googlemaps
from random import random
from math import pi, sin, cos
from datetime import datetime

WALKING_SPEED = 3.9
LAT_TO_KM = 110.574
def LNG_TO_KM(lng): return 111.320 * cos(pi * lng / 180)


def main(address: str, KEY: str, mins: int):
    gmaps = googlemaps.Client(key=KEY)
    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    location = geocode_result[0]['geometry']['location']
    lat, lng = location['lat'], location['lng']

    # Choice a random angle and add 10kms in that direction
    theta = random() * 2 * pi
    # assume walking speed
    distance = WALKING_SPEED * mins / 60 / 2  # factor of 2 due to return trip
    x, y = sin(theta) * distance, cos(theta) * distance
    new_lat = lat + x / LAT_TO_KM
    new_lng = lng + y / LNG_TO_KM(lng)

    reverse_geocode_result = gmaps.reverse_geocode((new_lat, new_lng))
    target_address = reverse_geocode_result[0]['formatted_address']

    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions(address,
                                         target_address,
                                         mode="walking",
                                         departure_time=now)
    trip_dist = directions_result[0]['legs'][0]['distance']['value']
    trip_dura = directions_result[0]['legs'][0]['duration']['value']
    print('''destination: {}
distance: {:.1f} kms each way
duration: {:.0f} mins each way'''
          .format(target_address, trip_dist/1e3, trip_dura/60))


if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('address', type=str, help="Your starting point")
    parser.add_argument('--key', type=str, help="YOUR API KEY")
    parser.add_argument('--mins', type=int,
                        help="How long you want to walk", default=60)
    args = parser.parse_args()
    main(args.address, args.key, args.mins)
