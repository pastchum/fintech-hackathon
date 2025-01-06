from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.utils.scraper_manager import ScraperManager

app = FastAPI(title="ScrapeGraphAI Backend")


class ScrapeRequest(BaseModel):
    prompt: str
    url: str
    scraper_type: str = "default"  # Optional field to select different scrapers


@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    """
    FastAPI endpoint to run the scraper with the given prompt, URL, and scraper type.
    """
    try:
        scraper_manager = ScraperManager(request.scraper_type)
        result = await scraper_manager.run_scraper(prompt=request.prompt, source_url=request.url)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
