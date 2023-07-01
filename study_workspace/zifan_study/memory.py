from langchain import OpenAI, ConversationChain
import os
os.environ["OPENAI_API_KEY"] = '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'
llm = OpenAI(temperature=0)
conversation = ConversationChain(llm=llm, verbose=True)
output = conversation.predict(input="Hi there!")
print(output)
output = conversation.predict(input="I'm doing well! Just having a conversation with an AI.")
print(output)
output = conversation.predict(input="About the language?")
print(output)
output = conversation.predict(input="Can you teach me English?")
print(output)