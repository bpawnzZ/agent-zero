import aiohttp
import json
from typing import List, Dict, Any
from urllib.parse import quote

async def search(query: str, results: int = 5, engines: str = "duckduckgo,google") -> List[Dict[str, Any]]:
    """
    Search using SearXNG instance
    
    Args:
        query: Search query string
        results: Number of results to return (default 5)
        engines: Comma-separated list of search engines to use
        
    Returns:
        List of search results with title, url, and snippet
    """
    encoded_query = quote(query)
    url = f"https://searxng.2damoon.xyz/search?q={encoded_query}&engines={engines}&format=json"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return []
                
            data = await response.json()
            
            if not data or 'results' not in data:
                return []
                
            results_list = []
            for result in data['results'][:results]:
                results_list.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'snippet': result.get('content', '')
                })
                
            return results_list
