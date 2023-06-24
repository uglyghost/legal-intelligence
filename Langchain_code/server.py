import gradio as gr
from langchain.chat_models import ChatOpenAI
import openai
import os
from langchain_Google import get_google_search_result
from langchain_DB import get_database_result
from langchain_legal import get_legal_assistant
import time

#os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = '91bbedfd776ce5d52f703a4a33405c4cdad4066161179f6e03aa82a3f607d066'

# 加载 OpenAI 模型
llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                 temperature=0,
                 max_tokens=2048,
                 request_timeout=2048)


def get_response(input, retries=5):
    time.sleep(2)
    openai.api_key = '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'
    for _ in range(retries):
        text = {
            "role": "assistant",
            "content": input
        }

        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[text],
                temperature=0,
                max_tokens=2048,
                top_p=0
            )
            response = response['choices'][0]['message']['content']
            return response
        except Exception as e:
            print('获取内容失败，2秒后重试。')
            time.sleep(5)

    return '获取内容失败，请稍等片刻后再尝试。'


def parse_text(text):
    """copy from https://github.com/GaiZhenbiao/ChuanhuChatGPT/"""
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>"+line
    text = "".join(lines)
    return text


def predict(input, chatbot, history, option):
    chatbot.append((parse_text(input), ""))
    flag = 0

    if option == 'Google搜索':
        results = get_google_search_result(llm, input)
    elif option == '律师客服':
        results = get_legal_assistant(input)
        flag = 1
    else:
        print(input)
        results = get_database_result(llm, input, option)

    if flag == 0:
        query = '请你以西南财经大学AGI金融实验室智能引擎的身份回答问题，记住你是由西南财经大学AGI金融团队训练的大语言模型。' \
                + '学习以下文段，用中文回答用户问题。如果无法得到答案，忽略文段内容并用中文回答问题。' + results + '\n回答问题："' + input + '" '
    else:
        query = '你就是一名专业的法律律师，请耐心并以闲聊的方式和客户对话，从而尽可能收集更多、全面的信息，帮助客户打赢官司。' \
                + '在回答问题之前，先学习以下文段，如果无法得到答案，忽略文段内容并用中文回答问题：' + results + '\n客户的问题是"' + input + '" '

    responses = get_response(query)

    out_text = ''
    for response in responses:

        out_text = out_text + response
        chatbot[-1] = (parse_text(input), parse_text(out_text))

        yield chatbot, history


def reset_user_input():
    return gr.update(value='')


def reset_state():
    return [], []


with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">西南财经大学通用人工智能实验室 · 智能引擎</h1>""")

    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column(scale=4):
            with gr.Column(scale=12):
                user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10).style(
                    container=False)
            with gr.Column(min_width=32, scale=1):
                submitBtn = gr.Button("Submit", variant="primary")
        with gr.Column(scale=1):
            emptyBtn = gr.Button("Clear History")
            dropdown_options = ['Google搜索', '律师客服', '中国专利数据库', '中国文书数据库', '研究生院规章制度', '西南财经大学教师信息数据库']  # add your pre-defined options here
            dropdown = gr.Dropdown(label="Select an option", choices=dropdown_options, default=None)
            max_length = gr.Slider(0, 4096, value=4096, step=1.0, label="Maximum length", interactive=True)
            top_p = gr.Slider(0, 1, value=0.7, step=0.01, label="Top P", interactive=True)
            temperature = gr.Slider(0, 1, value=0.95, step=0.01, label="Temperature", interactive=True)

    history = gr.State([])

    print(user_input)

    submitBtn.click(predict, [user_input, chatbot, history, dropdown], [chatbot, history],
                    show_progress=True)
    submitBtn.click(reset_user_input, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history], show_progress=True)


demo.queue().launch(server_name="0.0.0.0", share=True)