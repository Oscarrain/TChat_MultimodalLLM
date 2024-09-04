import requests
from bs4 import BeautifulSoup


def fetch(url: str):
    # Step 1: 拉取网页内容
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {response.status_code}")

    # Step 2: 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: 提取main类下的第一个 <p> 标签中的文字，一般为重要信息
    main_element = soup.select_one('main')
    if main_element:
        paragraphs = main_element.find_all('p')
        if paragraphs:
            processed_result = paragraphs[0].get_text()
        else:
            processed_result = "No <p> tag found under .main class."
    else:
        processed_result = "No element with .main class found."

    # Step 4: 生成有效的提问
    question = f"Act as a summarizer. Please summarize {url}. The following is the content:\n\n{processed_result}"

    return question


if __name__ == "__main__":
    url = "https://dev.qweather.com/en/help"
    question = fetch(url)
    print(question)
