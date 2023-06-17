import { useState, useEffect } from "react";
import axios from 'axios';
import TypingAnimation from "../components/TypingAnimation"

export default function Home() {
  const [inputValue, setInputValue] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    setChatLog((prevChatLog) => [...prevChatLog, { role: 'user', content: inputValue }])

    sendMessage(inputValue);

    setInputValue('');
  }
  const sendMessage = (message) => {
    const url = 'http://localhost:4242/chat';

    var logs = [...chatLog, { role: "user", content: message }]

    // console.info(logs)
    // return

    


    const data = {
      model: "gpt-3.5-turbo-0301",
      messages: [{ "role": "user", "content": message }]
    };

    const config = {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST"
      },
      body: data
    };

    setIsLoading(true);
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    // myHeaders.append("Access-Control-Allow-Origin", "*");
    // myHeaders.append("Access-Control-Allow-Methods", "POST");

    var raw = JSON.stringify({
      "api_secret_key": "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",
      "messages": logs
    });

    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      // redirect: 'follow'
    };

    fetch("http://127.0.0.1:4242/chat", requestOptions)
      .then(response => response.json())
      .then((response) => {
          console.log(response);
          setChatLog((prevChatLog) => [...prevChatLog, { role: 'assistant', content: response.choices[0].message.content }])
          setIsLoading(false);
        }).catch((error) => {
          setIsLoading(false);
          console.log(error);
        })
    // axios.post(url, data).then((response) => {
    //   console.log(response);
    //   setChatLog((prevChatLog) => [...prevChatLog, { type: 'bot', message: response.data.choices[0].message.content }])
    //   setIsLoading(false);
    // }).catch((error) => {
    //   setIsLoading(false);
    //   console.log(error);
    // })
  }

  return (
    <div className="container mx-auto max-w-[700px] overflow-y-auto">
      <div className="flex flex-col h-screen bg-gray-900">
        <h1 className="sticky top-0 bg-gradient-to-r from-white to-cyan-300 text-transparent bg-clip-text text-center py-3 font-bold text-6xl">Oper<span className="text-white">AI</span>te</h1>
        <div className="flex-grow p-6 bg-gray-900">
          <div className="flex flex-col space-y-4 ">
            {
              chatLog.map((message, index) => (
                <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}>
                  <div className={`${message.role === 'user' ? 'bg-gray-200' : 'bg-gray-500'
                    } rounded-xl p-4 text-black max-w-sm`}>
                    {message.content}
                  </div>
                </div>
              ))
            }
            {
              isLoading &&
              <div key={chatLog.length} className="flex justify-start">
                <div className="bg-gray-800 rounded-lg p-4 text-white max-w-sm">
                  <TypingAnimation />
                </div>
              </div>
            }

          </div>
        </div>
        <form onSubmit={handleSubmit} className="flex-none p-6">
          <div className="flex rounded-lg border border-gray-700 bg-gray-800">
            <input type="text" className="flex-grow px-4 py-2 bg-transparent text-white focus:outline-none" placeholder="Ask me... " value={inputValue} onChange={(e) => setInputValue(e.target.value)} />
            <button type="submit" className="bg-gray-500 rounded-lg px-4 py-2 text-white font-semibold focus:outline-none hover:bg-black transition-colors duration-300">send</button>
          </div>
        </form>
      </div>
    </div>
  )
}


