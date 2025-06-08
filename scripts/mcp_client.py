from fastmcp import Client

async def main():
    # Connect via SSE
    async with Client("http://127.0.0.1:17324/sse") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        result = await client.call_tool("semantic_search", {"query": "Can we have a Pet ?", "limit": 10})
        print(f"Result: {result[0].text}")

if __name__ == "__main__":
    import asyncio
    
    asyncio.run(main())