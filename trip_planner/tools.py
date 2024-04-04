import json

import yaml

from trip_planner.schemas import BroadRecommendations, TripAgenda, TripRequest
import structlog

logger = structlog.get_logger()

all_tools = {
    "trip_request": {
        "description": "Extract relevant information from a trip request",
        "schema": TripRequest,
    },
    "broad_recommendations": {
        "description": "Provide broad recommendations for a trip",
        "schema": BroadRecommendations,
    },
    "agenda": {
        "description": "Generate an agenda for a trip",
        "schema": TripAgenda,
    },
}


def get_tools(tool_name):
    tool = all_tools[tool_name]
    tools = [
        {
            "type": "function",
            "function": {
                "description": tool["description"],
                "name": tool_name,
                "parameters": tool["schema"].schema(),
            },
        }
    ]
    tool_choice = {"type": "function", "function": {"name": tool_name}}
    return tools, tool_choice


def parse_response(response, ResponseModel):
    parsed_response = ResponseModel(**json.loads(response))
    return parsed_response


def save_tool(tool, tool_name):
    filename = f"data/{tool_name}.yaml"
    yaml.dump(tool.dict(), open(filename, "w"), sort_keys=False)
    logger.info(f"Saved {tool_name}", filename=filename)


def reload(tool_name):
    schema = all_tools[tool_name]["schema"]
    filename = f"data/{tool_name}.yaml"
    data = yaml.safe_load(open(filename, "r"))
    tool = schema(**data)
    return tool
