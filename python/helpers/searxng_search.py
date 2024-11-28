import aiohttp
import json
import trafilatura
import litellm
from typing import List, Dict, Any
from urllib.parse import quote
from bs4 import BeautifulSoup

async def get_webpage_content(url: str) -> str:
    """Extract main content from webpage"""
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded) or ""
    except:
        return ""
    return ""

async def get_embedding(text: str) -> List[float]:
    """Get embedding vector for text using OpenAI"""
    try:
        response = await litellm.aembedding(
            model="openai/text-embedding",
            input=text,
            api_base="https://litellm.2damoon.xyz",
            api_key="sk-FiIu6b1Hyq7TDX-C9phogQ"
        )
        return response.data[0].embedding
    except:
        return []

async def summarize_content(content: str) -> str:
    """Summarize webpage content using OpenAI"""
    if not content:
        return ""
    try:
        response = await litellm.acompletion(
            model="openai/gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "Summarize the following text in a concise way:"
            }, {
                "role": "user", 
                "content": content[:4000]  # Limit content length
            }],
            api_base="https://litellm.2damoon.xyz",
            api_key="sk-FiIu6b1Hyq7TDX-C9phogQ"
        )
        return response.choices[0].message.content
    except:
        return ""

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
            query_embedding = await get_embedding(query)
            
            for result in data['results'][:results]:
                url = result.get('url', '')
                content = await get_webpage_content(url)
                summary = await summarize_content(content)
                
                # Get embedding for the full content to enable semantic search
                content_embedding = await get_embedding(content) if content else []
                
                results_list.append({
                    'title': result.get('title', ''),
                    'url': url,
                    'snippet': result.get('content', ''),
                    'content': content,
                    'summary': summary,
                    'embedding': content_embedding
                })
            
            # Sort results by semantic similarity if we have embeddings
            if query_embedding and any(r['embedding'] for r in results_list):
                results_list.sort(
                    key=lambda x: sum(a*b for a,b in zip(query_embedding, x['embedding'])) if x['embedding'] else -1,
                    reverse=True
                )
                
            return results_list
