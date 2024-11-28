from ..helpers.tool import Tool, Response
from ..helpers.searxng_search import search

class SearxngSearch(Tool):
    """Tool for performing web searches using SearXNG"""

    async def execute(self, query: str = "", results: int = 5, **kwargs):
        """
        Execute a web search using SearXNG
        
        Args:
            query: Search query string
            results: Number of results to return (default 5)
        """
        if not query:
            return Response(
                message="Please provide a search query",
                break_loop=False
            )

        try:
            search_results = await search(query, results)
            
            if not search_results:
                return Response(
                    message="No results found",
                    break_loop=False
                )

            # Format results into a readable message
            message = f"Here are the top {len(search_results)} results for '{query}':\n\n"
            
            for i, result in enumerate(search_results, 1):
                message += f"{i}. {result['title']}\n"
                message += f"   URL: {result['url']}\n"
                message += f"   {result['snippet']}\n\n"

            return Response(
                message=message,
                break_loop=False
            )

        except Exception as e:
            return Response(
                message=f"Error performing search: {str(e)}",
                break_loop=False
            )
