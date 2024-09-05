import requests  # 导入 requests 库
import json


def chat(messages):
    url = "http://localhost:8080/v1/chat/completions"  # 更新为聊天 API 的 URL
    payload = {
        "model": "gpt-3.5-turbo",  # 使用的模型
        "messages": messages,  # 传入的消息
        "temperature": 0.7, # 温度设置
        "stream": True  # 设置为流式输出
    }
    response = requests.post(url, json=payload,stream=True)  # 发送 POST 请求

    if response.status_code == 200:  # 检查响应是否成功
        for chunk in response.iter_lines():  # 逐行处理响应
            if chunk and chunk.strip():  # 确保 chunk 不为空
                chunk = chunk.decode('utf-8').lstrip('data: ').strip()  # 解码并去掉前缀
                if chunk == "[DONE]":  # 检查是否是完成标记
                    break  # 结束处理
                if chunk.startswith('{') and chunk.endswith('}'):  # 检查是否是有效的 JSON
                    try:
                        data = json.loads(chunk)  # 解析 JSON 数据
                        if 'choices' in data and data['choices'][0]['delta']['content']:  # 检查内容是否非空
                            yield data['choices'][0]['delta']['content']  # 生成输出
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}, chunk: {chunk}")  # 打印错误信息和无效的 chunk
    else:
        yield "Error: Failed to get response"  # 请求失败，返回错误信息