import os
import openai

openai.api_key = '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'


class ChatBot:
    
    def __init__(self,type='q'):
        if type == 'q':
            self.messages=[
                            {
                                "role": "system",
                                "content": '''
                                you are an engine that convert from question to sql query and 
                                this is my table schema:
                                fix_deposit_view : (bank,rate,term in months only,rate_at,ccy,open:which mean user open with anything)
                                saving_view: (bank,rate,ccy)
                                + here are the rule
                                - give me only raw data, and data need to be full columns,
                                - mother fucker please use select *
                                
                            
                                '''
                                },
                                
                                {
                                "role": "user",
                                "content": "which bank has the highest fix deposit"
                                },
                                {
                                "role": "assistant",
                                "content": "select * from fix_deposit_view  order by rate desc limit 3"	
                                },
                                {
                                "role": "user",
                                "content": "compare aba fix deposit and acleda fix desposit "
                                },
                                {
                                "role": "assistant",
                                "content": "select * from fix_deosit_view  where bank in ('ABA','ACLEDA') order by rate  desc"
                                },
                                {
                                    'role': 'user',
                                    'content': 'compare fix deposit rate of aba bank and acleda bank'
                                },
                                {
                                    'role': 'assistant',
                                    'content': 'select * from fix_deposit_view  where bank in (\'ABA\',\'ACLEDA\')  by rate desc'
                                }
                            ]
        else:
            self.messages = [
                                {
                                "role": "system",
                                "content": '''

                                this is my table schema:
                                    fix_deposit_view : (bank,rate,term in months only,rate_at,ccy,open:which mean user open with anything)
                                    saving_view: (bank,rate,ccy)

                                you are a system that help me analysis the data 
                                i give you data frame you help me answer the question, 
                                if dataframe empty you just say you don't know you don't hae info right now 
                                ** please answer in less than 30 words
                                '''
                                },
                                {
                                    'role':'user',
                                    'content':''''
                                    - Question : which bank has the highest fix deposit ?

                                    - Dataframe
                                        bank  term     open  ccy       date  rate
                                        0  SHINHAN    36   MOBILE  KHR 2023-07-08   9.1
                                        1      ABA    60  COUNTER  KHR 2023-07-08   9.0
                                        2      ABA    60   MOBILE  KHR 2023-07-08   9.0
                                        3  SHINHAN    36  COUNTER  KHR 2023-07-08   9.0
                                        4    WOORI    36   MOBILE  KHR 2023-07-08   9.0
                                    
                                    '''

                                },
                                {
                                    'role':'assistant',
                                    'content':''' 
                                    Shihan bank has the highest fix depeposit rate with 9.1% in 36 months term in KHR currency and you need to open via mobile app.
                
                                    '''
                                }

            ]
                    

    def get_messages(self,question):
        print(question)
        new_message = {"role": "user",
                    "content": question
                    }
        me= []
        message = self.messages
        message.append(new_message)      
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

        assistant_reply = response['choices'][-1]['message']['content']
        print(assistant_reply)

        return assistant_reply
    
    # def get_description(self,question):
