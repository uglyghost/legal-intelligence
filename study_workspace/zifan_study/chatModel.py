from langchain.chat_models import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = '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'
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
chat = ChatOpenAI(temperature=0)
'''
messages = [
    SystemMessage(content="You are a helpful assistant that translates English to French."),
    HumanMessage(content="Translate this sentence from English to French. I love programming.")
]
print(chat(messages))
'''
batch_messages = [
    [
        SystemMessage(content="You are a helpful assistant that translates English to Chinese."),
        HumanMessage(content="Translate this sentence from English to Chinese. You love programming.")
    ],
    [
        SystemMessage(content="You are a helpful assistant that translates English to Chinese."),
        HumanMessage(content="Translate this sentence from English to Chinese. You love artificial intelligence.")
    ],
]
result = chat.generate(batch_messages)
print(result)

#generations=[[ChatGeneration(text='你喜欢编程。', generation_info=None, message=AIMessage(content='你喜欢编程。', additional_kwargs={}, example=False))],
# [ChatGeneration(text='你喜欢人工智能。', generation_info=None, message=AIMessage(content='你喜欢人工智能。', additional_kwargs={}, example=False))]]
# llm_output={'token_usage': {'prompt_tokens': 69, 'completion_tokens': 19, 'total_tokens': 88}, 'model_name': 'gpt-3.5-turbo'}
# run=[RunInfo(run_id=UUID('1234edaf-cb49-4f83-a67c-7a187a817730')), RunInfo(run_id=UUID('b57f0f4e-41ec-46ba-bb24-eac5e9998411'))]

print(result.llm_output['token_usage'])
#{'prompt_tokens': 69, 'completion_tokens': 19, 'total_tokens': 88}