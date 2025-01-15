"use client";
import Image from "next/image";
import React, { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";

export default function ChatBox() {
  const params = useParams();  // URL 파라미터 예: { role: 'ai-chatbot' }
  const chatContainerRef = useRef(null);

  const [messages, setMessages] = useState([
    // 초기에 들어있는 대화 예시
    {
      id: 1,
      type: "assistant",
      text: "Hello, I'm here to help. Feel free to share your concerns.",
      timestamp: "09:00 AM",
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);

  useEffect(() => {
    // 스크롤 맨 아래로
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, loading]);

  // 실제 Flask로 메시지 보내는 함수
  const sendToFlask = async (userInput) => {
    // chatbot_type: A or B. role에 따라 달리할 수도 있음
    // 예시: ai-chatbot => A, medical-professional => B
    let chatbotType = "A";
    if (params.role === "medical-professional") {
      chatbotType = "B";
    }

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput, chatbot_type: chatbotType }),
      });
      const data = await res.json();
      if (data.bot_response) {
        return data.bot_response;
      } else if (data.error) {
        return `Error: ${data.error}`;
      } else {
        return "Something went wrong.";
      }
    } catch (err) {
      console.error(err);
      return "Request failed.";
    }
  };

  const handleAddMessage = async () => {
    if (!inputValue.trim()) return;

    // 1) 유저 메시지 추가
    const newUserMessage = {
      id: Date.now(),
      type: "user",
      text: inputValue.trim(),
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };
    setMessages((prev) => [...prev, newUserMessage]);
    setInputValue("");
    setLoading(true);

    // 2) Flask API로 보낸 뒤, 봇 응답 받기
    const assistantResponse = await sendToFlask(newUserMessage.text);

    // 3) 봇 메시지 추가
    const newAssistantMessage = {
      id: Date.now() + 1,
      type: "assistant",
      text: assistantResponse,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };
    setMessages((prev) => [...prev, newAssistantMessage]);
    setLoading(false);
  };

  const today = new Date().toLocaleDateString("en-US", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });

  return (
    <div className="grid md:grid-cols-[30%,auto] lg:grid-cols-[40%,auto] xl:grid-cols-[30%,auto] ">
      {/* 좌측 사이드 */}
      <div className="px-[15px] lg:px-[20px] xl:px-[40px] py-[40px]">
        <Image
          src="/logo.svg"
          width={182}
          height={40}
          alt="logo"
        />

        <div className="flex flex-col mt-[89px] justify-center items-center">
          <div className="mb-[80px]">
            <Image src="/sky.svg" width={132} height={44} alt="sky" />
          </div>
          <div>
            {/* 역할별 SVG */}
            <Image
              src={`/${params.role}.svg`}
              width={245}
              height={329}
              alt="doctor"
            />
          </div>

          <div className="bg-[#F6F6F2] custom-shadow mt-[14px] font-semibold text-[16px] leading-[19px] px-[24px] rounded-[16px] flex justify-center items-center py-[14px] text-center text-[#232C3C]">
            Just know that I’m here for you. Always.
          </div>
        </div>
      </div>

      {/* 우측 채팅 영역 */}
      <div className="flex px-[20px]  xl:px-[40px] py-[32px] flex-col md:h-screen justify-between bg-white flex-grow">
        {/* 날짜 라벨 */}
        <div className="flex items-center pb-[40px] gap-2 px-4">
          <div className="h-[1px] w-[40%] flex-grow bg-[#D9D9D9]"></div>
          <p className="flex-shrink-0">{today}</p>
          <div className="h-[1px] w-[40%] flex-grow-0 bg-[#D9D9D9]"></div>
        </div>

        {/* 채팅 메시지 목록 */}
        <div className="flex-grow overflow-y-auto custom-scrollbar" ref={chatContainerRef}>
          <div className="flex flex-col gap-2">
            {messages.map((msg) => {
              const isAssistant = msg.type === "assistant";
              const alignmentClass = isAssistant ? "self-start" : "self-end";
              const bubbleClass = isAssistant
                ? "bg-[#EEF2FD] text-black"
                : "bg-[#F6F6F2] text-black";

              return (
                <div
                  key={msg.id}
                  className={`${alignmentClass} ${
                    isAssistant ? "flex items-center justify-center " : ""
                  } max-w-[85%] lg:max-w-[70%] mb-2`}
                >
                  <div className={`${bubbleClass} px-4 py-3 rounded-2xl text-sm`}>
                    {msg.text}
                  </div>
                  {isAssistant && (
                    <span className="text-xs ml-[16px] flex-shrink-0 text-gray-400">
                      {msg.timestamp}
                    </span>
                  )}
                </div>
              );
            })}
          </div>

          {/* 로딩 중 점 세 개 표시 */}
          {loading && (
            <div className="self-start w-fit">
              <div className="bg-[#EEF2FD] text-black px-4 py-3 rounded-2xl text-sm">
                <div className="flex gap-1">
                  <span className="dot-animation bg-gray-400 w-2 h-2 rounded-full"></span>
                  <span className="dot-animation bg-gray-400 w-2 h-2 rounded-full"></span>
                  <span className="dot-animation bg-gray-400 w-2 h-2 rounded-full"></span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* 자동완성 / 예시 버튼들 */}
        {showSuggestions && (
          <div className="flex pt-[24px] pb-[24px] overflow-y-hidden items-center gap-3 overflow-x-auto relative">
            <Image
              onClick={() => setShowSuggestions(false)}
              src="/cross.svg"
              width={50}
              height={50}
              alt="x"
            />

            {[
              "Schedule availability",
              "Tell me something about..",
              "Clinic Information",
              "Make a reservation",
            ].map((suggestion, index) => (
              <button
                key={index}
                onClick={() => setInputValue(suggestion)}
                className="bg-white custom-shadow flex-shrink-0 text-[#363A3D] font-bold text-[16px] leading-[19px] rounded-[40px] border border-gray-300 px-[20px] py-[12px] text-sm hover:shadow-md transition-all"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}

        {/* 입력창 + 전송 버튼 */}
        <div className="py-[24px] px-[12px] lg:px-[24px] rounded-[20px] border border-[#D9D9D9] bg-[#F6F6F2] flex items-center">
          <input
            type="text"
            placeholder="What you want to share today?"
            className="flex-grow bg-transparent text-[16px] leading-[19px] outline-none"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleAddMessage();
            }}
          />
          <button
            onClick={handleAddMessage}
            className="bg-gradient-to-r w-[48px] h-[48px] from-[#28AAE1] via-[#0364B3] to-[#012B4D] text-white px-4 py-2 rounded-[12px] text-sm ml-2"
          >
            <Image src="/send.svg" width={24} height={24} alt="send" />
          </button>
        </div>

        {/* 아래쪽 아이콘들 (디자인용) */}
        <div className="flex items-center gap-[24px] mt-[12px]">
          <Image src="/A.svg" width={24} height={24} alt="A" />
          <Image src="/A2.svg" width={24} height={24} alt="A2" />
          <Image src="/smile.svg" width={24} height={24} alt="smile" />
          <Image src="/drive.svg" width={24} height={24} alt="drive" />
          <Image src="/lock.svg" width={24} height={24} alt="lock" />
          <Image src="/pen.svg" width={24} height={24} alt="pen" />
          <Image src="/vertical.svg" width={24} height={24} alt="vertical" />
        </div>
      </div>
    </div>
  );
}
