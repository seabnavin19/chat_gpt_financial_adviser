from fastapi import FastAPI
from utils.chat import ChatBot
from utils.excute_query import DatabaseInterpreter, DataframeTranslate
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/chat")
def chat(question: str):
    chatbot = ChatBot()
    interpreter = DatabaseInterpreter()
    sql_question = chatbot.get_messages(question)

    answer=interpreter.InterpretRespone(sql_question)

    description = DataframeTranslate().get_description(question=question,data=answer)



    return description



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
