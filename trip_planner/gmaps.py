import os
import urllib
import webbrowser

from googlemaps import Client

from trip_planner.schemas import BroadRecommendations


def make_gmaps_url(broad_recommendations: BroadRecommendations):
    sights_to_see = broad_recommendations.sights_to_see
    url = "https://www.google.com/maps/dir/?api=1"
    url += f"&origin={sights_to_see[0]}"
    url += f"&destination={sights_to_see[-1]}"
    remaining = sights_to_see[1:-1]
    waypoints = "|".join(remaining)
    url += f"&waypoints={waypoints}"
    webbrowser.open(url)
    encoded_url = urllib.parse.quote(url, safe=":/?&=")
    return url


def get_place_id(location):
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    client = Client(GOOGLE_MAPS_API_KEY)
    place_result = client.geocode(location)
    if place_result and len(place_result["candidates"]):
        place_id = place_result[0]["place_id"]
    else:
        place_id = None
    return place_id


def test_get_place_id(broad_recommendations: BroadRecommendations):
    location = broad_recommendations.sights_to_see[0]
    place_id = get_place_id(location)

    print(f"Place ID for {location}: {place_id}")
