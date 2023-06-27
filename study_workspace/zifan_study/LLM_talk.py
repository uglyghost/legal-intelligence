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

#result1="一个老太太和一个小男孩在乘公交车。小男孩惊讶地说：“外婆，你可以拿一张票，然后我们就能从这里走了？”老太太摇摇头：“不，不，孩子，我们付了钱，得到一张票，然后就可以乘车去另外一个地方了！"