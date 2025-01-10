import RenderArticle, { Articles } from "@/components/RenderArticle";

export default function ResultsPage() {
  const persons = test.Persons;
  const company = Object.entries(test)
    .filter(([key]) => key != "Persons")
    .reduce<Record<string, Categories>>((obj, [key, value]) => {
      obj[key] = value as Categories;
      return obj;
    }, {});

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
      <div className="flex flex-row">
        <div>Showing:</div>
        <div className="m-5 border p-2 mt-32 rounded-xl w-3/5">
          <div className="overflow-y-auto ">
            {Object.entries(persons).map(([name, data]) => (
              <div key={name}>
                <div>{name}</div>
                {Object.entries(data.Categories).map(([category, articles]) => (
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
            <br />
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
  [companyName: string]: Company | Persons;
};

type Categories = {
  [category: string]: Articles[]; // Category names map to arrays of articles
};

type Persons = {
  [name: string]: {
    Categories: Categories;
  };
};

type Company = {
  [companyName: string]: Categories; // Company names map to their categories
};

type Test = {
  Persons: Persons;
  [companyName: string]: Company | Persons; // Dynamic keys for other companies
};
