import gradio as gr
import os
import time
from chat import chat  # 导入chat函数
from search import search  # 导入search函数
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
    messages.append({"role": "user", "content": file.name})  # 更新messages
    history = history + [((file.name,), None)]
    return history


def bot(history):
    global messages  # 声明使用全局变量
    user_input = history[-1][0]  # 获取用户输入
    response_generator = None  # 初始化response_generator

    # 检查是否为搜索指令
    history[-1][1]=""
    if(True):
        response_generator = chat(messages)  # 调用chat函数，获取生成器
        for response in response_generator:
            print(response)
            history[-1][1] += response  # 更新history中的助手回复
            time.sleep(0.05)
            yield history  # 每次生成新的history

    # 完成后更新messages
    if response_generator:  # 确保response_generator已定义
        messages.append({"role": "assistant", "content": ''.join(response_generator)})  # 更新messages

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
#demo.launch(server_name="166.111.80.101", server_port=8080, share=True)
#demo.launch(server_name="166.111.80.101")