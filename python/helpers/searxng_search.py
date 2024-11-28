import aiohttp
import json
import trafilatura
import litellm
import logging
import os
from typing import List, Dict, Any
from urllib.parse import quote
from bs4 import BeautifulSoup
import models

logger = logging.getLogger(__name__)

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
    """Get embedding vector for text using project's configured embedding model"""
    try:
        # Use OpenAI embeddings directly from models
        embeddings = models.get_openai_embedding(model_name="openai/text-embedding")
        if not embeddings:
            logger.warning("Failed to initialize embedding model")
            return []
            
        result = embeddings.embed_query(text)
        logger.debug(f"Generated embedding of length {len(result)}")
        return result
    except Exception as e:
        logger.warning(f"Failed to generate embedding: {str(e)}")
        return []

async def summarize_content(content: str) -> str:
    """Summarize webpage content using OpenAI"""
    if not content:
        return ""
    try:
        # Use OpenAI chat model directly from models
        chat_model = models.get_openai_chat(model_name="openai/gpt-4o-mini", temperature=0.8)
        if not chat_model:
            logger.warning("Failed to initialize chat model")
            return ""

        response = await chat_model.apredict(
            f"Summarize the following text in a concise way:\n\n{content[:4000]}"  # Limit content length
        )
        return response
    except Exception as e:
        logger.warning(f"Failed to summarize content: {str(e)}")
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
