from langchain.llms import OpenAI
#import os
#os.environ["OPENAI_API_KEY"] = "···"

# llm = OpenAI(openai_api_key="···")
#llm = OpenAI(model_name="text-davinci-003", temperature=0.3)
llm = OpenAI(temperature=0.9)
text = "can you give a classic joke to me in Chinese?"
print(llm(text))
#Feetful of Fun
#llm("给我讲一个笑话")


result1:"为什么海鸥不下蛋？ 因为它们住在海里，没有鸡笼！"
result2:"猴子穿衣服，好像在扮演猴王！"