"use client";
import Image from "next/image";
import React, { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";

export default function ChatBox() {
  const params = useParams(); // 예상 역할: "ai", "student", "doctor"
  const chatContainerRef = useRef(null);

  // 모든 역할에서 초기 인삿말 메시지를 제거하여 평가 화면부터 보이도록 설정
  const initialMessages = [];

  // 채팅 관련 상태
  const [messages, setMessages] = useState(initialMessages);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);

  // 평가 상태 (모든 역할 전용)
  const [assessmentStep, setAssessmentStep] = useState(0);
  const [assessmentScore, setAssessmentScore] = useState(0);
  const [assessmentComplete, setAssessmentComplete] = useState(false);
  const [assessmentEnded, setAssessmentEnded] = useState(false);

  // 평가가 완료되거나 거부될 때까지 평가 UI를 표시
  const showAssessment = !assessmentComplete && !assessmentEnded;

  // 평가 플로우: 버튼을 통해 5개 질문에 답변하여 점수를 산출
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
        { text: "Daily (5 pts)", score: 5, next: 4 },
        { text: "Weekly (4 pts)", score: 4, next: 4 },
        { text: "Occasionally (3 pts)", score: 3, next: 4 },
        { text: "Rarely (2 pts)", score: 2, next: 4 },
        { text: "Never (0 pts) (Skip to CRAFFT)", score: 0, next: "result" },
      ],
    },
    4: {
      text: "How many drinks do you typically consume in one sitting?",
      options: [
        { text: "1-2 drinks (1 pt)", score: 1, next: 5 },
        { text: "3-4 drinks (2 pts)", score: 2, next: 5 },
        { text: "5-6 drinks (3 pts)", score: 3, next: 5 },
        { text: "More than 6 (4 pts)", score: 4, next: 5 },
        { text: "None (0 pts)", score: 0, next: 5 },
      ],
    },
    5: {
      text: "Have you ever experienced any negative consequences from drinking?",
      options: [
        { text: "Yes (4 pts)", score: 4, next: "result" },
        { text: "No (0 pts)", score: 0, next: "result" },
      ],
    },
  };

  // 평가 답변 처리 함수
  const handleAssessmentAnswer = (option) => {
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

  // 평가 결과 계산 함수 (총 점수에 따른 위험 수준과 권장 조치)
  const getRiskResult = () => {
    let riskLevel = "";
    let recommendation = "";
    if (assessmentScore <= 3) {
      riskLevel = "Low Risk (Safe Zone)";
      recommendation = "일반적인 알코올 교육 및 책임 음주 가이드 제공";
    } else if (assessmentScore <= 7) {
      riskLevel = "Moderate Risk (Caution)";
      recommendation = "절제 음주 방법, 또래 압력 대처, 자기 모니터링 전략 안내";
    } else if (assessmentScore <= 12) {
      riskLevel = "High Risk (Intervention)";
      recommendation = "해로운 음주 완화 방안, 스트레스 관리 대안, 행동 변화 기법 제안";
    } else {
      riskLevel = "Severe Risk (Critical)";
      recommendation = "전문가 상담, 치료 프로그램 혹은 전문 서비스 연계 권장";
    }
    return { riskLevel, recommendation };
  };

  // 채팅 API 호출 (평가 점수 포함)
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

  // 사용자가 메시지를 입력하면 채팅 API를 호출하고 응답을 표시
  const handleAddMessage = async () => {
    if (!inputValue.trim()) return;
    const newUserMessage = {
      id: Date.now(),
      type: "user",
      text: inputValue.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };
    setMessages((prev) => [...prev, newUserMessage]);
    setInputValue("");
    setLoading(true);

    const assistantResponse = await sendToFlask(newUserMessage.text);
    const newAssistantMessage = {
      id: Date.now() + 1,
      type: "assistant",
      text: assistantResponse,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };
    setMessages((prev) => [...prev, newAssistantMessage]);
    setLoading(false);
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const today = new Date().toLocaleDateString("en-US", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });

  return (
    <div className="grid md:grid-cols-[30%,auto] lg:grid-cols-[40%,auto] xl:grid-cols-[30%,auto] ">
      {/* 사이드바 */}
      <div className="px-[15px] lg:px-[20px] xl:px-[40px] py-[40px]">
        <Image src="/logo.svg" width={182} height={40} alt="logo" />
        <div className="flex flex-col mt-[89px] justify-center items-center">
          <div className="mb-[80px]">
            <Image src="/sky.svg" width={132} height={44} alt="sky" />
          </div>
          <div>
            <Image src={`/${params.role}.svg`} width={245} height={329} alt={params.role} />
          </div>
        </div>
      </div>

      {/* 메인 콘텐츠 영역 */}
      <div className="flex px-[20px] xl:px-[40px] py-[32px] flex-col md:h-screen justify-between bg-white flex-grow">
        <div className="flex items-center pb-[40px] gap-2 px-4">
          <div className="h-[1px] w-[40%] flex-grow bg-[#D9D9D9]"></div>
          <p className="flex-shrink-0">{today}</p>
          <div className="h-[1px] w-[40%] flex-grow-0 bg-[#D9D9D9]"></div>
        </div>

        {/* 평가 UI (모든 역할 전용): 평가가 완료되기 전까지 표시 */}
        {showAssessment && (
          <div className="p-6 bg-gray-50 rounded-lg shadow-md flex flex-col items-center">
            {assessmentStep !== "result" ? (
              <>
                <p className="text-lg font-semibold mb-4">
                  {assessmentSteps[assessmentStep].text}
                </p>
                <div className="flex flex-col gap-3">
                  {assessmentSteps[assessmentStep].options.map((option, index) => (
                    <button
                      key={index}
                      onClick={() => handleAssessmentAnswer(option)}
                      className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
                    >
                      {option.text}
                    </button>
                  ))}
                </div>
              </>
            ) : (
              (() => {
                const { riskLevel, recommendation } = getRiskResult();
                return (
                  <div className="text-center">
                    <p className="text-xl font-bold mb-2">Assessment Complete</p>
                    <p className="mb-2">
                      <strong>Total Score:</strong> {assessmentScore}
                    </p>
                    <p className="mb-2">
                      <strong>Risk Level:</strong> {riskLevel}
                    </p>
                    <p className="mb-4">
                      <strong>Recommendation:</strong> {recommendation}
                    </p>
                    <button
                      onClick={() => setAssessmentComplete(true)}
                      className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
                    >
                      Proceed to Chat
                    </button>
                  </div>
                );
              })()
            )}
          </div>
        )}

        {/* 평가 거부 시 */}
        {assessmentEnded && (
          <div className="p-6 bg-red-100 rounded-lg text-center">
            <p className="text-xl font-bold mb-2">Chat session ended.</p>
            <p>You chose not to participate in the assessment.</p>
          </div>
        )}

        {/* 평가 완료 후에만 채팅 UI 표시 */}
        {assessmentComplete && !assessmentEnded && (
          <>
            <div className="flex-grow overflow-y-auto custom-scrollbar" ref={chatContainerRef}>
              <div className="flex flex-col gap-2">
                {messages.map((msg) => {
                  const isAssistant = msg.type === "assistant";
                  const alignmentClass = isAssistant ? "self-start" : "self-end";
                  const bubbleClass = isAssistant
                    ? "bg-[#EEF2FD] text-black"
                    : "bg-[#F6F6F2] text-black";
                  return (
                    <div key={msg.id} className={`${alignmentClass} max-w-[85%] lg:max-w-[70%] mb-2`}>
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

            {/* 채팅 입력 영역 */}
            <div className="py-[24px] px-[12px] lg:px-[24px] rounded-[20px] border border-[#D9D9D9] bg-[#F6F6F2] flex items-center">
              <input
                type="text"
                placeholder="What do you want to share today?"
                className="flex-grow bg-transparent text-[16px] leading-[19px] outline-none"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter") handleAddMessage(); }}
              />
              <button
                onClick={handleAddMessage}
                className="bg-gradient-to-r w-[48px] h-[48px] from-[#28AAE1] via-[#0364B3] to-[#012B4D] text-white px-4 py-2 rounded-[12px] text-sm ml-2"
              >
                <Image src="/send.svg" width={24} height={24} alt="send" />
              </button>
            </div>

            {/* 하단 아이콘 */}
            <div className="flex items-center gap-[24px] mt-[12px]">
              <Image src="/A.svg" width={24} height={24} alt="A" />
              <Image src="/A2.svg" width={24} height={24} alt="A2" />
              <Image src="/smile.svg" width={24} height={24} alt="smile" />
              <Image src="/drive.svg" width={24} height={24} alt="drive" />
              <Image src="/lock.svg" width={24} height={24} alt="lock" />
              <Image src="/pen.svg" width={24} height={24} alt="pen" />
              <Image src="/vertical.svg" width={24} height={24} alt="vertical" />
            </div>
          </>
        )}
      </div>
    </div>
  );
}
