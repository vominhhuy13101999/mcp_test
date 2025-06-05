# filepath: c:\Users\anhld\Work\Learn\mcp_test\src\tools\rag.py
from typing import List, Dict, Any, Optional

import httpx
import json
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastmcp import FastMCP, Context

from core.config import config

class RAGTool:
    def __init__(self, qdrant_url: Optional[str] = None, collection_name: Optional[str] = None, 
                 jina_api_url: Optional[str] = None):
        """
        Initialize the RAG tool with Qdrant client and Jina Embedding service.
        
        Args:
            qdrant_url (str, optional): URL of the Qdrant server. Defaults to value from config.
            collection_name (str, optional): Name of the collection to search in. Defaults to value from config.
            jina_api_url (str, optional): URL for the Jina Embedding API. Defaults to value from config.
        """
        # Initialize Qdrant client with API key if available (for cloud-hosted Qdrant)
        if config.QDRANT_API_KEY:
            self.client = QdrantClient(url=qdrant_url or config.QDRANT_URL, api_key=config.QDRANT_API_KEY)
        else:
            self.client = QdrantClient(url=qdrant_url or config.QDRANT_URL)
            
        self.collection_name = collection_name or config.QDRANT_COLLECTION
        self.jina_api_url = jina_api_url or config.JINA_API_URL
        
        # Get Jina API key from config
        self.jina_api_key = config.JINA_API_KEY
        
        if not self.jina_api_key:
            print("Warning: JINA_API_KEY not set in environment variables or .env file")
        
    async def get_embedding(self, text: str) -> List[float]:
        """
        Get vector embedding for text using Jina Embedding service.
        
        Args:
            text (str): The text to convert to embedding vector.
            
        Returns:
            List[float]: The embedding vector representation of the text.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.jina_api_key}"
        }
        
        payload = {
            "input": text,
            "model": config.JINA_EMBEDDING_MODEL
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.jina_api_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()  # Raise an exception for bad responses
            result = response.json()
            
            # Extract the embedding from response
            embedding = result.get("data", [])[0].get("embedding", [])
            if not embedding:
                raise ValueError("Failed to get embedding from Jina API")
                
            return embedding
        
    async def vector_search(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector embeddings.
        
        Args:
            query_vector (List[float]): The vector representation of the query.
            limit (int, optional): Maximum number of results to return. Defaults to 5.
            
        Returns:
            List[Dict[str, Any]]: List of search results with their payload and scores.
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        
        results = []
        for scored_point in search_result:
            results.append({
                "id": scored_point.id,
                "score": scored_point.score,
                "payload": scored_point.payload
            })
            
        return results
    
    async def text_search(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for documents matching the given text query.
        
        Args:
            query_text (str): The text query to search for.
            limit (int, optional): Maximum number of results to return. Defaults to 5.
            
        Returns:
            List[Dict[str, Any]]: List of search results with their payload and scores.
        """
        search_result = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="text",
                        match=models.MatchText(text=query_text)
                    )
                ]
            ),
            limit=limit
        )
        
        results = []
        for point in search_result[0]:
            results.append({
                "id": point.id,
                "payload": point.payload
            })
            
        return results

def register_rag_tools(mcp: FastMCP):
    """
    Register RAG tools with the MCP server.
    
    Args:
        mcp (FastMCP): The MCP server instance.
    """
    rag_tool = RAGTool()
    
    @mcp.tool()
    async def semantic_search(query: str, ctx: Context, limit: int = 5) -> str:
        """
        Search for documents semantically related to the query using embeddings.
        
        Arguments:
            query (str): The search query.
            limit (int, optional): Maximum number of results to return (default: 5).
            
        Returns:
            str: A formatted string containing search results with their content and relevance scores.
        """
        await ctx.info(f"Performing semantic search for: {query}")
        
        try:
            # Get the embedding for the query
            query_vector = await rag_tool.get_embedding(query)
            
            # Search for similar documents using the embedding
            results = await rag_tool.vector_search(query_vector, limit=limit)
            
            if not results:
                return f"No semantically similar documents found for query '{query}'."
            
            formatted_results = "\n\n".join([
                f"Document ID: {result['id']}\n"
                f"Similarity Score: {result['score']:.4f}\n"
                f"Content: {result['payload'].get('text', 'No content available')}\n"
                f"Metadata: {', '.join([f'{k}: {v}' for k, v in result['payload'].items() if k != 'text'])}"
                for result in results
            ])
            
            return f"Found {len(results)} semantically similar documents:\n\n{formatted_results}"
            
        except Exception as e:
            return f"Error during semantic search: {str(e)}"
    
    @mcp.tool()
    async def keyword_search(query: str, ctx: Context, limit: int = 5) -> str:
        """
        Search for documents containing specific keywords or text.
        
        Arguments:
            query (str): The search query keywords.
            limit (int, optional): Maximum number of results to return (default: 5).
            
        Returns:
            str: A formatted string containing search results with their content.
        """
        await ctx.info(f"Searching for documents with keywords: {query}")
        
        # Use text-based search
        results = await rag_tool.text_search(query, limit=limit)
        
        if not results:
            return f"No documents found containing '{query}'."
        
        formatted_results = "\n\n".join([
            f"Document ID: {result['id']}\n"
            f"Content: {result['payload'].get('text', 'No content available')}\n"
            f"Metadata: {', '.join([f'{k}: {v}' for k, v in result['payload'].items() if k != 'text'])}"
            for result in results
        ])
        
        return f"Found {len(results)} documents containing '{query}':\n\n{formatted_results}"