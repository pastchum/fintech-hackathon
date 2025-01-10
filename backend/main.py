# backend/app/main.py

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
from app.scrape_utils import run_scraper, run_searchscraper
import tracemalloc
import json
import asyncio

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

## trace issue
tracemalloc.start()

app = FastAPI(title="ScrapeGraphAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    prompt: str
    url: str

class SearchGraphScrapeRequest(BaseModel):
    name: str
    companyName: str
    appointmentHolders: dict

class ScrapeResult:
    def __init__(self, summary, url):
        self.summary = summary
        self.url = url

@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    """
    FastAPI endpoint to run the scraper with the given prompt and URL.
    """
    try:
        result = await run_scraper(prompt=request.prompt, source_url=request.url)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/searchgraphscrape')
async def searchgraph_endpoint(request: SearchGraphScrapeRequest):
    """
    FastAPI endpoint to run the scraper with the given prompt and URL.
    """
    person_prompt = """List out any non pdf article regarding PERSON,
    that contains any unsavoury news only regarding KEYWORD.
    Consider only content from HTML pages, and exclude all links to PDFs or non-HTML resources.
    Return me the title of each article, and a brief description of each article.
    Give me the link to each article in a separate field in JSON format."""

    company_prompt = """List out any non pdf article regarding COMPANY,
    that contains any unsavoury news only regarding KEYWORD.
    Consider only content from HTML pages, and exclude all links to PDFs or non-HTML resources.
    Return me the title of each article, and a brief description of each article.
    Give me the link to each article in a separate field in JSON format. Return only content from HTML pages, and exclude all links to PDFs or non-HTML resources."""

    # Dictionaries of person-related keywords
    keyword_map = {
        "Criminal and Legal Concerns" : [
            "money laundering",
            "bribery",
            "corruption",
            "embezzlement",
        ],
        "Financial Mismanagement" :  [
            "bankruptcy",
        ],
        "Professional Integrity" : [
            "ethics violation",
            "professional misconduct"
        ],
        "Social and Reputational red flags" : [
            "controversy",
            "dismissal",
        ]
    }

    # Single-layer array for company keywords
    company_flags = [
        "anti-money laundering violations",
        "know your customer failures",
        "foreign corrupt practices act breaches",
        "GDPR violations"
    ]

    person_output = []
    company_output = []

    try:
        # Unpack request data
        company = request.companyName
        key_appt_holders_info = request.appointmentHolders.items()

        # Process appointment holders
        for role, name in key_appt_holders_info:
            try:
                # Create a unique categories dictionary for each full_title
                categories = {category: [] for category in keyword_map.keys()}

                full_title = f"{name}, {role} of {company}"
                prompt_with_name = person_prompt.replace("PERSON", full_title)

                for category, flaglist in keyword_map.items():
                    for flag in flaglist:
                        full_prompt = prompt_with_name.replace("KEYWORD", flag)

                        # Run the scraper and collect results
                        result = await run_searchscraper(prompt=full_prompt)
                        await asyncio.sleep(2)

                        # Add the scraper result to the corresponding category
                        if result:
                            categories[category].append(result)

                # Append the full_title and its categories to person_output
                person_output.append((full_title, categories))
            
            except Exception as e: 
                continue

        # Process company keywords
        company_results = {flag: [] for flag in company_flags}

        for flag in company_flags:
            try:
                full_prompt = company_prompt.replace("COMPANY", company).replace("KEYWORD", flag)

                # Run the scraper for each company keyword
                result = await run_searchscraper(prompt=full_prompt)
                await asyncio.sleep(2)

                # Add the scraper result to the corresponding company flag
                if result:  # Ensure the result is valid
                    company_results[flag].append(result)
            except Exception as e:
                continue

        if not person_output:
            person_output = [{"note": "No results found for appointment holders"}]

        if not company_results:
            company_results = {"note": "No results found for company keywords"}

        # Transform person_output to JSON format, skipping invalid or empty items
        person_result = {}

        for item in person_output:
            if isinstance(item, tuple) and len(item) == 2:
                full_title, categories = item

                # Ensure categories is a dictionary; skip if invalid
                if isinstance(categories, dict):
                    person_result[full_title] = {"Categories": categories}
                else:
                    # Log invalid categories for debugging but continue
                    print(f"Skipping invalid categories for {full_title}: {categories}")
            else:
                # Log invalid item structure for debugging but continue
                print(f"Skipping invalid item in person_output: {item}")

        # Default to an empty structure if no valid items are found
        if not person_result:
            person_result = {"note": "No results found for any person"}

        # Combine person and company results
        final_result = {
            "Persons": person_result,
            company: company_results
        }

        return final_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
