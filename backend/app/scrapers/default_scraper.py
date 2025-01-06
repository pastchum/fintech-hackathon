import sys
import json
from scrapegraphai.graphs import SmartScraperGraph
from app.config import OPENAI_API_KEY

#this is the default scraper that will be called, this can be used as a template for other scrapers
def main():
    input_data = json.loads(sys.argv[1])
    prompt = input_data["prompt"]
    source_url = input_data["source_url"]

    graph_config = {
        "llm": {
            "api_key": OPENAI_API_KEY,
            "model": "openai/gpt-4o-mini",
        },
    }

    smart_scraper_graph = SmartScraperGraph(
        prompt=prompt,
        source=source_url,
        config=graph_config,
    )

    try:
        result = smart_scraper_graph.run()
        print(json.dumps(result))
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
