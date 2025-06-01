from typing import Any, List, Dict

import httpx

from fastmcp import FastMCP, Context

# Get API key from environment variable
API_KEY = "pub_8778629f5d920f128b0179428747dda95fab9"
if not API_KEY:
    raise ValueError("NEWS_API_KEY not found in .env file")

BASE_URL = "https://newsdata.io/api/1"

# Helper function to fetch news from the API with nextPage pagination
async def fetch_crypto_news(path: str, query: str = None, max_pages: int = 1) -> List[Dict[str, Any]]:
    all_articles = []
    next_page = None  # Start with no page token for the first request
    
    async with httpx.AsyncClient() as client:
        params = {
            "apikey": "pub_8778629f5d920f128b0179428747dda95fab9",
        }
        if query:
            params["q"] = query
        
        # Fetch up to max_pages
        for _ in range(max_pages):
            if next_page:
                params["page"] = next_page  # Use nextPage token from previous response
            
            response = await client.get(path)
            response.raise_for_status()  # Raise an exception for bad responses
            
            data = response.json()
            
            print(data)
            
            articles = data.get("results", [])
            all_articles.extend(articles)
            
            # Get the nextPage token from the response
            next_page = data.get("nextPage")
            
            # Stop if there’s no nextPage or no more articles
            if not next_page or not articles:
                break
        
        return all_articles

def register_news_tools(mcp: FastMCP):
    # Tool: Fetch the latest cryptocurrency news headlines
    @mcp.tool()
    async def get_latest_news(ctx: Context) -> str:
        """
        Fetch the latest cryptocurrency news headlines.
        
        Returns:
            str: A formatted string of the latest news headlines with publication dates.
        """
        ctx.info("Fetching latest cryptocurrency news headlines")
        articles = await fetch_crypto_news("https://newsdata.io/api/1/latest?apikey=pub_8778629f5d920f128b0179428747dda95fab9")
        headlines = "\n".join(
            f"{article['title']} (Published: {article['pubDate']})"
            for article in articles
        )
        return headlines if headlines else "No recent news available."

    # Tool: Fetch news for a specific cryptocurrency with pagination
    @mcp.tool()
    async def get_crypto_news(query: str, max_pages: int = 1, ctx: Context = None) -> str:
        """
        Fetch news articles for a specific cryptocurrency or topic with pagination support.
        
        Arguments:
            query (str): The cryptocurrency or keyword to search for (e.g., 'bitcoin', 'ethereum').
            max_pages (int, optional): Maximum number of pages to fetch (default: 1). Each page typically contains up to 10 articles.
        
        Returns:
            str: A formatted string containing news article titles, dates, and descriptions.
        """
        ctx.info(f"Fetching news for query: {query} with max_pages: {max_pages}")
        
        print(query, max_pages)
        
        articles = await fetch_crypto_news(f"https://newsdata.io/api/1/latest?apikey=pub_8778629f5d920f128b0179428747dda95fab9&q={query}", max_pages=max_pages)
        
        if not articles:
            return f"No news found for query '{query}'."
        
        result = "\n\n".join(
            f"Title: {article['title']}\n"
            f"Date: {article['pubDate']}\n"
            f"Description: {article['description'] or 'No description available'}"
            for article in articles
        )
        return result