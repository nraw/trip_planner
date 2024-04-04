from trip_planner.get_agenda import get_agenda
from trip_planner.get_broad_recommendations import get_broad_recommendations
from trip_planner.get_plan import get_plan
from trip_planner.get_trip_request import get_trip_request
from trip_planner.tools import reload


def main(trip_query: str):
    trip_request = get_trip_request(trip_query)
    trip_request = reload("trip_request")
    broad_recommendations, broad_recommendations_text = get_broad_recommendations(
        trip_request
    )
    broad_recommendations = reload("broad_recommendations")
    plan = get_plan(trip_request, broad_recommendations)
    agenda = get_agenda(trip_request, plan)
    return agenda
