import yaml

from trip_planner.ping_azure_gpt import ping_azure_gpt
from trip_planner.prompts import get_agenda_prompt, get_draft_plan_prompt
from trip_planner.schemas import TripAgenda
from trip_planner.tools import get_tools, parse_response, save_tool


def get_agenda(trip_request, plan):
    tool_name = "agenda"
    prompt = count_days_prompt(trip_request)
    prompt = get_agenda_prompt(trip_request, plan)
    tools, tool_choice = get_tools(tool_name)
    agenda_raw = ping_azure_gpt(prompt, tools=tools, tool_choice=tool_choice)
    agenda = parse_response(agenda_raw, TripAgenda)
    save_tool(agenda, tool_name)

    return plan


def back_and_forth_planning(prompt, first_plan):
    done = False
    messages = [
        {"role": "system", "content": prompt},
        {"role": "assistant", "content": first_plan},
    ]
    plan = first_plan
    print(plan)
    while not done:
        user_response = input("> ")
        if user_response == "done":
            done = True
        else:
            messages.append({"role": "user", "content": user_response})
            plan = ping_azure_gpt(messages)
            print(plan)
            messages.append({"role": "assistant", "content": plan})

    return plan
