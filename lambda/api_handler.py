import json
import boto3

bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

AGENT_ID = "MLBTT9M2CA"
AGENT_ALIAS_ID = "TSTALIASID"

def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": ""
        }

    try:
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body)
        query = body.get("query", "")
        session_id = body.get("session_id", "default-session")

        if not query:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "query is required"})
            }

        response = bedrock_agent.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=query
        )

        completion = ""
        for event in response.get("completion"):
            if "chunk" in event:
                chunk = event["chunk"]
                completion += chunk["bytes"].decode()

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"response": completion})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }