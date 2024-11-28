### searxng_search

Use this tool to perform web searches with semantic ranking of results. The tool uses SearxNG to aggregate search results and enhances them with embeddings for better relevance.

**Parameters:**
- query (string): The search query to execute
- results (optional number): Number of results to return (default: 5)
- engines (optional string): Comma-separated list of search engines to use (default: "duckduckgo,google")

**Returns:**
A list of search results, each containing:
- title: The page title
- url: The page URL
- snippet: A brief excerpt from the page
- content: The full page content
- summary: An AI-generated summary of the content
- embedding: Vector embedding for semantic similarity ranking

**Example:**
```json
{
    "query": "quantum computing basics",
    "results": 3,
    "engines": "duckduckgo,google"
}
```

Note: For semantic search functionality to work, ensure you have set your OpenAI API key in the .env file (API_KEY_OPENAI).
