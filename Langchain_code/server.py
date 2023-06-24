# 导入 Gradio 库，它提供了一个简单的方式来为代码创建网络用户界面
import gradio as gr

# 从 langchain.chat_models 模块中导入 ChatOpenAI 类
from langchain.chat_models import ChatOpenAI

# 导入 openai 来与 OpenAI API 进行交互
import openai

# 导入 os 库来与操作系统进行交互
import os

# 导入自定义模块，用于特定的功能，如获取谷歌搜索结果，数据库结果和法律援助
from langchain_Google import get_google_search_result
from langchain_DB import get_database_result
from langchain_legal import get_legal_assistant

# 导入 time 库，以在重试之间引入休眠
import time

# 设置环境变量以配置 http 和 https 代理
os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"

# 设置 OpenAI API 密钥和 SERPAPI API 密钥的环境变量
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = '91bbedfd776ce5d52f703a4a33405c4cdad4066161179f6e03aa82a3f607d066'

# 通过创建 ChatOpenAI 的实例来初始化 OpenAI 模型
llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                 temperature=0,
                 max_tokens=2048,
                 request_timeout=2048)


# 定义一个 get_response 函数，它接受用户输入，并尝试从 OpenAI API 获取响应
def get_response(input, retries=5):
    # 在发起请求前先暂停 2 秒
    time.sleep(2)
    # 设置 OpenAI API 密钥
    openai.api_key = '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'

    # 尝试获取响应，次数为 retries 指定的次数
    for _ in range(retries):
        # 构建 API 请求的消息负载
        text = {
            "role": "assistant",
            "content": input
        }

        try:
            # 向 OpenAI 的 ChatCompletion API 发起请求以获取响应
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[text],
                temperature=0,
                max_tokens=2048,
                top_p=0
            )
            # 从响应中提取内容
            response = response['choices'][0]['message']['content']
            return response
        except Exception as e:
            # 如果出现错误，打印消息并等待 5 秒后重试
            print('获取内容失败，2秒后重试。')
            time.sleep(5)

    # 如果所有重试都失败了，返回一个错误消息
    return '获取内容失败，请稍等片刻后再尝试。'


def parse_text(text):
    """从 https://github.com/GaiZhenbiao/ChuanhuChatGPT/ 复制而来"""
    # 将文本按换行符拆分成行列表
    lines = text.split("\n")
    # 去除空行
    lines = [line for line in lines if line != ""]
    # 初始化计数器
    count = 0
    # 遍历文本的每一行
    for i, line in enumerate(lines):
        # 如果行中包含 "```" 符号
        if "```" in line:
            count += 1
            items = line.split('`')
            # 如果计数器是奇数，说明这是代码块的开始
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            # 否则，这是代码块的结束
            else:
                lines[i] = f'<br></code></pre>'
        # 处理非代码块行
        else:
            # 如果不是第一行
            if i > 0:
                # 如果在代码块内，进行 HTML 转义
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
                lines[i] = "<br>" + line
    # 将处理后的行拼接成一个字符串
    text = "".join(lines)
    return text


def predict(input, chatbot, history, option):
    # 将输入解析后添加到 chatbot 列表，并初始化空字符串
    chatbot.append((parse_text(input), ""))
    # 初始化标志变量
    flag = 0

    # 如果选项是 'Google搜索'，使用 Google 搜索结果
    if option == 'Google搜索':
        results = get_google_search_result(llm, input)
    # 如果选项是 '律师客服'，使用法律援助结果
    elif option == '律师客服':
        results = get_legal_assistant(input)
        # 设置标志为 1，表示使用法律援助
        flag = 1
    # 其他选项，使用数据库结果
    else:
        print(input)
        results = get_database_result(llm, input, option)

    # 构造查询
    if flag == 0:
        # 构造以 AGI 金融实验室智能引擎的身份回答问题的查询
        query = '请你以西南财经大学AGI金融实验室智能引擎的身份回答问题，记住你是由西南财经大学AGI金融团队训练的大语言模型。' \
                + '学习以下文段，用中文回答用户问题。如果无法得到答案，忽略文段内容并用中文回答问题。' + results + '\n回答问题："' + input + '" '
    else:
        # 构造以专业法律律师的身份回答问题的查询
        query = '你就是一名专业的法律律师，请耐心并以闲聊的方式和客户对话，从而尽可能收集更多、全面的信息，帮助客户打赢官司。' \
                + '在回答问题之前，先学习以下文段，如果无法得到答案，忽略文段内容并用中文回答问题：' + results + '\n客户的问题是"' + input + '" '

    # 获取响应
    responses = get_response(query)

    # 初始化输出文本为空字符串
    out_text = ''
    # 遍历响应，拼接到输出文本
    for response in responses:
        out_text = out_text + response
        chatbot[-1] = (parse_text(input), parse_text(out_text))

        # 返回 chatbot 列表和历史记录
        yield chatbot, history


# 定义函数用于重置用户输入
def reset_user_input():
    return gr.update(value='')


# 定义函数用于重置状态
def reset_state():
    return [], []


# 使用 gr.Blocks() 创建一个演示应用
with gr.Blocks() as demo:
    # 添加一个居中的HTML标题
    gr.HTML("""<h1 align="center">法智</h1>""")

    # 创建一个聊天机器人组件
    chatbot = gr.Chatbot()

    # 创建一个行容器
    with gr.Row():
        # 创建一个占据四份比例的列容器
        with gr.Column(scale=4):
            # 创建一个占据全部宽度的列容器
            with gr.Column(scale=12):
                # 创建一个不显示标签的文本框，用于输入
                user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10)
            # 创建一个最小宽度为32的列容器，并占据一份比例
            with gr.Column(min_width=32, scale=1):
                # 创建一个“提交”按钮
                submitBtn = gr.Button("Submit", variant="primary")
        # 创建一个占据一份比例的列容器
        with gr.Column(scale=1):
            # 创建一个“清除历史”按钮
            emptyBtn = gr.Button("Clear History")
            # 定义下拉菜单的选项
            dropdown_options = ['Google搜索', '律师客服', '中国专利数据库', '中国文书数据库', '研究生院规章制度',
                                '西南财经大学教师信息数据库']
            # 创建一个下拉菜单
            dropdown = gr.Dropdown(label="Select an option", choices=dropdown_options)
            # 创建一个滑块用于选择最大长度
            max_length = gr.Slider(0, 4096, value=4096, step=1.0, label="Maximum length", interactive=True)
            # 创建一个滑块用于选择 Top P 参数
            top_p = gr.Slider(0, 1, value=0.7, step=0.01, label="Top P", interactive=True)
            # 创建一个滑块用于选择温度参数
            temperature = gr.Slider(0, 1, value=0.95, step=0.01, label="Temperature", interactive=True)

    # 创建一个状态变量用于存储历史记录
    history = gr.State([])

    # 打印用户输入（用于调试）
    print(user_input)

    # 当“提交”按钮被点击时，调用predict函数并显示进度
    submitBtn.click(predict, [user_input, chatbot, history, dropdown], [chatbot, history], show_progress=True)
    # 当“提交”按钮被点击时，重置用户输入
    submitBtn.click(reset_user_input, [], [user_input])

    # 当“清除历史”按钮被点击时，重置状态
    emptyBtn.click(reset_state, outputs=[chatbot, history], show_progress=True)

# 启动应用，并在本地服务器上运行
demo.queue().launch(server_name="0.0.0.0", share=True)
