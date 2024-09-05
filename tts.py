
import requests
import os
import json

def text2audio(content: str)->str:
    """
    Converts text to audio using LocalAI TTS API and returns the path to the audio file.
    
    Args:
    - content (str): The text content to be converted to audio.

    Returns:
    - str: The path to the saved audio file.
    """
    url = "http://localhost:8080/tts" # LocalAI's TTS endpoint
    headers = {"Content-Type": "application/json"}
    data = {"model": "en-us-blizzard_lessac-medium.onnx", "input": content}
    data_json = json.dumps(data)
    # 获取已有的音频文件数量
    audio_folder = "LocalAI/generated/audio"
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
    existing_audio_files = [f for f in os.listdir(audio_folder) if f.startswith("response") and f.endswith(".wav")]
    audio_count = len(existing_audio_files)

    # 生成新的文件名
    audio_file_name = f"response{audio_count + 1}.wav"
    audio_file_path = os.path.join(audio_folder, audio_file_name)
    response = requests.post(url, headers=headers, data=data_json)
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(response.content)
    #print(response.content)
    #print("音频文件已生成")
    return audio_file_path

    

if __name__ == "__main__":
    text2audio("Sun Wukong (also known as the Great Sage of Qi Tian, Sun Xing Shi, and Dou Sheng Fu) is one of the main characters in the classical Chinese novel Journey to the West")