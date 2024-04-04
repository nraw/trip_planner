import yaml


def get_trip_request_prompt(trip_query):
    prompt = f"""You are a travel assistant.
I will share with you a request for a trip.
You will extract the relevant information.
Try to break down the details into small pieces of information.

Prompt request:
---
{trip_query}
---
    """
    return prompt


def get_broad_recommendations_prompt(trip_request):
    prompt = f"""You are a travel assistant.
I will share with you the rough details of a trip.
You will provide broad recommendations for the trip.
Focus on the sights to see, trips to make, activities to do, food to try, and events that might be worth checking out.
Provide a list of options for each category together with a brief description.
Try to provide a vast variety of options.
Be concise with each option.
Ask for more details if needed.
Ask the most important questions regarding choosing which options to undertake.

Trip details:
---
{yaml.dump(trip_request.dict())}
---
"""
    return prompt


def get_draft_plan_prompt(trip_request, broad_recommendations):
    prompt = f"""You are a travel assistant.
I will share with you a request for a trip and some recommendations that could interest me.
You will propose a draft plan for the trip.
Focus on proposing overarching segments of the trip instead of exact daily plans.
Propose alternative overarching plans or constructive ways in which the plan could be changed.
Be concise.
Ask for more details if needed.
If I confirm the plan, you will summarize the plan.

Trip request:
---
{yaml.dump(trip_request.dict())}
---

Broad recommendations:
---
{yaml.dump(broad_recommendations.dict())}
---
"""
    return prompt


def get_agenda_prompt(trip_request, plan):
    prompt = f"""You are a travel assistant.
I will share with you a request for a trip and a draft plan agreed with the user.
You will propose a detailed agenda for the trip.

Trip request:
---
{yaml.dump(trip_request.dict())}
---

Draft plan:
---
{plan}
---
"""
    return prompt
