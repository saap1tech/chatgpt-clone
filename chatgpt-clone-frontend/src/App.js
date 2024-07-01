import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const onSubmit = (e) => {
    e.preventDefault();

    setIsLoading(true);

    setMessages([{ content: input, isUser: true }, ...messages]);

    axios
      .post("http://127.0.0.1:5000/chat", { input })
      .then((response) => {
        setMessages([
          { content: response.data.result, isUser: false },
          { content: input, isUser: true },
          ...messages,
        ]);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("error: ", error);
      });

    setInput("");
  };

  return (
    <div className="h-screen flex bg-[#212121] text-white">
      <div className="h-screen flex-[0.15] bg-[#171717] font-bold text-2xl flex flex-col items-center justify-center">
        ChatGPT-Clone
      </div>
      <div className="h-screen flex-[0.85]">
        <div className="h-[85vh] flex flex-col overflow-y-auto p-4 m-4">
          {messages.length > 0 ? (
            messages.map((msg) => (
              <div
                className={`flex ${
                  msg.isUser ? "justify-end" : "justify-start"
                }`}
              >
                <div className="bg-[#4F4F4F] w-1/4 rounded-lg p-4 m-4">
                  {msg.content}
                </div>
              </div>
            ))
          ) : (
            <div className="text-center text-xl font-semibold">
              Please, Start a new chat
            </div>
          )}
        </div>
        <div className="flex justify-center">
          <form onSubmit={onSubmit} className="absolute bottom-5 w-1/2 flex">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Message ChatGPT-Clone"
              className="bg-[#2F2F2F] outline-none rounded-l-full p-4 h-12 w-full"
            />
            {isLoading ? (
              <div className="flex items-center justify-center pr-4 rounded-r-full bg-[#2F2F2F]">
                <div
                  className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
                  role="status"
                >
                  <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
                    Loading...
                  </span>
                </div>
              </div>
            ) : (
              <button
                type="submit"
                className="bg-[#2F2F2F] rounded-r-full pr-4"
              >
                Chat
              </button>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}
