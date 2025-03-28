"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

const roles = [
  {
    id: "ai",
    name: "ai",
    image: "/ai-chatbot.svg",
    alt: "ai",
  },
  {
    id: "doctor",
    name: "doctor",
    image: "/doctor2.svg",
    alt: "doctor",
  },
  {
    id: "student",
    name: "student",
    image: "/student.svg",
    alt: "student",
  },
];

export default function ChooseAvatar() {
  const router = useRouter();

  useEffect(() => {
    const randomIndex = Math.floor(Math.random() * roles.length);
    const selectedRole = roles[randomIndex].id;
    router.push(`/${selectedRole}`);
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-[#F6F6F2]">
      <p className="text-xl font-semibold">Redirecting...</p>
    </div>
  );
}
