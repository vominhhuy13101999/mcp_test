
def main():
    from fastmcp import FastMCP
    from core.config import config
    from news import register_news_tools
    from tools.rag import register_rag_tools
    
    mcp = FastMCP("Demo Model Context Protocol")

    register_news_tools(mcp)
    register_rag_tools(mcp)
    
    mcp.run(
        transport="sse",
        host=config.HOST,
        port=config.PORT,
        log_level=config.LOG_LEVEL
    )

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv("../scripts/environments/.env")

    main()
    
    
    