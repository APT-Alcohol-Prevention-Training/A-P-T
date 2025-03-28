import { NextResponse } from "next/server";

export async function POST(req) {
  try {
    const { message, chatbot_type } = await req.json();

    // Flask 서버로 요청
    const flaskRes = await fetch("http://34.68.0.228:8080/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, chatbot_type }),
    });
    const data = await flaskRes.json();

    return NextResponse.json(data);
  } catch (error) {
    console.error("Error in /api/chat route:", error);
    return NextResponse.json({ error: "!!Server error!!" }, { status: 500 });
  }
}
