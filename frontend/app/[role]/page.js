"use client";
import React, { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";
import Image from "next/image";

// 정확한 이미지 매핑 (기존 사용 유지)
const roleImageMap = {
  ai: "/ai-chatbot.svg",
  doctor: "/doctor2.svg",
  student: "/student.svg",
};

export default function ChatBox() {
  const params = useParams(); // "ai", "student", "doctor"
  const chatContainerRef = useRef(null);

  // 아바타 이미지 (기존 이미지 유지)
  const avatarImageSrc = roleImageMap[params.role];

  // 초기 상태
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);

  // Assessment 상태
  const [assessmentSteps, setAssessmentSteps] = useState({
    text: "Hello! I'm Dr. Sky, here to provide guidance on alcohol awareness and healthier choices. Before we begin, can I ask a couple of quick questions? Are you between the ages of 18 and 20?",
    options: [
      { text: "Yes", next: "1" },
      { text: "No", next: "confirm_continue" },
    ],
  });
  const [assessmentScore, setAssessmentScore] = useState(0);
  const [assessmentEnded, setAssessmentEnded] = useState(false);
  const [assessmentCompleted, setAssessmentCompleted] = useState(false);

  // Training 상태 (추가 구현)
  const [trainingSteps, setTrainingSteps] = useState([]);
  const [currentTrainingStep, setCurrentTrainingStep] = useState(0);
  const [trainingCompleted, setTrainingCompleted] = useState(false);

  // 채팅 기록 추가 함수
  const addToChatHistory = (question, answer) => {
    setChatHistory((prev) => [...prev, { question, answer }]);
  };

  // Assessment 답변 처리
  const handleAssessmentAnswer = (option) => {
    addToChatHistory(assessmentSteps.text, option.text);
    if (option.end) {
      setAssessmentEnded(true);
      return;
    }
    const newScore = assessmentScore + (option.score || 0);
    if (option.next === "result") {
      setAssessmentScore(newScore);
      setAssessmentCompleted(true);
    } else {
      setAssessmentScore(newScore);
      getAssessmentStep(option.next);
    }
  };

  // Assessment 단계 불러오기
  const getAssessmentStep = async (stepkey) => {
    try {
      const res = await fetch("http://34.68.0.228:8080/api/get_assessment_step", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stepKey: stepkey }),
      });
      if (res.ok) {
        const data = await res.json();
        setAssessmentSteps(data);
      } else {
        console.error("Failed to fetch next assessment step");
      }
    } catch (err) {
      console.error("Error fetching assessment data:", err);
    }
  };

  // Training 질문/정답 데이터 로딩 (Assessment 완료 후)
  useEffect(() => {
    if (assessmentCompleted) {
      const riskLevel =
        assessmentScore <= 3 ? "low_risk" :
        assessmentScore <= 7 ? "moderate_risk" :
        assessmentScore <= 12 ? "high_risk" : "severe_risk";
      fetch(`/training_data.json`)
        .then((res) => res.json())
        .then((data) => {
          setTrainingSteps(data[riskLevel] || []);
          setCurrentTrainingStep(0);
        })
        .catch((error) => console.error("Training data load error:", error));
    }
  }, [assessmentCompleted, assessmentScore]);

  // Training 질문 답변 처리 함수
  const handleTrainingAnswer = (isCorrect) => {
    if (isCorrect) {
      alert("Correct! 🎉");
    } else {
      alert("Not quite! 🚫");
    }
    if (currentTrainingStep < trainingSteps.length - 1) {
      setCurrentTrainingStep((prev) => prev + 1);
    } else {
      setTrainingCompleted(true); // Training 완료 처리
    }
  };

  // Assessment 점수 기반 Risk 결과 계산 함수
  const getRiskResult = () => {
    if (assessmentScore <= 3) {
      return { riskLevel: "Low Risk (Safe Zone)", recommendation: "General education" };
    } else if (assessmentScore <= 7) {
      return { riskLevel: "Moderate Risk (Caution)", recommendation: "Moderate drinking strategies" };
    } else if (assessmentScore <= 12) {
      return { riskLevel: "High Risk (Intervention)", recommendation: "Harm reduction" };
    } else {
      return { riskLevel: "Severe Risk (Critical)", recommendation: "Professional help" };
    }
  };

  // 채팅 메시지 처리 함수 (AI 채팅 시작 후)
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
      return data.bot_response || `Error: ${data.error || "Unknown error"}`;
    } catch (err) {
      console.error(err);
      return "Request failed.";
    }
  };

  // 실제 메시지 보내기 (AI 채팅 시 사용)
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

  // 채팅 스크롤 자동 조정
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory, messages, loading]);

  const today = new Date().toLocaleDateString("en-US", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });

  useEffect(() => {
    console.log("Training completed?", trainingCompleted);
  }, [trainingCompleted]);

  return (
    <div className="grid md:grid-cols-[30%,auto] lg:grid-cols-[40%,auto] xl:grid-cols-[30%,auto]">
      {/* Sidebar with Avatar Image */}
      <div className="px-[15px] lg:px-[20px] xl:px-[40px] py-[40px]">
        <Image src="/logo.svg" width={182} height={40} alt="logo" />
        <div className="flex flex-col mt-[89px] justify-center items-center">
          <div className="mb-[80px]">
            <Image src="/sky.svg" width={132} height={44} alt="sky" />
          </div>
          <div>
            <Image src={avatarImageSrc} width={245} height={329} alt={params.role} />
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div
        className="flex flex-col px-[20px] xl:px-[40px] py-[32px] md:h-screen bg-white overflow-y-auto"
        ref={chatContainerRef}
      >
        <div className="flex items-center pb-[40px] gap-2 px-4">
          <div className="h-[1px] w-[40%] bg-[#D9D9D9]" />
          <p className="flex-shrink-0">{today}</p>
          <div className="h-[1px] w-[40%] bg-[#D9D9D9]" />
        </div>

        {/* Chat History (Assessment / Training) */}
        <div className="space-y-2">
          {chatHistory.map((entry, idx) => (
            <div key={idx}>
              <p className="bg-[#E1E6F9] text-sm px-4 py-2 rounded-2xl shadow-sm w-fit">
                {entry.question}
              </p>
              <div className="flex justify-end mt-2">
                <button className="bg-[#EDEDE8] text-sm px-4 py-2 rounded-2xl shadow-sm w-fit" disabled>
                  {entry.answer}
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Assessment UI */}
        {!assessmentEnded && !assessmentCompleted && (
          <div className="p-6 bg-gray-50 rounded-lg shadow-md">
            <p className="font-semibold text-sm px-4 py-2 bg-[#E1E6F9] rounded-2xl w-fit">
              {assessmentSteps.text}
            </p>
            {assessmentSteps.options.map((opt, idx) => (
              <div key={idx} className="mt-2 flex justify-end">
                <button
                  onClick={() => handleAssessmentAnswer(opt)}
                  className="bg-[#F0EAD6] hover:bg-[#D6C4A1] px-4 py-2 rounded-2xl shadow-sm"
                >
                  {opt.text}
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Training UI */}
        {assessmentCompleted && !trainingCompleted && trainingSteps.length > 0 && (
          <div className="p-6 bg-[#FAFAF5] rounded-lg shadow-md">
            <p className="font-semibold mb-4 bg-[#E1E6F9] px-4 py-2 rounded-2xl w-fit">
              {trainingSteps[currentTrainingStep].question}
            </p>
            {trainingSteps[currentTrainingStep].options.map((opt, idx) => (
              <button
                key={idx}
                onClick={() => handleTrainingAnswer(opt.correct)}
                className="bg-[#F0EAD6] hover:bg-[#D6C4A1] px-4 py-2 rounded-2xl shadow-sm m-2"
              >
                {opt.text}
              </button>
            ))}
          </div>
        )}

        {/* AI Chat UI */}
        {assessmentCompleted && (trainingCompleted || messages.length > 0) && (
          <>
            {/* 간단하게 메시지 렌더링 */}
            <div>
              {messages.map((msg, idx) => (
                <p key={idx} className="text-sm">
                  {msg.type}: {msg.text}
                </p>
              ))}
              {loading && <p className="text-sm">Loading...</p>}
            </div>

            {/* Input Area */}
            <div className="py-[24px] px-[24px] rounded-[20px] border border-[#D9D9D9] bg-[#F6F6F2] flex items-center mt-4">
              <input
                type="text"
                placeholder="What do you want to share today?"
                className="flex-grow bg-transparent text-[16px] outline-none"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleAddMessage()}
              />
              <button
                onClick={handleAddMessage}
                className="bg-gradient-to-r w-[48px] h-[48px] from-[#28AAE1] via-[#0364B3] to-[#012B4D] text-white px-4 py-2 rounded-[12px] ml-2"
              >
                <Image src="/send.svg" width={24} height={24} alt="send" />
              </button>
            </div>

            {/* Bottom Icons */}
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

        {/* Rejected Assessment UI */}
        {assessmentEnded && (
          <div className="p-6 bg-red-100 rounded-lg text-center">
            <p className="text-xl font-bold">Chat session ended.</p>
            <p>You chose not to participate in the assessment.</p>
          </div>
        )}
      </div>
    </div>
  );
}
