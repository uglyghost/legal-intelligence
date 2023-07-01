from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
os.environ["OPENAI_API_KEY"] = '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'

chat = ChatOpenAI(temperature=0)
template = "You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
chain = LLMChain(llm=chat, prompt=chat_prompt)
print(chain.run(input_language="English", output_language="French", text="I love programming."))

# -> "J'aime programmer."