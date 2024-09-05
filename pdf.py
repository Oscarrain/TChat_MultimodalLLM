import os
import re
import requests
import json

def generate_text(prompt):
    # url = "http://166.111.80.101:8080/v1/completions"  # 更新为聊天 API 的 URL
    # payload = {
    #     "model": "gpt-3.5-turbo",
    #     "prompt": prompt,
    #     "temperature": 0,
    #     #"stream": True
    # }

    # response = requests.post(url, json=payload, stream=False)
    # print(response)
    # if response.status_code == 200:  # 检查响应是否成功
    #     for chunk in response.iter_lines():  # 逐行处理响应
    #         if chunk:  # 确保 chunk 不为空
    #             try:
    #                 json_chunk = chunk.decode('utf-8').lstrip('data: ')
    #                 data = json.loads(json_chunk)  # 解析 JSON 数据
    #                 print(data)
    #                 # if 'choices' in data and data['choices'][0]['delta']['content'] is not None:  # 检查内容
    #                 #     return data['choices'][0]['delta']['content']  # 生成输出
    #             except json.JSONDecodeError as e:
    #                 pass
    # else:
    #     return "Error: Failed to get response"  # 请求失败，返回错误信息

    url = "http://localhost:8080/v1/completions"
    payload = {
        'model': "gpt-3.5-turbo",
        'prompt': prompt,
        'temperature': 0.7,
        'stream': True
    }

    try: 
        response = requests.post(url, json=payload, stream=True)

        for chunk in response.iter_lines():
            if chunk and chunk.strip():  # 确保 chunk 不为空
                chunk = chunk.decode('utf-8').lstrip('data: ').strip()  # 解码并去掉前缀
                if chunk == "[DONE]":  # 检查是否是完成标记
                    break  # 结束处理
                if chunk.startswith('{') and chunk.endswith('}'):  # 检查是否是有效的 JSON
                    try:
                        data = json.loads(chunk)  # 解析 JSON 数据
                        if 'choices' in data and data['choices'][0]['text']:  # 检查内容是否非空
                            yield data['choices'][0]['text']  # 生成输出
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}, chunk: {chunk}")  # 打印错误信息和无效的 chunk

        
    
    except Exception as e:
        yield ''

                
    
    
def generate_answer(current_file_text: str, content: str):
    prompt = f"According to the following text: {current_file_text}\nAnswer the following question: {content}"
    #res = generate_text(prompt)
    return prompt


def generate_summary(current_file_text: str):
    prompt = f"Act as a summarizer. Please summarize the following text: {current_file_text}"
    #res = generate_text(prompt)
    return prompt

if __name__ == "__main__":
    prompt = generate_answer("Sun Wukong is a monkey born from a stone who acquires supernatural powers through Taoist practices.", "Who is Sun Wukong?")
    print(prompt)
    prompt = generate_summary("Sun Wukong is a monkey born from a stone who acquires supernatural powers through Taoist practices.")
    #prompt = generate_summary("Sun Wukong is a monkey born from a stone who acquires supernatural powers through Taoist practices.")
    print(prompt)
