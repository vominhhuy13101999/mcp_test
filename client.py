import asyncio

from pprint import pprint

from fastmcp import Client

# client = Client("src/server.py")
client = Client("http://127.0.0.1:17324/sse")

print(client.transport)

# Asynchronous program 

async def call_tool(first_number: int, second_number: int) -> int:
    """
        Call the add tool
    """
    
    # Above code
    async with client:
        result = await client.call_tool("add", {"x": first_number, "y": second_number}) # -> gọi API Service
    
    return result

async def main():
    async with client:
        print(f"Client connected: {client.is_connected()}")
        
        while True:
            tools = await client.list_tools()
            print(f"Available tools".center('=', 50))
            for tool in tools:
                print(tool)
            
            resources = await client.list_resources()
            pprint(f"Available resources: {resources}")
        
            if any(tool.name == "add" for tool in tools):
                result = await client.call_tool("add", {"x": 5, "y": 10})
                print(f"Result of add: {result}")

            text = input("Press Enter to call the add tool again or type 'exit' to quit: ")
            if text.strip().lower() == "exit":
                print("Exiting...")
                break
            
            
if __name__ == "__main__":
    asyncio.run(main())