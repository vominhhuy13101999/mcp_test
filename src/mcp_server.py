from fastmcp import FastMCP


def create_server():
    from tools.news import register_news_tools
    from tools.rag import register_rag_tools

    server = FastMCP("MCP Server for Agents")

    register_news_tools(server)
    register_rag_tools(server)
    
    return server
