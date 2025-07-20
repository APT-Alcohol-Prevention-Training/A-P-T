import { NextResponse } from "next/server";

export async function POST(req) {
  try {
    const { message, chatbot_type, risk_score, conversation_context } = await req.json();

    // Flask 서버로 요청
    const flaskRes = await fetch(`${process.env.BACKEND_API_URL || 'http://localhost:8000'}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, chatbot_type, risk_score, conversation_context }),
    });
    const data = await flaskRes.json();

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: "Server error" }, { status: 500 });
  }
}
