from main import *


def test_main():
    trip_query = "I am going to spend 6 days in Korea from 26 March 2024 until 1 April starting in Seoul and leaving from Seoul. Some tips we received: Changing of the royal guard, Bukchon Hanok Village, Jjimjilbang and tea houses. Then maybe trips to busan and jinhae gunhangje festival or nami island, suwon, everland park, seoraksan national park. Feel free to recommend more."

    trip_query = """We are going to Australia from 17 March 8 AM until 26 March 11:45 AM.
We are landing in Brisbane.
We were also considering making a trip to Sydney, but we need to be back in Brisbane on the 23 March. There are friends that are leaving from Sydney on the 19 March towards Brisbane by car, so if possible we would like to join them.
We would like to visit the Great Barrier Reef. """

    trip_query = """We are travelling to Korea and landing there at 10:40 at the Incheon airport after a night flight. We are leaving Korea the next day at 21:50 from Incheon airport. We want to make the most of our time there. Make a plan for us."""
    main(trip_query)
