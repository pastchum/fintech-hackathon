"use client";

import { useState } from "react";

import { Input } from "@nextui-org/input";
import Image from "next/image";
import FacecardPopup from "@/components/FacecardPopup";

import eyeIcon from "@/icons/eye-open.png";
import eyeClosedIcon from "@/icons/eye-invisible.png";

export default function Home() {
  const [userID, setUserID] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [visible, setVisible] = useState<boolean>(false);

  const [overlayVisible, setOverlayVisible] = useState<boolean>(false);

  const handleSubmit = () => {
    setOverlayVisible(true);
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      {overlayVisible && <FacecardPopup />}

      <div className="flex flex-row justify-between w-full pt-20">
        <div>test</div>
        <div className="w-1/5 space-y-2 mt-32">
          <div className="text-2xl font-bold py-2 mt-32 pt-5">Client Login</div>
          Enter your Northern Trust credentials below to sign in. Please contact
          your relationship manager if you need to register.
          <Input
            label="UserID"
            type="UserID"
            value={userID}
            onChange={(e) => setUserID(e.target.value)}
          />
          <Input
            label="Password"
            type={visible ? "text" : "password"}
            value={password}
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
          <div className="p-1 text-slate-700 text-sm">Remember Me</div>
          <div className="py-2 flex justify-between">
            <button className="underline text-green-700 text-xs">
              Forgot Password?
            </button>
            <a className="underline text-green-700 text-xs" href="/Register">
              Register
            </a>
          </div>
          <button onClick={handleSubmit} className="w-full py-3">
            <div className="w-8/10 flex p-2 border bg-green-700 text-slate-50 flex align-center justify-center transition-transform transition scale-95 hover:scale-100 hover:bg-white hover:text-green-700">
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
