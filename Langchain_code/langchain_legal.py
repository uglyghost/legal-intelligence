import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# 设置 OpenAI API 的密钥
os.environ["OPENAI_API_KEY"] = "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"


# 加载嵌入模型，并返回相关文档的检索器
def load_embedding():
    # 初始化嵌入模型
    embedding = OpenAIEmbeddings()
    # 初始化向量数据库，并设置嵌入函数
    vectordb = Chroma(persist_directory='db', embedding_function=embedding)
    # 获取检索器，并设置搜索参数k为5
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    return retriever


# 根据检索器和查询生成提示
def prompt(retriever, query):
    # 设置提示模板
    prompt_template = """请注意：请谨慎评估query与提示的Context信息的相关性，只根据本段输入文字信息的内容进行回答，如果query与提供的材料无关，请回答"我不知道"，另外也不要回答无关答案：
    Context: {context}
    Context: {context}
    Question: {question}
    Answer:"""
    # 初始化提示模板，并设置输入变量
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    # 使用检索器获取相关文档
    docs = retriever.get_relevant_documents(query)

    # 使用相关文档生成提示，返回想要的内容
    chain = load_qa_chain(ChatOpenAI(temperature=0), chain_type="stuff", prompt=PROMPT)
    print(docs)
    # 获取输出结果
    result = chain({"input_documents": docs, "question": query}, return_only_outputs=False)
    return result['output_text']


# 获取法律助手的回答
def get_legal_assistant(query):
    # 设置代理服务器地址
    os.environ["http_proxy"] = "http://127.0.0.1:1080"
    os.environ["https_proxy"] = "http://127.0.0.1:1080"
    # 加载嵌入模型
    retriever = load_embedding()
    # 返回生成的提示
    return prompt(retriever, query)


if __name__ == "__main__":
    # 设置代理服务器地址
    os.environ["http_proxy"] = "http://127.0.0.1:1080"
    os.environ["https_proxy"] = "http://127.0.0.1:1080"
    # 加载嵌入模型
    retriever = load_embedding()
    # 循环输入查询，直到输入 "exit" 退出
    while True:
        query = input("输入查询（或输入 'exit' 退出）: ")
        if query == 'exit':
            print('退出')
            break
        print("查询：" + query + '\n回答：' + prompt(retriever, query) + '\n')
