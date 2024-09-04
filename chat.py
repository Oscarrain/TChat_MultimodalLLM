# import os
# import openai  # 导入 OpenAI SDK
# from openai import OpenAI
# #openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_base = "http://localhost:8080"
# openai.api_key = os.getenv("OPENAI_API_KEY") or "your_api_key"  # 检查环境变量并设置默认值

# client = OpenAI(api_key=openai.api_key)  # 使用从环境变量获取的 API 密钥


# def chat(messages):
    
#     # 调用语言模型的API
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",  # 替换为你使用的模型
#         messages=messages,
#         stream=True
#     )
#     for line in response:
#         yield line['choices'][0]['message']['content']  # 生成输出

# # openai.api_key = "your_api_key"  # 替换为你的 API 密钥

# # def chat(messages):
# #        # 调用 Chat Completions API
# #     response = openai.ChatCompletion.create(
# #         model="gpt-4o-mini",  # 使用你选择的模型
# #         messages=messages,
# #         stream=True  # 如果需要逐步返回结果，可以设置为 True
# #     )
       
# #        # 处理响应
# #     for choice in response.choices:
# #         yield choice.message.content  # 提取助手的回复内容

import os
import requests  # 导入 requests 库
import json
# from openai import OpenAI  # 移除 OpenAI 导入

# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_base = "http://localhost:8080"  # 移除 OpenAI API 基础 URL

# client = OpenAI(api_key=openai.api_key)  # 移除 OpenAI 客户端初始化

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
                    #print(data)
                    if 'choices' in data and data['choices'][0]['delta']['content'] is not None:  # 检查内容
                        yield data['choices'][0]['delta']['content']  # 生成输出
                except json.JSONDecodeError as e:
                    #print(f"JSON 解码错误: {e}，chunk 内容: {chunk}")  # 输出错误信息和 chunk 内容
                    pass  # 忽略 JSON 解码错误
    else:
        yield "Error: Failed to get response"  # 请求失败，返回错误信息