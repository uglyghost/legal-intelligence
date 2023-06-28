import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.agents import AgentType

# openAI的Key
os.environ["OPENAI_API_KEY"] = '********************'
# 谷歌搜索的Key
os.environ["SERPAPI_API_KEY"] = '**********************'

# 加载 OpenAI 模型
llm = OpenAI(temperature=0, max_tokens=2048)

# 加载 serpapi 工具
tools = load_tools(["serpapi"])

# 如果搜索完想在计算一下可以这么写
# tools = load_tools(['serpapi', 'llm-math'])

# 如果搜索完想再让他再用python的print做点简单的计算，可以这样写
# tools=load_tools(["serpapi","python_repl"])

"""
agent：代理类型  
<p>
    zero-shot-react-description: 根据工具的描述和请求内容的来决定使用哪个工具（最常用）
    react-docstore: 使用 ReAct 框架和 docstore 交互, 使用Search 和Lookup 工具, 前者用来搜, 后者寻找term, 举例: Wipipedia 工具
    self-ask-with-search 此代理只使用一个工具: Intermediate Answer, 它会为问题寻找事实答案(指的非 gpt 生成的答案, 而是在网络中,文本中已存在的), 如 Google search API 工具
    conversational-react-description: 为会话设置而设计的代理, 它的prompt会被设计的具有会话性, 且还是会使用 ReAct 框架来决定使用来个工具, 并且将过往的会话交互存入内存
</p>
"""
# 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 运行 agent
agent.run("今天星期几?，历史上的今天发生了哪些大事")

'''
result:
> Entering new  chain...
 我需要搜索历史上的今天发生了什么大事
Action: Search
Action Input: "历史上的今天发生了什么大事"
Observation: 6月2日 汪达尔-阿兰王国君主盖萨里克率领汪达尔人进入罗马，展开长达两个星期的洗劫。 意大利发明家古列尔莫·马可尼在英国获得其发明的无线电技术专利，并用于电报工作上。 意大利王国举行决定国家政体公民投票，决定废黜国王翁贝托二世并成立共和国。
Thought: 根据搜索结果，今天是星期二
Final Answer: 今天是星期二，历史上的今天发生了汪达尔-阿兰王国君主盖萨里克率领汪达尔人进入罗马，古列尔莫·马可尼在英国获得其发明的无线电技术专利，以及意大利王国举行决定国家政体公民投票，决定废黜国王翁贝托二世并成立共和国的大事。

> Finished chain.
'''