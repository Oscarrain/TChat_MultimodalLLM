import gradio as gr
import os
import time
from chat import chat  # 导入chat函数
from search import search  # 导入search函数
from mnist import image_classification
from image_generate import image_generate
from stt import audio2text
from fetch import fetch
from tts import text2audio
from function import function_calling
from pdf import generate_answer, generate_summary, generate_text
# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.

messages = []
current_file_text = None
history = []


def add_text(history, text):
    global messages  # 声明使用全局变量
    messages.append({"role": "user", "content": text})  # 更新messages
    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)

def add_file(history, file):
    global messages  # 声明使用全局变量
    global current_file_text
    result = None
    # 直接使用 Gradio 上传的文件路径
    file_path = file.name
    # 修改路径格式，否则无法识别
    file_path = file_path.replace('\\', '/')
    # 检查文件类型
    if file.name.lower().endswith('.wav'):
        try:
            # 调用 audio2text 函数处理音频文件
            text_content = audio2text(file_path)
            messages.append({"role": "user", "content": text_content})
        except Exception as e:
            # 处理 audio2text 函数可能抛出的异常
            print(f"Error processing audio file: {str(e)}")

    elif file.name.lower().endswith('.png'):
        result = image_classification(file.name)
        messages.append({'role': 'user',"content": f"Please classify {file.name}"})

    
    elif file.name.lower().endswith('.txt'):
        try:
            current_file_text = open(file.name).read()
            summary_prompt = generate_summary(current_file_text)
            messages.append({"role": "user", "content": summary_prompt})
        except Exception as e:
            print(f"Error processing text file: {str(e)}")
    
    # 在聊天记录中显示文件名
    history = history + [((file.name,), result)]

    return history

def bot(history):
    global messages  # 声明使用全局变量
    global current_file_text

    user_input = history[-1][0]  # 获取用户输入
    response_generator = None  # 初始化response_generator

    # 检查是否为搜索指令
    if history[-1][1] is None:
        history[-1][1] = ""
    if isinstance(user_input, str) and user_input.startswith("/search "):
        content = user_input[len("/search "):]  # 提取搜索内容
        search_results = search(content)  # 调用search函数
        # 构造新的用户输入
        new_user_input = f"Please answer {content} based on the search result:\n\n{search_results}"
        messages[-1]["content"] = new_user_input  # 添加新的用户输入
        response_generator = chat([messages[-1]])  # 调用chat函数，获取生成器
        for response in response_generator:
            history[-1][1] += response  # 更新history中的助手回复
            time.sleep(0.05)
            yield history  # 每次生成新的history

    elif isinstance(user_input, str) and user_input.startswith("/image "):
        content = user_input[len("/image "):]
        image_path = image_generate(content)  # 调用image_generate函数
        messages.append({"role": "assistant", "content": image_path})  # 记录助手回复的图片路径
        history[-1] = (history[-1][0], (image_path,))  # 在history中更新为图片路径
        yield history

    elif isinstance(user_input, str) and user_input.startswith("/fetch "):
        url = user_input[len("/fetch "):]  # 提取URL
        question = fetch(url)  # 调用fetch函数
        messages[-1]["content"] = question  # 更新messages
        response_generator = chat([messages[-1]])  # 调用chat函数，获取生成器
        for response in response_generator:
            history[-1][1] += response  # 更新history中的助手回复
            time.sleep(0.05)
            yield history  # 每次生成新的history

    elif isinstance(user_input, str) and user_input.startswith("/audio "):
        text = user_input[len("/audio "):]  # 提取URL
        audio_path = text2audio(text)  # 调用text2audio函数
        messages.append({"role": "assistant", "content": audio_path})  # 记录助手回复的音频路径
        history[-1] = (history[-1][0], (audio_path,))
        yield history

    elif isinstance(user_input, str) and user_input.startswith("/function "):
        function = user_input[len("/function "):]
        response = function_calling([messages[-1]])
        messages.append({"role": "assistant", "content": response})
        history[-1][1] = response
        yield history
    
    
    elif isinstance(user_input, str) and user_input.startswith("/file "):
        question_content = user_input[len("/file"):]
        question = generate_answer(current_file_text, question_content)
        response_generator = generate_text(question)
        for response in response_generator:
            history[-1][1] += response
            time.sleep(0.05)
            yield history
        
        yield history
    
    elif isinstance(user_input[0], str) and user_input[0].endswith(".png"):
        response_generator = history[-1][1]
        yield history

    elif isinstance(user_input[0], str) and user_input[0].endswith(".txt"):
        prompt = messages[-1]["content"]
        response_generator = generate_text(prompt)
        for response in response_generator:
            history[-1][1] += response
            time.sleep(0.05)
            yield history

    elif isinstance(user_input[0], str) and user_input[0].endswith(".zip"):
        yield history

    else:
        response_generator = chat(messages)  # 调用chat函数，获取生成器
        for response in response_generator:
            history[-1][1] += response  # 更新history中的助手回复
            time.sleep(0.05)
            yield history  # 每次生成新的history
    # 完成后更新messages
    if response_generator:  # 确保response_generator已定义
        responses = []  # 创建一个列表来存储响应
        for response in response_generator:  # 迭代生成器
            responses.append(response)  # 添加每个响应到列表
        combined_response = ''.join(responses)  # 拼接所有响应
        messages.append({"role": "assistant", "content": combined_response})  # 更新messages

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio", "text"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch()
