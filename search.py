import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch


def search(content: str):
    api_key = "ffbcca4c0f75e7e54a673872ab4b05b8cca05dfd7f49e241b3c5291b6793765c"
    search_url = "https://serpapi.com/search"

    params = {
        "q": content,
        "api_key": api_key,
        "engine": "bing"
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    # 获取第一条搜索结果的snippet
    search_results = data.get("organic_results", [{}])[0].get("snippet", "No results found.")

    # 组合内容
    # combined_content = f"Please answer '{content}' based on the search result:\n\n{search_results}"

    return search_results


if __name__ == "__main__":
    search("Sun Wukong")