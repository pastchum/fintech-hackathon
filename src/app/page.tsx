"use client";

import { useState } from "react";

import { Input } from "@nextui-org/input";
import Image from "next/image";

import eyeIcon from "@/icons/eye-open.png";
import eyeClosedIcon from "@/icons/eye-invisible.png";

export default function Home() {
  const [userID, setUserID] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [visible, setVisible] = useState<boolean>(false);

  const handleSubmit = () => {};

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <div className="flex flex-row justify-between w-full">
        <div>test</div>
        <div className="w-1/5 space-y-2 mt-32">
          <div className="text-2xl font-bold py-2">Client Login</div>
          Enter your Northern Trust credentials below to sign in. Please contact
          your relationship manager if you need to register.
          <Input
            label="UserID"
            type="UserID"
            onChange={(e) => setUserID(e.target.value)}
          />
          <Input
            label="Password"
            type={visible ? "text" : "password"}
            onChange={(e) => setPassword(e.target.value)}
            endContent={
              <button onClick={() => setVisible(!visible)}>
                {visible ? (
                  <Image
                    src={eyeClosedIcon}
                    className="w-5 h-5"
                    alt="Invisible"
                  ></Image>
                ) : (
                  <Image
                    src={eyeIcon}
                    className="w-5 h-5"
                    alt="Visible"
                  ></Image>
                )}
              </button>
            }
          />
          <div className="py-3 flex justify-between">
            <button type="checkbox"></button>
            <button className="underline text-green-700 text-xs">
              Forgot Password?
            </button>
          </div>
          <button onClick={handleSubmit} className="w-full py-3">
            <div className="w-8/10 flex p-2 border bg-green-700 text-slate-50 flex align-center justify-center">
              Log In
            </div>
          </button>
          <div className="justify-center p-10 text-green-700 underline">
            <a href="https://www.northerntrust.com/united-states/contact-us-corporate-overview">
              Passport Help
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
