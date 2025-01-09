# backend/app/main.py

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
from app.scrape_utils import run_scraper, run_searchscraper
import tracemalloc
import json
import asyncio

## trace issue
tracemalloc.start()

app = FastAPI(title="ScrapeGraphAI Backend")


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

# @app.post('/searchgraphscrape')
# async def searchgraph_endpoint(request: SearchGraphScrapeRequest):
#     """
#     FastAPI endpoint to run the scraper with the given prompt and URL.
#     """
#     prompt = """List out any article regarding PERSON,
#     that contains any unsavoury news only regarding KEYWORD.
#     Return me the title of each article, and a brief description of each article.
#     Give me the link to each article in a separate field in JSON format. Skip all pdfs and think before you answer"""

#     # dictionaries of keywords
#     keyword_map = {
#         "Criminal and Legal Concerns" : [
#             "criminal record",
#             # "money laundering",
#             # "fraud",
#             # "tax evasion",
#             # "bribery",
#             # "corruption",
#             # "embezzlement",
#             # "insider trading",
#             # "regulatory violations"
#         ],
#         "Financial Mismanagement" :  [
#             "bankruptcy",
#             # "financial mismangement",
#             # "auditing irregularities",
#             # "conflict of interest"
#         ],
#         "Professional Integrity" : [
#             "ethics violation",
#             # "plagiarism",
#             # "dismissal",
#             # "professional misconduct"
#         ],
#         "Social and Reputational red flags" : [
#             "controversy",
#             # "dismissal",
#         ]
#     }

#     company_flags = [
#         "anti-money laundering violations",
#         "know your customer failures",
#         "foreign corrupt practices act breaches",
#         "GDPR violations"
#     ]

#     categories = {
#         "Criminal and Legal Concerns" : [],
#         "Financial Mismanagement" : [],
#         "Professional Integrity" : [],
#         "Social and Reputational red flags" : []
#     }

#     output = []

#     try:
#         # TODO
#         # unpack JSON here
#         company = request.companyName
        
#         # array of key value pairs, key is pos, value is name
#         key_appt_holders_info = request.appointmentHolders.items()

#         for role, name in key_appt_holders_info:
#             full_title = f"{name}, {role} of {company}"
#             # print(processed_name)
#             prompt_with_name = prompt.replace("PERSON", full_title)

#             for category, flaglist in keyword_map.items():
#                 for flag in flaglist:
#                     full_prompt = prompt_with_name.replace("KEYWORD", flag)
#                     # print(full_prompt)
#                     result = await run_searchscraper(prompt=full_prompt)
#                     categories[category].append(result)

#             output.append((full_title, categories))

#         # Transform data
#         result = {
#             full_title: {"Categories": categories}
#             for full_title, categories in output
#         }

#         # Convert to JSON
#         json_data = json.dumps(result, indent=4)

#         return json_data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post('/searchgraphscrape')
async def searchgraph_endpoint(request: SearchGraphScrapeRequest):
    """
    FastAPI endpoint to run the scraper with the given prompt and URL.
    """
    person_prompt = """List out any article regarding PERSON,
    that contains any unsavoury news only regarding KEYWORD.
    Return me the title of each article, and a brief description of each article.
    Give me the link to each article in a separate field in JSON format. Skip all pdfs and think before you answer."""

    company_prompt = """List out any article regarding COMPANY,
    that contains any unsavoury news only regarding KEYWORD.
    Return me the title of each article, and a brief description of each article.
    Give me the link to each article in a separate field in JSON format. Skip all pdfs and think before you answer."""

    # Dictionaries of person-related keywords
    keyword_map = {
        "Criminal and Legal Concerns" : [
            "criminal record",
            "money laundering",
            "fraud",
            "tax evasion",
            "bribery",
            "corruption",
            "embezzlement",
            "insider trading",
            "regulatory violations"
        ],
        "Financial Mismanagement" :  [
            "bankruptcy",
            "financial mismangement",
            "auditing irregularities",
            "conflict of interest"
        ],
        "Professional Integrity" : [
            "ethics violation",
            "plagiarism",
            "dismissal",
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
            # Create a unique categories dictionary for each full_title
            categories = {category: [] for category in keyword_map.keys()}

            full_title = f"{name}, {role} of {company}"
            prompt_with_name = person_prompt.replace("PERSON", full_title)

            for category, flaglist in keyword_map.items():
                for flag in flaglist:
                    full_prompt = prompt_with_name.replace("KEYWORD", flag)

                    # Run the scraper and collect results
                    result = await run_searchscraper(prompt=full_prompt)
                    # asyncio.sleep(2)

                    # Add the scraper result to the corresponding category
                    if result:  # Ensure the result is valid
                        categories[category].append(result)

            # Append the full_title and its categories to person_output
            person_output.append((full_title, categories))

        # Process company keywords
        company_results = {flag: [] for flag in company_flags}

        for flag in company_flags:
            full_prompt = company_prompt.replace("COMPANY", company).replace("KEYWORD", flag)

            # Run the scraper for each company keyword
            result = await run_searchscraper(prompt=full_prompt)
            # asyncio.sleep(2)

            # Add the scraper result to the corresponding company flag
            if result:  # Ensure the result is valid
                company_results[flag].append(result)

        # Transform person_output to JSON format
        person_result = {
            full_title: {"Categories": categories}
            for full_title, categories in person_output
        }

        # Combine person and company results
        final_result = {
            "Persons": person_result,
            company: company_results
        }

        return final_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
