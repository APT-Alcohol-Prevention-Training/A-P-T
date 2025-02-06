import React, { useState } from "react";
import Image from "next/image";
import Link from "next/link";

const roles = [
  {
    id: "ai",
    name: "ai",
    image: "/ai.svg",
    alt: "ai",
  },
  {
    id: "doctor",
    name: "doctor",
    image: "/doctor.svg",
    alt: "doctor",
  },
  {
    id: "student",
    name: "student",
    image: "/student.svg",
    alt: "student",
  },
];

const ChooseAvatar = () => {
  const [selected, setSelected] = useState("");

  const handleSelection = (roleId) => {
    setSelected(roleId);
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

        <div className="flex flex-col justify-center items-center">
          <Link href={selected ? `/${selected}` : "#"}>
            <p
              className={`mt-12 flex items-center mb-8 text-2xl leading-7 font-bold text-white px-10 py-4 gap-2 rounded-full ${
                selected
                  ? "bg-gradient-to-r from-[#28AAE1] via-[#0364B3] to-[#012B4D] hover:opacity-90"
                  : "bg-[#C9C7C7] cursor-not-allowed"
              }`}
              onClick={(e) => { if (!selected) e.preventDefault(); }}
            >
              Carry On
              <Image src="/arrow-right.svg" width={28} height={28} alt="Arrow Right" />
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ChooseAvatar;
