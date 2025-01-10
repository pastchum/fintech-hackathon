"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/router";

import { Input } from "@nextui-org/input";

type AppointmentHolders = {
  CEO: string;
  COO: string;
  CFO: string;
} & {
  [key: string]: string;
};

type formType = {
  name: string;
  companyName: string;
  appointmentHolders: AppointmentHolders;
};

export default function Register() {
  const [company, setCompany] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [CEO, setCEO] = useState<string>("");
  const [COO, setCOO] = useState<string>("");
  const [CFO, setCFO] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({});

  const [fields, setFields] =
    useState<{ id: number; name: string; position: string }[]>();

  const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setLoading(true);

    var additional: { [key: string]: string } = {};

    fields?.map((field, index) => {
      additional = { ...additional, [field.position]: field.name };
    });

    const AppointmentHolders: AppointmentHolders = {
      CEO: CEO,
      COO: COO,
      CFO: CFO,
      ...additional,
    };

    const formSubmit: formType = {
      name: name,
      companyName: company,
      appointmentHolders: AppointmentHolders,
    };

    console.log(formSubmit);

    try {
      const response = await fetch("http://127.0.0.1:8000/searchgraphscrape", {
        body: JSON.stringify(formSubmit),
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Error sending to backend");
      }
      const jsonData = response.json();
      setData(jsonData);
    } catch (e) {
      console.error("Error submitting form: ", e);
      alert("Error");
    } finally {
      console.log(data);
    }
  };

  const addField = () => {
    setFields((prevFields) =>
      prevFields
        ? [...prevFields, { id: prevFields.length, name: "", position: "" }]
        : [{ id: 0, name: "", position: "" }]
    );
  };

  const handleFieldChange = (id: number, key: string, value: string) => {
    setFields((prevFields) =>
      prevFields?.map((field) =>
        field.id === id ? { ...field, [key]: value } : field
      )
    );
  };

  return (
    <div className="items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <div className="flex flex-row justify-between w-full">
        <div></div>
        <form className="flex flex-col space-y-3">
          <div className="text-2xl font-bold py-2 pt-5">Register</div>
          <div>
            Please input your details so you can register for an account.
          </div>
          <Input
            label="Name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <Input
            label="Company Name"
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
          />

          <div className="font-bold p-2 border rounded-xl space-y-3">
            Key Appointment Holders
            <div className="flex flex-row space-x-2">
              <Input label="CEO" type="text" disabled={true} />
              <Input
                label="Name"
                type="text"
                value={CEO}
                onChange={(e) => setCEO(e.target.value)}
              />
            </div>
            <div className="flex flex-row space-x-2">
              <Input label="COO" type="text" disabled={true} />
              <Input
                label="Name"
                type="text"
                value={COO}
                onChange={(e) => setCOO(e.target.value)}
              />
            </div>
            <div className="flex flex-row space-x-2">
              <Input label="CFO" type="text" disabled={true} />
              <Input
                label="Name"
                type="text"
                value={CFO}
                onChange={(e) => setCFO(e.target.value)}
              />
            </div>
            {fields &&
              fields.map((field, index) => {
                return (
                  <div key={field.id} className="flex flex-row space-x-2">
                    <Input
                      label="Position"
                      type="text"
                      value={field.position}
                      onChange={(e) =>
                        handleFieldChange(field.id, "position", e.target.value)
                      }
                    />
                    <Input
                      label="Name"
                      type="text"
                      value={field.name}
                      onChange={(e) =>
                        handleFieldChange(field.id, "name", e.target.value)
                      }
                    />
                  </div>
                );
              })}
            <button
              className={`${
                fields &&
                !fields[fields.length - 1].name &&
                !fields[fields.length - 1].position
                  ? "text-slate-500"
                  : "text-green-700"
              } text-xs m-2`}
              onClick={addField}
              disabled={
                fields &&
                !fields[fields.length - 1].name &&
                !fields[fields.length - 1].position
              }
            >
              Add Appointment Holder
            </button>
          </div>
          <button
            type="submit"
            onClick={(e) => handleSubmit(e)}
            className="w-full py-3"
          >
            <div className="w-8/10 flex p-2 border bg-green-700 text-slate-50 flex align-center transition-transform transition scale-95 hover:scale-100 hover:bg-white hover:text-green-700 justify-center">
              Register
            </div>
          </button>
        </form>
      </div>
    </div>
  );
}
