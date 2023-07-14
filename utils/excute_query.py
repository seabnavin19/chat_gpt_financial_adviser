from .database import Connection
import pandas as pd
from .chat import ChatBot
import re
class DatabaseInterpreter:
    def __init__(self):
        self.database = Connection().create_engine()


    def InterpretRespone(self,response):
        if 'order' not in response:
            response = response + ' order by rate desc'

        pattern = r"select.*?from"
        replacement = "select * from"

        response = re.sub(pattern, replacement,response,count=1)
        df = pd.read_sql(response,self.database)
        df = df.head(10)
        return df



class DataframeTranslate:
    def __init__(self):
        self.chatbot = ChatBot(type='d')

    def get_description(self,question,data):
    
    
        question =  f'''
            - Question : {question} + " please answer like you are a financial a"
            
            - Dataframe:
            {data}
            '''
        
        response = self.chatbot.get_messages(question=question)
        print(response)
        return response


    
