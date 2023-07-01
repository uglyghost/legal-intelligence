from langchain.chat_models import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = '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'
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
chat = ChatOpenAI(temperature=0)

print(chat([HumanMessage(content="Translate this sentence from English to Chinese. The weather today is so nice.")]))

# content='今天的天气真好。' additional_kwargs={} example=False
