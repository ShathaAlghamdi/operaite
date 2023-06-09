from fastapi import FastAPI, requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import openai
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")



class Item(BaseModel):
    # api_secret_key: str
    messages: list


app = FastAPI(
    title="Fast API",
    description="description",
)
origins = [
    "http://localhost",
    "http://127.0.0.1:3000/v1/qcm",
    # "http://localhost:3000",
    # "http://127.0.0.1:3000/",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def inits():

    return {

        "access": True,
        "message": "Hello world from operaite Fast API.."
    }

# @cross_origin(supports_credentials=True)


@app.post('/chat')
def chat(data: Item):
    # response.headers.add('Access-Control-Allow-Origin', '*')

    # body = request.json
    messages = data.messages
    # return data
    # api_secret_key = data.api_secret_key

    try:
        # openai.api_key = api_secret_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)

        return response
        return {
            "access": True,
            "response": response
        }

    except openai.error.AuthenticationError as e:
        print("OpenAI unknown authentication error")
        print(e.json_body)
        print(e.headers)
        return {

            "access": False,
            "headers": str(e.headers),
            "json_body": str(e.json_body)
        }

    except Exception as e:
        return {

            "access": False,
            "message": f"Error says {e}"

        }


if __name__ == "__main__":
    uvicorn.run('app:app', host="127.0.0.1", port=4242)