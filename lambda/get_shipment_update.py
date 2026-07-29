import json
import boto3
import time

BUCKET = "company-agent"
DATABASE = "company_cs"
RESULTS_LOCATION = f"s3://{BUCKET}/athena-results/"

athena = boto3.client("athena", region_name="us-east-1")

def run_query(sql):
    response = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={"Database": DATABASE},
        ResultConfiguration={"OutputLocation": RESULTS_LOCATION}
    )
    execution_id = response["QueryExecutionId"]

    while True:
        result = athena.get_query_execution(QueryExecutionId=execution_id)
        state = result["QueryExecution"]["Status"]["State"]
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(1)

    if state != "SUCCEEDED":
        raise Exception(f"Query failed with state: {state}")

    results = athena.get_query_results(QueryExecutionId=execution_id)
    rows = results["ResultSet"]["Rows"]

    headers = [col["VarCharValue"] for col in rows[0]["Data"]]
    data = []
    for row in rows[1:]:
        values = [col.get("VarCharValue", "") for col in row["Data"]]
        data.append(dict(zip(headers, values)))

    return data

def lambda_handler(event, context):
    # Extract order_id from Bedrock Agent event format
    order_id = ""

    parameters = event.get("parameters", [])
    for param in parameters:
        if param.get("name") == "order_id":
            order_id = param.get("value", "").upper()

    action_group = event.get("actionGroup", "")
    function = event.get("function", "")
    message_version = event.get("messageVersion", "1.0")

    if not order_id:
        response_body = {"TEXT": {"body": "order_id parameter is required"}}
    else:
        sql = f"SELECT * FROM shipments WHERE order_id = '{order_id}'"
        try:
            results = run_query(sql)
            if not results:
                response_body = {"TEXT": {"body": f"No shipment found for order_id: {order_id}. Order may still be processing."}}
            else:
                shipment = results[0]
                response_body = {
                    "TEXT": {
                        "body": json.dumps(shipment)
                    }
                }
        except Exception as e:
            response_body = {"TEXT": {"body": f"Error: {str(e)}"}}

    # Bedrock Agent required response format
    return {
        "messageVersion": message_version,
        "response": {
            "actionGroup": action_group,
            "function": function,
            "functionResponse": {
                "responseBody": response_body
            }
        }
    }