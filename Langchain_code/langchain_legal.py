import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

os.environ["OPENAI_API_KEY"] = "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"


def load_embedding():
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory='db', embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    return retriever


def prompt(retriever, query):
    prompt_template = """请注意：请谨慎评估query与提示的Context信息的相关性，只根据本段输入文字信息的内容进行回答，如果query与提供的材料无关，请回答"我不知道"，另外也不要回答无关答案：
    Context: {context}
    Context: {context}
    Question: {question}
    Answer:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    docs = retriever.get_relevant_documents(query)

    # 基于docs来prompt，返回你想要的内容
    chain = load_qa_chain(ChatOpenAI(temperature=0), chain_type="stuff", prompt=PROMPT)
    print(docs)
    result = chain({"input_documents": docs, "question": query}, return_only_outputs=False)
    return result['output_text']


def get_legal_assistant(query):
    os.environ["http_proxy"] = "http://127.0.0.1:1080"
    os.environ["https_proxy"] = "http://127.0.0.1:1080"
    retriever = load_embedding()
    return prompt(retriever, query)


if __name__ == "__main__":
    os.environ["http_proxy"] = "http://127.0.0.1:1080"
    os.environ["https_proxy"] = "http://127.0.0.1:1080"
    # load embedding
    retriever = load_embedding()
    # 循环输入查询，直到输入 "exit"
    while True:
        query = input("Enter query (or 'exit' to quit): ")
        if query == 'exit':
            print('exit')
            break
        print("Query:" + query + '\nAnswer:' + prompt(retriever, query) + '\n')