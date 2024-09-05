import requests  # 导入 requests 库
import json

def chat(messages):
    url = "http://166.111.80.101:8080/v1/chat/completions"  # 更新为聊天 API 的 URL
    payload = {
        "model": "gpt-3.5-turbo",  # 使用的模型
        "messages": messages,  # 传入的消息
        "temperature": 0.7, # 温度设置
        "stream": True  # 设置为流式输出
    }
    response = requests.post(url, json=payload,stream=True)  # 发送 POST 请求

    if response.status_code == 200:  # 检查响应是否成功
        for chunk in response.iter_lines():  # 逐行处理响应
            if chunk:  # 确保 chunk 不为空
                try:
                    json_chunk = chunk.decode('utf-8').lstrip('data: ')
                    data = json.loads(json_chunk)  # 解析 JSON 数据
                    if 'choices' in data and data['choices'][0]['delta']['content'] is not None:  # 检查内容
                        yield data['choices'][0]['delta']['content']  # 生成输出
                except json.JSONDecodeError as e:
                    pass
    else:
        yield "Error: Failed to get response"  # 请求失败，返回错误信息