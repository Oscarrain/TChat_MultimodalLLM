import os
import requests
from typing import List, Dict
import json
from openai import OpenAI


to_do_list = ""

def lookup_location_id(location: str)->str:
    """
    Looks up the location ID for a given location name.
    """

    # Set the parameters for the API call
    url = "https://geoapi.qweather.com/v2/city/lookup"
    params = {
        'location': location,
        'key': '39c952c3626e4c86983f1a6595e4803b'
    }
    # Call the weather API
    response = requests.get(url, params=params)

    # Parse the response then return the location ID
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

    # Look up the location ID
    id = lookup_location_id(location)
    if id is None:
        return "Failed to get location information."
    
    # Set the parameters for the API call
    url = "https://devapi.qweather.com/v7/weather/now"
    params = {
        'location': id,
        'key': '39c952c3626e4c86983f1a6595e4803b'
    }

    # Call the weather API
    response = requests.get(url, params=params)

    # Parse the response then return the weather information
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
    # Use the global variable to store the todo list
    global to_do_list

    # Append the todo item to the todo list
    if to_do_list == "":
        to_do_list += f"- {todo}"
    else:
        to_do_list +=f"\n- {todo}"
    return to_do_list

def function_calling(messages: List[Dict])->str:
    """
    Processes the messages and calls the appropriate function using OpenAI's GPT model to determine which function to call.
    """

    # Define the functions that can be called
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "A city, province or counrty,or none. e.g. ShangHai, Beijing, China, US. No form of \"Shanghai, China\"",
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "add_todo",
            "description": "Add something on a TODO-list. Add a todo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo": {
                        "type": "string",
                        "description": "something added to the TODO-list, e.g. walk, swim",
                    }
                },
                "required": ["todo"],
            },
        }
    ]

    # Create an OpenAI client
    client = OpenAI(
        api_key="test",
        # base_url="http://localhost:8080/v1/",
        base_url= "http://166.111.80.101:8080/v1/",
    )



    try:
        # Call the completions API to get the function call
        response = client.chat.completions.create(
            messages=messages,
            functions=functions,
            tool_choice ="auto",
            model="ggml-openllama.bin",
        )
        
        # Parse the function call from the model response
        func = response.choices[0].message.function_call
        if func:
            if func.name == "add_todo":
                todo = json.loads(func.arguments)["todo"]
                return add_todo(todo)
            elif func.name == "get_current_weather":
                location = json.loads(func.arguments)["location"]
                return get_current_weather(location)
            else:
                return "Function not recognized."
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