"use client";
import React, { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";
import Image from "next/image";

// 정확한 이미지 매핑
const roleImageMap = {
  ai: "/ai-chatbot.svg",
  doctor: "/doctor2.svg",
  student: "/student.svg",
};

export default function ChatBox() {
  const params = useParams(); // "ai", "student", "doctor"
  const chatContainerRef = useRef(null);

  // Dark mode state toggle
  const [isDarkMode, setIsDarkMode] = useState(false);

  // 아바타 이미지
  const avatarImageSrc = roleImageMap[params.role];

  // 초기 상태
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);

  // Assessment 상태
  const [assessmentSteps, setAssessmentSteps] = useState({
    text: "Loading assessment questions...",
    options: [],
  });
  const [assessmentScore, setAssessmentScore] = useState(0);
  const [assessmentEnded, setAssessmentEnded] = useState(false);
  const [assessmentCompleted, setAssessmentCompleted] = useState(false);
  const [assessmentAnswers, setAssessmentAnswers] = useState([]); // 모든 평가 답변 저장
  const [assessmentLoading, setAssessmentLoading] = useState(false); // 중복 클릭 방지
  const [lastClickTime, setLastClickTime] = useState(0); // 마지막 클릭 시간
  const processingRef = useRef(false); // 처리 중 플래그
  
  // Conversation context state
  const [conversationContext, setConversationContext] = useState({});
  
  // 페이지 로드 시 초기 평가 단계 로드
  useEffect(() => {
    getAssessmentStep("0");
  }, []);

  // Training 상태
  const [trainingSteps, setTrainingSteps] = useState([]);
  const [currentTrainingStep, setCurrentTrainingStep] = useState(0);
  const [trainingCompleted, setTrainingCompleted] = useState(false);

  // 채팅 기록 추가 함수
  const addToChatHistory = (question, answer) => {
    setChatHistory((prev) => [...prev, { question, answer }]);
  };

  // Assessment 답변 처리
  const handleAssessmentAnswer = (option) => {
    // useRef를 사용한 즉각적인 중복 클릭 방지
    if (processingRef.current) {
      return;
    }
    
    // 중복 클릭 방지 - 300ms 이내 재클릭 무시
    const now = Date.now();
    if (now - lastClickTime < 300) {
      return;
    }
    
    // 중복 클릭 방지
    if (assessmentLoading || assessmentCompleted) {
      return;
    }
    
    processingRef.current = true;
    setLastClickTime(now);
    setAssessmentLoading(true);
    console.log("handleAssessmentAnswer called with option:", option);
    addToChatHistory(assessmentSteps.text, option.text);
    
    // 선택한 답변 기록
    const answerRecord = {
      question: assessmentSteps.text,
      selectedOption: option.text,
      score: option.score || 0,
      timestamp: new Date().toISOString(),
      stepKey: assessmentSteps.key || `step_${assessmentAnswers.length + 1}`
    };
    setAssessmentAnswers(prev => [...prev, answerRecord]);
    
    if (option.end) {
      setAssessmentEnded(true);
      setAssessmentLoading(false);
      processingRef.current = false;
      return;
    }
    const newScore = assessmentScore + (option.score || 0);
    if (option.next === "result") {
      setAssessmentScore(newScore);
      setAssessmentCompleted(true);
      setAssessmentLoading(false);
      processingRef.current = false;
    } else {
      setAssessmentScore(newScore);
      console.log("Calling getAssessmentStep with key:", option.next);
      getAssessmentStep(option.next);
    }
  };

  // Assessment 단계 불러오기
  const getAssessmentStep = async (stepkey) => {
    console.log("getAssessmentStep called with key:", stepkey);
    try {
      console.log("Sending request to API endpoint");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/get_assessment_step`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stepKey: stepkey }),
      });
      console.log("API response status:", res?.status);
      
      if (res?.ok) {
        const data = await res.json();
        console.log("Received assessment step data:", data);
        setAssessmentSteps({...data, key: stepkey});
        setAssessmentLoading(false); // 로딩 완료
        processingRef.current = false; // 처리 완료
      } else {
        const errorText = res ? await res.text() : 'Network error';
        console.error("Failed to fetch next assessment step:", res?.status || 'No response', errorText);
        setAssessmentLoading(false); // 에러 시에도 로딩 해제
        processingRef.current = false; // 처리 완료
      }
    } catch (err) {
      console.error("Error fetching assessment data:", err);
      setAssessmentLoading(false); // 에러 시에도 로딩 해제
      processingRef.current = false; // 처리 완료
    }
  };

  // Training 질문/정답 데이터 로딩
  useEffect(() => {
    if (assessmentCompleted) {
      // Add initial AI message when assessment completes
      const initialMessage = {
        id: Date.now(),
        type: "assistant",
        text: "Let's try a quick example together. It's something that could easily happen in real life, just imagine how you might respond if it were you",
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
      
      // Add party scenario message after a short delay
      const scenarioMessage = {
        id: Date.now() + 1,
        type: "assistant",
        text: "You're at a party, hanging out with friends, when someone passes you a drink and says, \"Come on, just one won't hurt!\"",
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
      
      setMessages([initialMessage]);
      
      // Send scenario message after 2 seconds
      setTimeout(() => {
        setMessages(prev => [...prev, scenarioMessage]);
        // Set conversation context to track party scenario (1 for first scenario)
        setConversationContext({ party_scenario: 1 });
      }, 2000);
      
      const riskLevel =
        assessmentScore <= 3
          ? "low_risk"
          : assessmentScore <= 7
          ? "moderate_risk"
          : assessmentScore <= 12
          ? "high_risk"
          : "severe_risk";
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
      setTrainingCompleted(true);
    }
  };


  // 채팅 메시지 처리 (AI 채팅)
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
          conversation_context: {
            ...conversationContext,
            assessment_answers: assessmentAnswers,
            chat_history: messages.map(msg => ({
              type: msg.type,
              text: msg.text,
              timestamp: msg.timestamp
            }))
          },
        }),
      });
      
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ error: 'Network error' }));
        return `Error: ${errorData.error || `HTTP ${res.status}`}`;
      }
      
      const data = await res.json();
      return data.bot_response || `Error: ${data.error || "Unknown error"}`;
    } catch (err) {
      console.error("Chat request failed:", err);
      return "Sorry, I encountered an error. Please try again.";
    }
  };

  // 메시지 보내기
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
    
    // Handle scenario progression
    if (conversationContext.party_scenario === 1) {
      // After first scenario, send second scenario
      setTimeout(() => {
        const secondScenarioMessage = {
          id: Date.now() + 2,
          type: "assistant",
          text: "Your friends say they're going to pre-game before the concert and ask if you're in. One says, 'It'll be more fun if you're not the only sober one.'",
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        };
        setMessages(prev => [...prev, secondScenarioMessage]);
        setConversationContext({ party_scenario: 2 });
      }, 2000);
    } else if (conversationContext.party_scenario === 2) {
      // After second scenario, send third scenario
      setTimeout(() => {
        const thirdScenarioMessage = {
          id: Date.now() + 3,
          type: "assistant",
          text: "You're on a first date. They order drinks and say, 'Let's have some fun tonight!' but you weren't planning to drink.",
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        };
        setMessages(prev => [...prev, thirdScenarioMessage]);
        setConversationContext({ party_scenario: 3 });
      }, 2000);
    }
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
    // Apply the dark class conditionally at the top-level container
    <div className={isDarkMode ? "dark min-h-screen" : "min-h-screen"}>
      {/* A wrapper that uses dark mode classes */}
      <div className="grid md:grid-cols-[30%,auto] lg:grid-cols-[40%,auto] xl:grid-cols-[30%,auto] min-h-screen bg-white dark:bg-gray-900 text-black dark:text-white">
        {/* Sidebar */}
        <div className="px-[15px] lg:px-[20px] xl:px-[40px] py-[40px] bg-white dark:bg-gray-800">
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
          className="flex flex-col px-[20px] xl:px-[40px] py-[32px] md:h-screen dark:bg-gray-900 overflow-y-auto"
          ref={chatContainerRef}
        >
          {/* Dark/Light Mode Toggle */}
          <div className="flex justify-end mb-4">
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              className="px-3 py-1 rounded-md bg-gray-200 dark:bg-gray-700 text-black dark:text-white text-sm"
            >
              {isDarkMode ? "Light Mode" : "Dark Mode"}
            </button>
          </div>

          {/* Date Divider */}
          <div className="flex items-center pb-[40px] gap-2 px-4">
            <div className="h-[1px] w-[40%] bg-[#D9D9D9] dark:bg-gray-700" />
            <p className="flex-shrink-0">{today}</p>
            <div className="h-[1px] w-[40%] bg-[#D9D9D9] dark:bg-gray-700" />
          </div>

          {/* Chat History (Assessment / Training) */}
          <div className="space-y-2">
            {chatHistory.map((entry, idx) => (
              <div key={idx}>
                <p className="bg-[#E1E6F9] dark:bg-[#2F3147] text-black dark:text-white text-sm px-4 py-2 rounded-2xl shadow-sm w-fit">
                  {entry.question}
                </p>
                <div className="flex justify-end mt-2">
                  <button
                    className="bg-[#EDEDE8] dark:bg-gray-600 text-black dark:text-white text-sm px-4 py-2 rounded-2xl shadow-sm w-fit"
                    disabled
                  >
                    {entry.answer}
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Assessment UI */}
          {!assessmentEnded && !assessmentCompleted && (
            <div className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg shadow-md my-4">
              <p className="font-semibold text-sm px-4 py-2 bg-[#E1E6F9] dark:bg-[#3B3F52] text-black dark:text-white rounded-2xl w-fit">
                {assessmentSteps.text}
              </p>
              {assessmentSteps.options.map((opt, idx) => (
                <div key={idx} className="mt-2 flex justify-end">
                  <button
                    onClick={() => handleAssessmentAnswer(opt)}
                    disabled={assessmentLoading}
                    className={`px-4 py-2 rounded-2xl shadow-sm text-black dark:text-white ${
                      assessmentLoading 
                        ? 'bg-gray-300 dark:bg-gray-700 cursor-not-allowed opacity-50' 
                        : 'bg-[#F0EAD6] hover:bg-[#D6C4A1] dark:bg-gray-600 dark:hover:bg-gray-500'
                    }`}
                  >
                    {assessmentLoading ? '로딩 중...' : opt.text}
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Training UI */}
          {assessmentCompleted && !trainingCompleted && trainingSteps.length > 0 && (
            <div className="p-6 bg-[#FAFAF5] dark:bg-gray-700 rounded-lg shadow-md my-4">
              <p className="font-semibold mb-4 bg-[#E1E6F9] dark:bg-[#3B3F52] text-black dark:text-white px-4 py-2 rounded-2xl w-fit">
                {trainingSteps[currentTrainingStep].question}
              </p>
              {trainingSteps[currentTrainingStep].options.map((opt, idx) => (
                <button
                  key={idx}
                  onClick={() => handleTrainingAnswer(opt.correct)}
                  className="bg-[#F0EAD6] hover:bg-[#D6C4A1] dark:bg-gray-600 dark:hover:bg-gray-500 text-black dark:text-white px-4 py-2 rounded-2xl shadow-sm m-2"
                >
                  {opt.text}
                </button>
              ))}
            </div>
          )}

          {/* AI Chat UI */}
          {assessmentCompleted && (trainingCompleted || messages.length > 0) && (
            <>
              <div className="space-y-2">
                {messages.map((msg, idx) => (
                  <div key={idx}>
                    {msg.type === "assistant" ? (
                      <p className="bg-[#E1E6F9] dark:bg-[#2F3147] text-black dark:text-white text-sm px-4 py-2 rounded-2xl shadow-sm w-fit">
                        {msg.text}
                      </p>
                    ) : (
                      <div className="flex justify-end mt-2">
                        <p className="bg-[#EDEDE8] dark:bg-gray-600 text-black dark:text-white text-sm px-4 py-2 rounded-2xl shadow-sm w-fit">
                          {msg.text}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
                {loading && (
                  <p className="bg-[#E1E6F9] dark:bg-[#2F3147] text-black dark:text-white text-sm px-4 py-2 rounded-2xl shadow-sm w-fit">
                    Loading...
                  </p>
                )}
              </div>

              {/* Input Area */}
              <div className="py-[24px] px-[24px] rounded-[20px] border border-[#D9D9D9] dark:border-gray-600 bg-[#F6F6F2] dark:bg-gray-700 flex items-center mt-4">
                <input
                  type="text"
                  placeholder="What do you want to share today?"
                  className="flex-grow bg-transparent text-[16px] outline-none text-black dark:text-white"
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
            <div className="p-6 bg-red-100 dark:bg-red-700 rounded-lg text-center my-4">
              <p className="text-xl font-bold">Chat session ended.</p>
              <p>You chose not to participate in the assessment.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
