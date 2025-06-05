from fastmcp import FastMCP

mcp = FastMCP("Demo Model Context Protocol")

@mcp.resource("data://{name}")
def get_greeting(name: str) -> str:
    """
        Get a greeting message for the given name.
    """
    return f"Hello, {name}!"

@mcp.resource("data://product-categories")
def get_categories() -> list[str]:
    """Returns a list of available product categories."""
    return ["Electronics", "Books", "Home Goods"]

@mcp.tool()
def add(x: int, y: int) -> int:
    """
        Add two integer numbers
    """    
    return sum([x, y])

@mcp.tool()
def divide(x: int, y: int) -> float:
    """
        Divide two integer numbers
    """
    if y == 0:
        raise ValueError("Division by zero is not allowed.")
    return x / y

@mcp.tool()
def multiply(x: int, y: int) -> int:
    """
        Multiply two integer numbers
    """
    return x * y

@mcp.tool()
def subtract(x: int, y: int) -> int:
    """
        Subtract two integer numbers
    """
    return x - y

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="127.0.0.1",
        port=17324,
        log_level="debug"
    )
    
    