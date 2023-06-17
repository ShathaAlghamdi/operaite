# ! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, jsonify, json, request, current_app
from dotenv import load_dotenv, find_dotenv
import openai
from flask_cors import CORS, cross_origin


load_dotenv(find_dotenv())


# print(os.getenv("OPENAI_API_KEY"))

openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST"]}})



@app.route('/', methods=["GET"])
def init():

    return jsonify(
        access=True,
        message="Hello world from operaite .."
    )

# @cross_origin(supports_credentials=True)


@app.route('/chat', methods=["POST"])
def chat():
    response.headers.add('Access-Control-Allow-Origin', '*')

    body = request.json
    messages = body['messages']
    api_secret_key = body['api_secret_key']

    try:
        openai.api_key = api_secret_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)

        return jsonify(
            access=True,
            response=response
        )

        result = ''

        messages.append(response.choices[0].message)
        for choice in response.choices:
            result += choice.message.content

        return jsonify(
            access=True,
            result=result,
            messages=messages
        )
    except openai.error.AuthenticationError as e:
        print("OpenAI unknown authentication error")
        print(e.json_body)
        print(e.headers)
        return jsonify(
            access=False,
            headers=str(e.headers),
            json_body=str(e.json_body),

        )
    except Exception as e:
        return jsonify(
            access=False,
            message=f"Error says {e}"
        )


@app.route('/chat_langchain', methods=["POST"])
def chat_langchain():
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        AIMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )
    from langchain.schema import AIMessage, HumanMessage, SystemMessage
    chat = ChatOpenAI(temperature=0)
    messages = [
        SystemMessage(
            content="You are a helpful assistant that translates English to French."
        ),
        HumanMessage(
            content="Translate this sentence from English to French. I love programming."
        ),
    ]
    chat(messages)
    # AIMessage(content="J'aime programmer.", additional_kwargs={}, example=False)

    return "done!"
    # return os.getenv("OPENAI_API_KEY")

    # openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = request.json

    # return messages

    try:

        template = """Assistant is a large language model trained by OpenAI.

        Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

        Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

        Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

        {history}
        Human: {human_input}
        Assistant:"""

        prompt = PromptTemplate(
            input_variables=["history", "human_input"], template=template)

        chatgpt_chain = LLMChain(
            llm=OpenAI(temperature=0),
            prompt=prompt,
            verbose=True,
            memory=ConversationBufferWindowMemory(k=2),
        )

        output = chatgpt_chain.predict(
            human_input="I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English I will do so by putting text inside curly brackets {like this}. My first command is pwd."
        )
        # print(output)

        # results = [**messages +  **result]

        # print(messages)

        return jsonify(
            access=True,
            message="Hello world from operaite ..",
            output=output
        )

    except Exception as e:
        return jsonify(
            access=False,
            message=f"Error says {e}"
        )


if __name__ == '__main__':
    app.run(port=4242, debug=True)
