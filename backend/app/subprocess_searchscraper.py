import sys
import os
import json
from scrapegraphai.graphs import SearchGraph

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OPENAI_APIKEY

def main():
    # Parse arguments passed to the subprocess
    try:
        input_data = json.loads(sys.argv[1])
    except Exception as e:
        print(f"Error parsing input data: {str(e)}", file=sys.stderr)
        sys.exit(1)
    prompt = input_data["prompt"]

    if not prompt:
        print("Error: Missing required arguments 'prompt'", file=sys.stderr)
        sys.exit(1)

    graph_config = {
        "llm": {
            "api_key": OPENAI_APIKEY,
            "model": "openai/gpt-4o-mini",
        },
        "settings": {
            "headless": False
        }
    }

    # Run the scraper
    smart_scraper_graph = SearchGraph(
        prompt=prompt,
        config=graph_config,
    )

    try:
        print(prompt)
        result = smart_scraper_graph.run()  # Run synchronously in the subprocess
        return result
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()