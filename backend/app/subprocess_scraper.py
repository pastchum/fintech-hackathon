import sys
import os
import json
from scrapegraphai.graphs import SmartScraperGraph

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import OPENAI_API_KEY

def main():
    # Parse arguments passed to the subprocess
    try:
        input_data = json.loads(sys.argv[1])
    except Exception as e:
        print(f"Error parsing input data: {str(e)}", file=sys.stderr)
        sys.exit(1)
    prompt = input_data["prompt"]
    source_url = input_data["source_url"]

    if not prompt or not source_url:
        print("Error: Missing required arguments 'prompt' or 'source_url'.", file=sys.stderr)
        sys.exit(1)

    graph_config = {
        "llm": {
            "api_key": OPENAI_API_KEY,
            "model": "openai/gpt-4o-mini",
        },
    }

    # Run the scraper
    smart_scraper_graph = SmartScraperGraph(
        prompt=prompt,
        source=source_url,
        config=graph_config,
    )

    try:
        result = smart_scraper_graph.run()  # Run synchronously in the subprocess
        print(json.dumps(result))
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
