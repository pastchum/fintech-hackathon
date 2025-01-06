import sys
import json
import time
from scrapegraphai.graphs import SearchGraph
sys.path.append('/Users/kaungzinye/Documents/SWE/fintech-hackathon/backend')
from app.config import OPENAI_API_KEY

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

    search_scraper_graph = SearchGraph(
        prompt=prompt,
        schema = "default",
        config=graph_config,
    )

    max_retries = 3  # Number of retry attempts
    retry_delay = 5  # Seconds to wait between retries

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt} of {max_retries}")
            result = search_scraper_graph.run()
            print(json.dumps(result))
            break  # Exit the loop if successful
        except Exception as e:
            print(f"Attempt {attempt} failed: {str(e)}", file=sys.stderr)
            if attempt < max_retries:
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print("All attempts failed.", file=sys.stderr)
                sys.exit(1)

if __name__ == "__main__":
    main()