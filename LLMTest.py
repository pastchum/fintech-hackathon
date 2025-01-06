from scrapegraphai.graphs import SearchGraph
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_APIKEY")
# Configuration for LLM and embeddings
graph_config = {
   "llm": {
        "api_key": API_KEY,
        "model": "openai/gpt-4o-mini",
   },
   "embeddings": {
        "api_key": API_KEY,
        "model": "text-embedding-ada-002",
   }
}

# Define the schema for extracted data
schema = {
    "fields": [
        {"name": "recipe_name", "type": "string"},
        {"name": "ingredients", "type": "list"},
        {"name": "steps", "type": "list"}
    ]
}

# Create the SearchGraph instance
search_graph = SearchGraph(
   prompt="List me all the articles mentioning money laundering with regards to 1MDB",
   config=graph_config,
   schema=schema
)

# Run the graph and print the results
result = search_graph.run()
print(result)
