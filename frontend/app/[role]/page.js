"use client";
import Image from "next/image";
import React, { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";

export default function ChatBox() {
  const params = useParams(); // Expected Role: "ai", "student", "doctor"
  const chatContainerRef = useRef(null);

  // Remove the initial greeting message from all roles, so that it appears only from the assessment screen
  const initialMessages = [];

  // Chat related status
  const [messages, setMessages] = useState(initialMessages);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);

  // Assessment Status (all roles only)
  const [assessmentStep, setAssessmentStep] = useState(0);
  const [assessmentScore, setAssessmentScore] = useState(0);
  const [assessmentEnded, setAssessmentEnded] = useState(false);

  // Assessment Flow: Answer questions via buttons to get a score
  const assessmentSteps = {
    0: {
      text: "Hello! I'm Dr. Sky, here to provide guidance on alcohol awareness and healthier choices. Before we begin, can I ask a couple of quick questions? Are you between the ages of 18 and 20?",
      options: [
        { text: "Yes", next: 1 },
        { text: "No", next: "confirm_continue" },
      ],
    },
    confirm_continue: {
      text: "This assessment is designed for individuals between 18 and 20 years old. If you're younger or older, I can still provide general information on alcohol awareness. Would you like to continue?",
      options: [
        { text: "Yes, I'd still like to learn more", next: 1 },
        { text: "No, I'd rather not", end: true },
      ],
    },
    1: {
      text: "Have you ever had alcohol before, even just a few sips?",
      options: [
        { text: "Yes", next: 2 },
        { text: "No", next: 2 },
      ],
    },
    2: {
      text: "Thanks for sharing! Even if you don't drink, this assessment can help you learn more about alcohol risks and peer influences. Would you like to continue?",
      options: [
        { text: "Yes, let's do it!", next: 3 },
        { text: "No, I just want general information.", end: true },
      ],
    },
    3: {
      text: "Great! Let's start with a few questions about your drinking habits. How often do you usually drink?",
      options: [
        { text: "Daily", score: 5, next: 4 },
        { text: "Weekly", score: 4, next: 4 },
        { text: "Occasionally", score: 3, next: 4 },
        { text: "Rarely", score: 2, next: 4 },
        { text: "Never", score: 0, next: 7 },
      ],
    },
    4: {
      text: "In the past year, how many times have you had 4 (women) or 5 (men) or more drinks in a single day",
      options: [
        { text: "Never", score: 0, next: 5 },
        { text: "Less than once a month", score: 1, next: 5 },
        { text: "1–3 times a month", score: 2, next: 5 },
        { text: "1–2 times a week", score: 3, next: 5 },
        { text: "More than twice a week", score: 4, next: 5 },
      ],
    },
    5: {
      text: "On average, how many days per week do you drink alcohol?",
      options: [
        { text: "0 days", score: 0, next: 6 },
        { text: "1–2 days", score: 1, next: 6 },
        { text: "3–4 days", score: 2, next: 6 },
        { text: "5+ days", score: 3, next: 6 },
      ],
    },
    6: {
      text: "When you drink, how many drinks do you usually have in one sitting?",
      options: [
        { text: "1 drink", score: 0, next: 7 },
        { text: "2–3 drinks", score: 1, next: 7 },
        { text: "4–5 drinks", score: 2, next: 7 },
        { text: "6+ drinks", score: 3, next: 7 },
      ],
    },
    7: {
      text: "Now, I’d like to ask a few questions about alcohol and substance use. Just answer honestly. there are no right or wrong answers! Have you ever ridden in a car driven by someone (including yourself) who was high or had been using alcohol or drugs?",
      options: [
        { text: "Yes", score: 1, next: 8 },
        { text: "No", score: 0, next: 8 },
      ],
    },
    8: {
      text: "Do you ever use alcohol or drugs to relax, feel better about yourself, or fit in?",
      options: [
        { text: "Yes", score: 1, next: 9 },
        { text: "No", score: 0, next: 9 },
      ],
    },
    9: {
      text: "Do you ever use alcohol or drugs when you are alone?",
      options: [
        { text: "Yes", score: 1, next: 10 },
        { text: "No", score: 0, next: 10 },
      ],
    },
    10: {
      text: "Do you ever forget things you did while using alcohol or drugs?",
      options: [
        { text: "Yes", score: 1, next: 11 },
        { text: "No", score: 0, next: 11 },
      ],
    },
    11: {
      text: "Have your family or friends ever told you that you should cut down on your drinking or drug use?",
      options: [
        { text: "Yes", score: 1, next: 12 },
        { text: "No", score: 0, next: 12 },
      ],
    },
    12: {
      text: "Have you ever gotten into trouble while you were using alcohol or drugs?",
      options: [
        { text: "Yes", score: 1, next: 13 },
        { text: "No", score: 0, next: 13 },
      ],
    },
    13: {
      text: "Thanks for sharing. What best describes your thoughts on alcohol and health?",
      options: [
        {
          text: " I think alcohol can be harmful, but I don’t know much about it",
          next: 14,
        },
        {
          text: " I know the risks but don’t feel personally affected",
          next: 14,
        },
        {
          text: " I’ve heard mixed information and want to learn more",
          next: 14,
        },
        { text: " I don’t think it’s a big deal for me", next: 14 },
        { text: " I actively try to drink less for health reasons", next: 14 },
      ],
    },
    14: {
      text: " Which of these statements feels most true for you?",
      options: [
        { text: " I’m already careful about my alcohol intake", next: 15 },
        { text: " I sometimes wonder if I should cut down", next: 15 },
        {
          text: " I don’t think about alcohol much, but I’m open to learning",
          next: 15,
        },
        {
          text: " I don’t see a reason to change my drinking habits",
          next: 15,
        },
        { text: " I want to cut back but don’t know where to start", next: 15 },
      ],
    },
    15: {
      text: " Based on what you've told me, would you be interested in exploring ways to build healthier habits around alcohol?",
      options: [
        { text: " Yes, that would be helpful", next: "result" },
        { text: " Maybe, I’m open to learning more", next: "result" },
        {
          text: " No, I just want general information for now",
          next: "result",
        },
      ],
    },
  };

  // Chat history adding function
  const addToChatHistory = (question, answer) => {
    setChatHistory((prev) => [...prev, { question, answer }]);
  }

  // Assessment response processing function
  const handleAssessmentAnswer = (option) => {
    addToChatHistory(assessmentSteps[assessmentStep].text, option.text);
    if (option.end) {
      setAssessmentEnded(true);
      return;
    }
    const newScore = assessmentScore + (option.score || 0);
    if (option.next === "result") {
      setAssessmentScore(newScore);
      setAssessmentStep("result");
    } else {
      setAssessmentScore(newScore);
      setAssessmentStep(option.next);
    }
  };

  // Assessment result calculation function (risk level and recommended action based on total score)
  const getRiskResult = () => {
    let riskLevel = "";
    let recommendation = "";
    if (assessmentScore <= 3) {
      riskLevel = "Low Risk (Safe Zone)";
      recommendation =
        "Provides general alcohol education and responsible drinking guidance";
    } else if (assessmentScore <= 7) {
      riskLevel = "Moderate Risk (Caution)";
      recommendation =
        "Guide to moderate drinking, dealing with peer pressure, and self-monitoring strategies";
    } else if (assessmentScore <= 12) {
      riskLevel = "High Risk (Intervention)";
      recommendation =
        "Suggestions for harmful drinking mitigation, stress management alternatives, and behavior change techniques";
    } else {
      riskLevel = "Severe Risk (Critical)";
      recommendation =
        "Recommend professional counseling, treatment programs, or referral to specialized services";
    }
    return { riskLevel, recommendation };
  };

  // Chat API call (including assessment score)
  const sendToFlask = async (userInput) => {
    const roleMapping = { ai: "ai", student: "student", doctor: "doctor" };
    const chatbotType = roleMapping[params.role] || "ai";

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userInput,
          chatbot_type: chatbotType,
          risk_score: assessmentScore,
        }),
      });
      const data = await res.json();
      if (data.bot_response) return data.bot_response;
      if (data.error) return `Error: ${data.error}`;
      return "Something went wrong.";
    } catch (err) {
      console.error(err);
      return "Request failed.";
    }
  };

  // When the user types a message, call the chat API and display a response.
  const handleAddMessage = async () => {
    if (!inputValue.trim()) return;
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

    const assistantResponse = await sendToFlask(newUserMessage.text);
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

  // Set the scroll down
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory, messages, loading]);

  const today = new Date().toLocaleDateString("en-US", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });

  return (
    <div className="grid md:grid-cols-[30%,auto] lg:grid-cols-[40%,auto] xl:grid-cols-[30%,auto]">
      {/* sidebar */}
      <div className="px-[15px] lg:px-[20px] xl:px-[40px] py-[40px]">
        <Image src="/logo.svg" width={182} height={40} alt="logo" />
        <div className="flex flex-col mt-[89px] justify-center items-center">
          <div className="mb-[80px]">
            <Image src="/sky.svg" width={132} height={44} alt="sky" />
          </div>
          <div>
            <Image
              src={`/${params.role}.svg`}
              width={245}
              height={329}
              alt={params.role}
            />
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div
        className="flex px-[20px] xl:px-[40px] py-[32px] flex-col md:h-screen justify-between bg-white flex-grow overflow-y-auto"
        ref={chatContainerRef}
      >
        
        {/* Date of today */}
        <div className="flex items-center pb-[40px] gap-2 px-4">
          <div className="h-[1px] w-[40%] flex-grow bg-[#D9D9D9]"></div>
          <p className="flex-shrink-0">{today}</p>
          <div className="h-[1px] w-[40%] flex-grow-0 bg-[#D9D9D9]"></div>
        </div>

        {/* Chat History */}
        <div className="space-y-2">
          {chatHistory.map((entry, index) => (
            <div key={index}>
              <p className="bg-[#E1E6F9] text-[#333] text-sm px-4 py-2 rounded-2xl shadow-sm w-fit">
                {entry.question}
              </p>
              <div className="flex justify-end mt-2">
                <button
                  className="bg-[#EDEDE8] text-black text-sm px-4 py-2 rounded-2xl shadow-sm w-fit"
                  disabled
                >
                  {entry.answer}
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Action UI : assessment or chatting UI */}
        { !assessmentEnded && (
          <div className="p-6 bg-gray-50 rounded-lg shadow-md flex flex-col justify-start h-full">
            {assessmentStep !== "result" ? (
              <>
              {/* Assessment UI (all roles only): Display question and option until the assessment is completed */}
                <p className="bg-[#E1E6F9] text-[#333] text-sm font-semibold px-4 py-2 rounded-2xl shadow-sm w-fit">
                  {assessmentSteps[assessmentStep].text}
                </p>
                <div className="flex flex-col gap-1 mb-4 items-center">
                  {assessmentSteps[assessmentStep].options.map(
                    (option, index) => (
                      <div className="flex justify-end mt-2">
                        <button
                          key={index}
                          onClick={() => handleAssessmentAnswer(option)}
                          className="bg-[#F0EAD6] hover:bg-[#D6C4A1] text-[#333] text-sm font-semibold px-4 py-2 rounded-2xl shadow-sm w-fit"
                        >
                          {option.text}
                        </button>
                      </div>
                    )
                  )}
                </div>
              </>
            ) : (
              (() => {
                {/* Chatting UI after assessment : only show after assessment */}
                const { riskLevel, recommendation } = getRiskResult();
                return (
                  <>
                    <div className=" flex-grow overflow-y-auto custom-scrollbar">
                      <div className="flex flex-col gap-2">
                        {messages.map((msg) => {
                          const isAssistant = msg.type === "assistant";
                          const alignmentClass = isAssistant
                            ? "self-start"
                            : "self-end";
                          const bubbleClass = isAssistant
                            ? "bg-[#EEF2FD] text-black"
                            : "bg-[#F6F6F2] text-black";
                          return (
                            <div
                              key={msg.id}
                              className={`${alignmentClass} max-w-[85%] lg:max-w-[70%] mb-2`}
                            >
                              <div
                                className={`${bubbleClass} px-4 py-3 rounded-2xl text-sm`}
                              >
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

                    {/* chatting input area */}
                    <div className="py-[24px] px-[12px] lg:px-[24px] rounded-[20px] mt-6 border border-[#D9D9D9] bg-[#F6F6F2] flex items-center">
                      <input
                        type="text"
                        placeholder="What do you want to share today?"
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
                        <Image
                          src="/send.svg"
                          width={24}
                          height={24}
                          alt="send"
                        />
                      </button>
                    </div>

                    {/* bottom icon */}
                    <div className="flex items-center gap-[24px] mt-[12px]">
                      <Image src="/A.svg" width={24} height={24} alt="A" />
                      <Image src="/A2.svg" width={24} height={24} alt="A2" />
                      <Image
                        src="/smile.svg"
                        width={24}
                        height={24}
                        alt="smile"
                      />
                      <Image
                        src="/drive.svg"
                        width={24}
                        height={24}
                        alt="drive"
                      />
                      <Image
                        src="/lock.svg"
                        width={24}
                        height={24}
                        alt="lock"
                      />
                      <Image src="/pen.svg" width={24} height={24} alt="pen" />
                      <Image
                        src="/vertical.svg"
                        width={24}
                        height={24}
                        alt="vertical"
                      />
                    </div>
                  </>
                );
              })()
            )}
          </div>
        )}

        {/* when reject assessment */}
        {assessmentEnded && (
          <div className="p-6 bg-red-100 rounded-lg text-center">
            <p className="text-xl font-bold mb-2">Chat session ended.</p>
            <p>You chose not to participate in the assessment.</p>
          </div>
        )}
      </div>
    </div>
  );
}
