import pytest
import asyncio
from python.helpers.searxng_search import search
from python.tools.searxng_search import SearxngSearch

@pytest.mark.asyncio
async def test_searxng_search_helper():
    # Test the search helper function
    results = await search("python programming", results=2)
    
    assert isinstance(results, list)
    assert len(results) <= 2
    
    if results:  # If we got results
        assert 'title' in results[0]
        assert 'url' in results[0]
        assert 'snippet' in results[0]
        assert 'content' in results[0]
        assert 'summary' in results[0]
        assert 'embedding' in results[0]
        
        # Verify embedding field exists and is a list
        assert isinstance(results[0]['embedding'], list)
            
        # Only verify embedding contents if we got embeddings
        if results[0]['embedding']:
            assert all(isinstance(x, float) for x in results[0]['embedding'])
                
            # Verify semantic sorting only if we have multiple results with embeddings
            if len(results) > 1 and results[1]['embedding']:
                first_similarity = sum(a*b for a,b in zip(results[0]['embedding'], results[0]['embedding']))
                second_similarity = sum(a*b for a,b in zip(results[1]['embedding'], results[1]['embedding']))
                assert first_similarity >= second_similarity

@pytest.mark.asyncio
async def test_searxng_search_tool():
    # Test the search tool
    tool = SearxngSearch(
        agent=None,
        name="searxng_search",
        args={"query": {"type": "string", "description": "Search query"}},
        message="Search the web using SearXNG"
    )
    response = await tool.execute(query="python programming", results=2)
    
    assert response is not None
    assert response.message is not None
    assert not response.break_loop
    assert "results for 'python programming'" in response.message

@pytest.mark.asyncio
async def test_empty_query():
    tool = SearxngSearch(
        agent=None,
        name="searxng_search",
        args={"query": {"type": "string", "description": "Search query"}},
        message="Search the web using SearXNG"
    )
    response = await tool.execute(query="")
    
    assert response is not None
    assert "Please provide a search query" in response.message
