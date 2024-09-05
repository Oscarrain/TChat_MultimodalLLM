import os
import requests


def image_generate(content: str):
    # OpenAI API 的 URL
    url = "http://localhost:8080/v1/images/generations"

    # 发送 POST 请求
    response = requests.post(url, json={
        "prompt": content,
        "size": "256x256"
    }, timeout=200)

    # 检查响应是否成功
    if response.status_code == 200:
        # 解析响应内容，获取图片的 URL
        image_url = response.json()["data"][0]["url"]
        return image_url
    else:
        # 请求失败，返回错误信息
        return "Error: Failed to generate image"


if __name__ == "__main__":
    image_generate('A woman with a red umbrella walking in the rain')
