"use client";

import { useState, useEffect } from "react";

import { Input } from "@nextui-org/input";
import Image from "next/image";

import eyeIcon from "@/icons/eye-open.png";
import eyeClosedIcon from "@/icons/eye-invisible.png";
import FacecardPopup from "@/components/FacecardPopup";

export default function Register() {
  const [userID, setUserID] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [passwordCheck, setPasswordCheck] = useState<string>("");
  const [passwordMatch, setPasswordMatch] = useState<boolean>(true);

  const [visible, setVisible] = useState<boolean>(false);

  const [overlayVisible, setOverlayVisible] = useState<boolean>(false);

  const handleSubmit = () => {
    setOverlayVisible(true);
  };

  useEffect(() => {
    if ((!password && !passwordCheck) || password == passwordCheck)
      setPasswordMatch(true);
    else setPasswordMatch(false);
  }, [password, passwordCheck]);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      {overlayVisible && <FacecardPopup />}
      <div className="flex flex-row justify-between w-full pt-20">
        <div className="flex flex-col space-y-3">
          <div className="text-2xl font-bold py-2 mt-32 pt-5">Register</div>
          <div>
            Please input your details so you can register for an account.
          </div>
          <Input
            label="Name"
            type="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
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
          <Input
            label="Re-enter Password"
            type={visible ? "text" : "password"}
            value={passwordCheck}
            onChange={(e) => setPasswordCheck(e.target.value)}
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
          {!passwordMatch && (
            <div className="text-red-700 text-sm">Passwords do not match</div>
          )}
          <button onClick={handleSubmit} className="w-full py-3">
            <div className="w-8/10 flex p-2 border bg-green-700 text-slate-50 flex align-center transition-transform transition scale-95 hover:scale-100 hover:bg-white hover:text-green-700 justify-center">
              Register
            </div>
          </button>
        </div>
      </div>
    </div>
  );
}
