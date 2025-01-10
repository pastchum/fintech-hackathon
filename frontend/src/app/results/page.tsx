"use client";

import { Key, useState } from "react";

import RenderArticle, { Articles } from "@/components/RenderArticle";
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
} from "@nextui-org/dropdown";

export default function ResultsPage({
  Response,
}: {
  Response: ScraperResponse;
}) {
  const [showPeople, setShowPeople] = useState(true);
  const [showCompany, setShowCompany] = useState(true);
  const persons: Persons = Response.Persons;
  const company = Object.entries(Response)
    .filter(([key]) => key != "Persons")
    .reduce<Record<string, Categories>>((obj, [key, value]) => {
      obj[key] = value as Categories;
      return obj;
    }, {});

  const onSelect = (key: Key) => {
    if (key == "all") {
      setShowPeople(true);
      setShowCompany(true);
    } else if (key == "persons") {
      setShowPeople(true);
      setShowCompany(false);
    } else {
      setShowPeople(false);
      setShowCompany(true);
    }
  };

  const dropdownItems = [
    {
      key: "persons",
      label: "Persons",
    },
    {
      key: "company",
      label: "Company",
    },
    {
      key: "all",
      label: "All",
    },
  ];

  return (
    <div className="min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <div className="fixed flex flex-col">
        <div className="flex-row flex space-x-1 font-bold text-xl">
          <div className="text-green-700">SCRAPE</div>{" "}
          <div className="font-italics">Daddy</div>
        </div>
        <br />
        <div className="">
          Results for Company:{" "}
          {Object.entries(company).map(([name, categories]) => name)}
        </div>
      </div>
      <div className="flex flex-row-reverse w-full">
        <div className="w-2/5 flex flex-col">
          Showing:{" "}
          <Dropdown>
            <DropdownTrigger>
              <button className="border p-2 rounded-xl">
                {showCompany && showPeople
                  ? "All"
                  : showCompany
                  ? "Company"
                  : "KAH"}
              </button>
            </DropdownTrigger>
            <DropdownMenu
              aria-label="Dynamic Actions"
              items={dropdownItems}
              onAction={(key) => onSelect(key)}
            >
              {(item) => (
                <DropdownItem key={item.key}>{item.label}</DropdownItem>
              )}
            </DropdownMenu>
          </Dropdown>
        </div>

        <div className="m-5 border p-2 mt-32 rounded-xl w-3/5 max-h-3/5">
          <div className="overflow-y-auto ">
            {showPeople && (
              <div>
                {Object.entries(persons).map(([name, data]) => (
                  <div key={name}>
                    <div>{name}</div>
                    {Object.entries(data.categories).map(
                      ([category, articles]) => (
                        <div key={category} className="mt-4">
                          <div className="font-semibold">{category}</div>
                          {articles.length > 0 ? (
                            articles.map((article, index) => (
                              <RenderArticle key={index} Articles={article} />
                            ))
                          ) : (
                            <div className="ml-4 text-gray-500">
                              No articles available.
                            </div>
                          )}
                        </div>
                      )
                    )}
                  </div>
                ))}
                <br />
              </div>
            )}

            {showCompany && (
              <div>
                {Object.entries(company).map(([name, data]) => (
                  <div key={name}>
                    <div>{name}</div>
                    {Object.entries(data).map(([category, articles]) => (
                      <div key={category} className="mt-4">
                        <div className="font-semibold">{category}</div>
                        {articles.length > 0 ? (
                          articles.map((article, index) => (
                            <RenderArticle key={index} Articles={article} />
                          ))
                        ) : (
                          <div className="ml-4 text-gray-500">
                            No articles available.
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

const test = {
  Persons: {
    "Tim Cook, CEO of Apple": {
      Categories: {
        "Criminal and Legal Concerns": [
          {
            title: "Tim Cook accused of criminal activities",
            description:
              "Tim Cook has been involved in allegations of criminal misconduct.",
            link: "https://example.com/tim-cook-criminal",
          },
        ],
        "Financial Mismanagement": [],
        "Professional Integrity": [],
        "Social and Reputational red flags": [],
      },
    },
  },
  Apple: {
    "anti-money laundering violations": [
      {
        title: "Apple accused of AML violations",
        description: "Apple faces scrutiny for anti-money laundering failures.",
        link: "https://example.com/apple-aml",
      },
    ],
    "know your customer failures": [],
    "foreign corrupt practices act breaches": [],
    "GDPR violations": [],
  },
};

type ScraperResponse = {
  Persons: Persons;
} & { [companyName: string]: Categories };

type Categories = {
  [category: string]: Articles[]; // Category names map to arrays of articles
};

type Persons = {
  [name: string]: { categories: Categories };
};
