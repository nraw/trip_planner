from trip_planner.ping_azure_gpt import ping_azure_gpt
from trip_planner.prompts import get_broad_recommendations_prompt
from trip_planner.schemas import BroadRecommendations
from trip_planner.tools import get_tools, parse_response, save_tool


def get_broad_recommendations(trip_request):
    tool_name = "broad_recommendations"
    prompt = get_broad_recommendations_prompt(trip_request)
    broad_recommendations_text = ping_azure_gpt(prompt)
    print(broad_recommendations_text)
    tools, tool_choice = get_tools(tool_name)
    broad_recommendations_raw = ping_azure_gpt(
        broad_recommendations_text, tools=tools, tool_choice=tool_choice
    )
    broad_recommendations = parse_response(
        broad_recommendations_raw, BroadRecommendations
    )
    print(broad_recommendations.dict())
    save_tool(broad_recommendations, tool_name)
    return broad_recommendations, broad_recommendations_text
