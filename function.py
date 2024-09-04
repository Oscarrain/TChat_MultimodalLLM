import os
import requests
from typing import List, Dict
import openai

to_do_list = ""

def lookup_location_id(location: str)->str:
    """
    Looks up the location ID for a given location name.
    """
    url = "https://geoapi.qweather.com/v2/city/lookup"
    params = {
        'location': location,
        'key': '39c952c3626e4c86983f1a6595e4803b'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('code') == '200':
        location_id = data.get('location')[0].get('id')
        return location_id
    else:
        return None

def get_current_weather(location: str)->str:
    """
    Gets the current weather for a given location.
    """
    id = lookup_location_id(location)
    if id is None:
        return "Failed to get location information."
    url = "https://devapi.qweather.com/v7/weather/now"
    params = {
        'location': id,
        'key': '39c952c3626e4c86983f1a6595e4803b'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('code') == '200':
        weather = data.get('now').get('text')
        temperature = data.get('now').get('feelsLike')
        humidity = data.get('now').get('humidity')
        return f"Temperature: {temperature} Description:{weather} Humidity: {humidity}"
    else:
        return "Failed to get weather information."

def add_todo(todo: str)->str:
    """
    Adds a todo item to the todo list.
    """
    todo_list +=f"- {todo}\n"
    return to_do_list

def function_calling(messages: List[Dict])->str:
    """
    Processes the messages and calls the appropriate function using OpenAI's GPT model to determine which function to call.
    """
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "A city, province, or country, e.g., Shanghai, Beijing, China, US. No form of 'Shanghai, China'.",
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "add_todo",
            "description": "Add something to a TODO-list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo": {
                        "type": "string",
                        "description": "An item to be added to the TODO-list, e.g., walk, swim.",
                    }
                },
                "required": ["todo"],
            },
        }
    ]

    openai.api_key = "oscardemo"
    openai.api_base = "http://localhost:8080"
    response = openai.ChatCompletion.create(
        model="ggml-openllama.bin",
        messages=messages,
        functions=functions,
        function_call="auto"
    )

    try:
        # Parse the function call from the model response
        func = response["choices"][0]["message"]["function_call"]
        if func["name"] == "add_todo":
            todo = func["arguments"]["todo"]
            return add_todo(todo)
        elif func["name"] == "get_current_weather":
            location = func["arguments"]["location"]
            return get_current_weather(location)
        else:
            return "Function not recognized."
    except Exception as e:
        return f"Error processing request: {str(e)}"

if __name__ == "__main__":
    messages = [{"role": "user", "content": "What's the weather like in Beijing?"}]
    response = function_calling(messages)
    print(response)

    messages = [{"role": "user", "content": "Add a todo: walk"}]
    response = function_calling(messages)
    print(response)