import requests

def search(content: str):
    # 定义API密钥
    api_key = "ffbcca4c0f75e7e54a673872ab4b05b8cca05dfd7f49e241b3c5291b6793765c"
    # 定义搜索URL
    search_url = "https://serpapi.com/search"
    params = {
        "q": content,   # 搜索内容
        "api_key": api_key, # API密钥
        "engine": "bing"  # 使用的搜索引擎
    }
    # 发送GET请求
    response = requests.get(search_url, params=params)
    # 解析返回的JSON数据
    data = response.json()
    
    # 获取第一条搜索结果的snippet
    search_results = data.get("organic_results", [{}])[0].get("snippet", "No results found.")

    return search_results

if __name__ == "__main__":
    search("Sun Wukong")