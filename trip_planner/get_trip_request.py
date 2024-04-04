import yaml

from trip_planner.ping_azure_gpt import ping_azure_gpt
from trip_planner.prompts import get_trip_request_prompt
from trip_planner.schemas import TripRequest
from trip_planner.tools import get_tools, parse_response, save_tool


def get_trip_request(trip_query: str) -> TripRequest:
    tool_name = "trip_request"
    tools, tool_choice = get_tools(tool_name)
    prompt = get_trip_request_prompt(trip_query)
    trip_request_raw = ping_azure_gpt(prompt, tools=tools, tool_choice=tool_choice)
    trip_request = parse_response(trip_request_raw, TripRequest)
    save_tool(trip_request, tool_name)
    return trip_request
