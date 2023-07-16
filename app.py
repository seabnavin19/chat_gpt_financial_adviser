from fastapi import FastAPI
from utils.chat import ChatBot
from utils.excute_query import DatabaseInterpreter, DataframeTranslate
import uvicorn

import firebase_admin
import pyrebase
import json
 
from firebase_admin import credentials, auth
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

cred = credentials.Certificate('adminSDK.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase_config.json','r')))


app = FastAPI()
allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)


@app.post("/signup", include_in_schema=True)
async def signup(request: Request):
    req = await request.json()
    google_token = req['google_token']
    if google_token is None:
        return HTTPException(detail={'message': 'Error! Missing Google Token'}, status_code=400)
    
    try:
        # Verify the Google token and retrieve user information
        id_token = pb.auth().verify_id_token(google_token)
        user_data = id_token['firebase']
        # Perform any additional logic or data storage related to the signed-up user
        
        # You can access user information like email and user ID
        email = user_data['email']
        user_id = user_data['user_id']
        
        return JSONResponse(content={'message': f'Successfully created user {user_id}'}, status_code=200)
    
    except:
        return HTTPException(detail={'message': 'Error Creating User'}, status_code=400)




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
