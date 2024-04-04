from trip_planner.ping_azure_gpt import ping_azure_gpt
from trip_planner.prompts import get_draft_plan_prompt


def get_plan(trip_request, broad_recommendations):
    prompt = get_draft_plan_prompt(trip_request, broad_recommendations)
    first_plan = ping_azure_gpt(prompt)
    plan = back_and_forth_planning(prompt, first_plan)
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
