from fastmcp import Client

async def main():
    # Connect via SSE
    async with Client("http://127.0.0.1:17324/sse") as client:
        print(f"Client connected: {client.is_connected()}")
        
        while True:
            tools = await client.list_tools()
            print(f"Available tools".center(50, "="))
            for tool in tools:
                print(tool)
                
            resources = await client.list_resources()
            print(f"Available resources: {resources}")
            
            result = await client.call_tool("semantic_search", {"query": "Can we have a Pet ?", "limit": 10})
            print(f"Result: {result[0].text}")
                
            text = input("Press Enter to call the add tool again or type 'exit' to quit: ")
            if text.strip().lower() == "exit":
                print("Exiting...")
                break

if __name__ == "__main__":
    import asyncio
    
    asyncio.run(main())