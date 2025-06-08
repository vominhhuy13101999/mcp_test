def create_app():
    from fastapi import FastAPI
    
    from mcp_server import create_server
    
    mcp = create_server()
    
    # Note: Create the ASGI app
    mcp_app = mcp.http_app(transport="sse", path="/sse")
    
    # Note: Create a FastAPI app and mount the MCP server
    fastapi_app = FastAPI(lifespan=mcp_app.lifespan)
    fastapi_app.mount("/mcp-server", mcp_app)

    return fastapi_app

app = create_app()
    
if __name__ == "__main__":
    import uvicorn
    
    from dotenv import load_dotenv
    
    from core.config import config
    
    load_dotenv("../scripts/environments/.env")

    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT
    )
    
    
    