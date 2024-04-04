import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import lru_cache

import openai
import structlog
from tqdm import tqdm

logger = structlog.get_logger()


def ping_azure_parallel(prompts):
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(
            tqdm(
                executor.map(ping_azure_gpt, prompts),
                total=len(prompts),
            )
        )
    return results


def ping_azure_gpt(prompt, model_name=None, tools=None, tool_choice=None):
    if not model_name:
        model_name = os.environ.get("OPENAI_MODEL", "gpt-4")
    tool_choice = "none" if not tool_choice else tool_choice
    client = instantiate_openai()
    messages = get_messages(prompt)
    if not messages:
        return ""
    attempt = 1
    response = None
    while attempt <= 15 and not response:
        try:
            if tools is None:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                )
            else:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    tools=tools,
                    tool_choice=tool_choice,
                    #  response_format={"type": "json_object"},
                )
        except openai.BadRequestError as e:
            model_name = "gpt-4-32k"
            logger.error(
                f"Didn't manage to get stuff, changing model to {model_name}. {attempt=}. {e}"
            )
        except Exception as e:
            logger.error(f"Failed to obtain data from openai. {attempt=}. {e}")
            time.sleep(attempt * 10)

            attempt += 1

    answer = parse_res(response)
    log_cost(response)
    log_prompt(prompt, response)
    return answer


def get_messages(prompt):
    if type(prompt) == str:
        messages = [{"role": "system", "content": prompt}]
    elif type(prompt) == list:
        messages = prompt
    else:
        return []
    return messages


def instantiate_openai():
    base_url = os.getenv("OPENAI_BASE_URL", "")
    api_version = os.getenv("OPENAI_API_VERSION", "2023-10-01-preview")
    # "2023-07-01-preview" "2023-10-01-preview" "2023-07-01-preview"
    #  openai.api_version = os.getenv("OPENAI_API_VERSION", "2023-05-15")
    api_key = os.getenv("OPENAI_API_KEY", "")

    client = openai.AzureOpenAI(
        api_key=api_key, azure_endpoint=base_url, api_version=api_version
    )
    return client


def get_json_data(model_name, prompt, max_tokens=400):
    #  if model_name in ["gpt-35-turbo", "gpt-4", "gpt-4-32k"]:
    json_data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        #  "max_tokens": conf["answer_max_tokens"],
    }
    #  else:
    #      json_data = {
    #          "model": model_name,
    #          "prompt": prompt,
    #          "temperature": 0,
    #          "max_tokens": max_tokens,
    #      }
    return json_data


def parse_res(res):
    choices = res.choices
    if not choices:
        logger.error(f"Failed to parse response: {res}")
        return ""
    message = choices[0].message
    if not message:
        logger.error(f"Failed to parse response: {res}")
        return ""
    answer = message.content
    if message.tool_calls:
        answer = message.tool_calls[0].function.arguments
    return answer


def log_cost(response):
    model_name = response.model
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    now = datetime.now().isoformat()
    log_line = f"andrej,{model_name},{now},{prompt_tokens},{completion_tokens}"
    logger.info(log_line)
    os.makedirs("logs", exist_ok=True)
    with open("logs/costs.log", "a") as f:
        f.write(log_line + "\n")


def log_prompt(prompt, response):
    should_log = True
    if should_log:
        response_dict = response.dict()
        response_dict["prompt"] = prompt
        now = datetime.now().isoformat()
        os.makedirs("data/prompt_logs", exist_ok=True)
        with open(f"data/prompt_logs/{now}.json", "w") as f:
            json.dump(response_dict, f)
