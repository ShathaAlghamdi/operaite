import { useState, useEffect } from "react";
import axios from 'axios';


export default function Home() {
  const [inputValue, setInputValue] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    setChatLog((prevChatLog) => [...prevChatLog, { type: 'user', message: inputValue }])

    sendMessage(inputValue);
    
    setInputValue('');
  }
  const sendMessage = (message) => {
    const url = './api/chat';

    const data = {
      model: "gpt-3.5-turbo-0301",
      messages: [{ "role": "user", "content": message }]
    };
    
    setIsLoading(true);

    axios.post(url, data).then((response) => {
      console.log(response);
      setChatLog((prevChatLog) => [...prevChatLog, { type: 'bot', message: response.data.choices[0].message.content }])
      setIsLoading(false);
    }).catch((error) => {
      setIsLoading(false);
      console.log(error);
    })
  }

  return (
    <div className="container mx-auto max-w-[700px] overflow-y-auto">
      <div className="flex flex-col h-screen bg-gray-900">
        <h1 className="sticky top-0 bg-gradient-to-r from-white to-cyan-300 text-transparent bg-clip-text text-center py-3 font-bold text-6xl">Oper<span className="text-white">AI</span>te</h1>
        <div className="flex-grow p-6">
          <div className="flex flex-col space-y-4">
          {
        chatLog.map((message, index) => (
          <div key={index} className={`flex ${
            message.type === 'user' ? 'justify-end' : 'justify-start'
            }`}>
            <div className={`${
              message.type === 'user' ? 'bg-gray-200' : 'bg-gray-500'
            } rounded-xl p-4 text-black max-w-sm`}>
            {message.message}
            </div>
            </div>
        ))
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


