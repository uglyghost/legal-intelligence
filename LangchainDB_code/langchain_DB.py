from langchain import SQLDatabase, SQLDatabaseChain


def get_database_result(llm, input, option):
    if option == '中国专利数据库':
        db = SQLDatabase.from_uri("mysql+pymysql://root:12345678@127.0.0.1/ChinaPatent")
    elif option == '中国文书数据库':
        db = SQLDatabase.from_uri("mysql+pymysql://root:12345678@127.0.0.1/LawWenshu")
    elif option == '研究生院规章制度':
        db = SQLDatabase.from_uri("mysql+pymysql://root:12345678@127.0.0.1/SwufeGraduate")
    elif option == '西南财经大学教师信息数据库':
        db = SQLDatabase.from_uri("mysql+pymysql://root:12345678@127.0.0.1/SwufeTeacher")
    else:
        return '数据库无相关数据'

    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
    return_text = db_chain.run(input)

    return return_text