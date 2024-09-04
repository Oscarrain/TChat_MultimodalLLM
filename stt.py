import requests

def audio2text(file_path):
    # Check if the file is a WAV file
    if not file_path.lower().endswith('.wav'):
        raise ValueError("Only WAV files are supported.")

    url = "http://localhost:8080/v1/audio/transcriptions"  # LocalAI's transcription endpoint
    model_name = "whisper-1"

    try:
        # 直接从传入的文件路径读取文件
        with open(file_path, "rb") as audio_file:
            files = {
                "file": (file_path, audio_file, "audio/wav"),
                "model": (None, model_name)
            }

            # Note: No need to manually set 'Content-Type' header, requests will handle it
            response = requests.post(url, files=files)

        if response.status_code == 200:
            content = response.json().get("text", "")  # Get text from the response
            return content
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        raise RuntimeError(f"Failed to process the file: {str(e)}")


if __name__ == "__main__":
    try:
        text = audio2text(r'C:/Users/zhang/Desktop/tsinghua/大二下/后端/AI_assistant/ai-assistant-2024/sun-wukong.wav')

        #print("Transcribed text:", text)
    except Exception as e:
        print("Error:", e)
