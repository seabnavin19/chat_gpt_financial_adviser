from fastapi import FastAPI
from utils.chat import ChatBot
from utils.excute_query import DatabaseInterpreter, DataframeTranslate
import uvicorn
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS configuration

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


class QuestionRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: QuestionRequest):
    question = request.question

    chatbot = ChatBot()
    interpreter = DatabaseInterpreter()
    sql_question = chatbot.get_messages(question)

    answer = interpreter.InterpretRespone(sql_question)

    description = DataframeTranslate().get_description(question=question, data=answer)

    # return a proper response with success code
    print(description)
    return {
        "success": True,
        "question": question,
        "answer": description
    }



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
