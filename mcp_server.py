from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import boto3
import asyncio

app = Server("company-cs-agent")
bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-1")


@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="query_customer_service",
            description="Look up order status or shipment updates for a customer by order ID or customer name",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language question e.g. 'What is the status of order ORD-0001?'",
                    }
                },
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name, arguments):
    response = bedrock_agent.invoke_agent(
        agentId="MLBTT9M2CA",
        agentAliasId="TSTALIASID",
        sessionId="session-001",
        inputText=arguments.get("query"),
    )
    completion = ""
    for event in response.get("completion"):
        # collect agent output
        if "chunk" in event:
            chunk = event["chunk"]
            completion += chunk["bytes"].decode()

    print(f"Agent response: {completion}")
    
    return [TextContent(type="text", text=completion)]


if __name__ == "__main__":
    async def main():
        async with stdio_server() as (read, write):
            await app.run(read, write, app.create_initialization_options())
    
    asyncio.run(main())
