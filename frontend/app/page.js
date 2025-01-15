"use client";
import React, { useState } from "react";
import Image from "next/image";
import Link from "next/link";

// roles 배열
const roles = [
  {
    id: "ai-chatbot",
    name: "AI Chatbot",
    image: "/ai-chatbot.svg",
    alt: "AI Chatbot",
  },
  {
    id: "medical-professional",
    name: "Medical Professional",
    image: "/medical-professional.svg",
    alt: "Medical Professional",
  },
  {
    id: "student",
    name: "Student",
    image: "/student.svg",
    alt: "Student",
  },
];

export default function ChooseAvatar() {
  const [selected, setSelected] = useState("");
  const [userMessage, setUserMessage] = useState("");
  const [botResponse, setBotResponse] = useState("");

  const handleSelection = (roleId) => {
    setSelected(roleId);
  };

  const sendMessageToFlask = async () => {
    if (!userMessage) return;
    // chatbot_type = 'A' (informal), 'B' (formal) 등 구분
    // 여기서는 예시로 'A'
    const chatbotType = "A";
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage, chatbot_type: chatbotType }),
      });
      const data = await res.json();
      if (data.bot_response) {
        setBotResponse(data.bot_response);
      } else if (data.error) {
        setBotResponse(`Error: ${data.error}`);
      } else {
        setBotResponse("Something went wrong.");
      }
    } catch (err) {
      console.error(err);
      setBotResponse("Request failed.");
    }
  };

  return (
    <div className="bg-[#F6F6F2] min-h-screen flex items-center">
      <div className="max-w-[100%] lg:max-w-[80%] mx-auto mt-18">
        <h2 className="text-4xl text-center leading-tight font-semibold">
          Choose your assistant
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 mt-24 gap-6">
          {roles.map((role) => (
            <div key={role.id} className="flex flex-col items-center">
              <div
                onClick={() => handleSelection(role.id)}
                className={`bg-[#FAFCFC] flex-grow h-full ${
                  selected === role.id ? "select-shadow" : "inner-shadow"
                } px-14 py-10 rounded-2xl flex justify-center items-center cursor-pointer transition-shadow duration-300`}
              >
                <Image
                  src={role.image}
                  width={204}
                  height={484}
                  alt={role.alt}
                  className="h-full"
                />
              </div>
              <h3 className="text-center mt-6 font-bold text-xl leading-6">
                {role.name}
              </h3>
            </div>
          ))}
        </div>

        {/* 사용자 메시지 입력란 */}
        <div className="mt-8 flex flex-col items-center">
          <input
            className="border p-2 rounded w-64"
            placeholder="Type your message..."
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
          />
          <button
            className="bg-blue-600 text-white mt-4 px-4 py-2 rounded"
            onClick={sendMessageToFlask}
          >
            Send to Flask
          </button>
        </div>

        {/* Flask로부터 받은 봇 응답 */}
        {botResponse && (
          <div className="mt-4">
            <p>Bot says: {botResponse}</p>
          </div>
        )}

        <div className="flex flex-col justify-center items-center">
          <Link href={selected ? `/${selected}` : "#"}>
            <p
              className={`mt-12 flex items-center mb-8 text-2xl leading-7 font-bold text-white px-10 py-4 gap-2 rounded-full ${
                selected
                  ? "bg-gradient-to-r from-[#28AAE1] via-[#0364B3] to-[#012B4D] hover:opacity-90"
                  : "bg-[#C9C7C7] cursor-not-allowed"
              }`}
              onClick={(e) => {
                if (!selected) {
                  e.preventDefault();
                }
              }}
            >
              Carry On
              <Image
                src="/arrow-right.svg"
                width={28}
                height={28}
                alt="Arrow Right"
              />
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
}
