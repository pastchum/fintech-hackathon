# backend/app/main.py

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
from app.scrape_utils import run_scraper, run_searchscraper
import tracemalloc
## trace issue
tracemalloc.start()

app = FastAPI(title="ScrapeGraphAI Backend")


class ScrapeRequest(BaseModel):
    prompt: str
    url: str

class SearchGraphScrapeRequest(BaseModel):
    prompt: str

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
    try:
        result = await run_searchscraper(prompt=request.prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))