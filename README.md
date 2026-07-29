# Customer Service Agent

AI-powered customer service agent for order and shipment lookups, built with AWS Bedrock (Claude Haiku 4.5), Lambda, S3, and Athena. Uses Amazon Bedrock Agents to enable natural language querying of order data - modeled after real retail operations at one of the companies I worked for.

---

## Overview

Customer service reps at retail companies spend a significant portion of their day navigating multiple systems to answer basic questions: *Where is this order? What's the tracking status? When will it arrive?* At this specific company, this meant manually querying Dynamics 365 F&O across order and shipment modules for every customer inquiry.

This project replaces that workflow with a natural language agent. A CS rep types a question in plain English, and the agent retrieves the answer directly from the data; no SQL, no system navigation required.

---

## Architecture

```
CS Rep (natural language question)
            │
            ▼
Amazon Bedrock Agent (Claude Haiku 4.5)
            │
     ┌──────┴──────┐
     ▼             ▼
Lambda            Lambda
get_order_status  get_shipment_update
     │             │
     └──────┬──────┘
            ▼
       Amazon Athena
            │
            ▼
        Amazon S3
     (orders.csv / shipments.csv)
```

**Services used:**
- **Amazon S3** - stores synthetic order and shipment datasets
- **Amazon Athena** - serverless SQL queries directly on S3 data
- **AWS Lambda** - serverless functions that handle tool execution
- **Amazon Bedrock Agents** - orchestration layer that routes natural language to the right Lambda tool
- **Claude Haiku 4.5** - the underlying LLM that interprets questions and formulates responses
- **AWS IAM** - role-based access control across all services
- **Amazon CloudWatch** - Lambda execution logging and monitoring

---

## What It Does

Ask the agent questions like:

- *"What is the status of order ORD-0042?"*
- *"Has ORD-0015 shipped yet?"*
- *"What carrier is handling order ORD-0023 and when will it arrive?"*

The agent decides which tools to call, retrieves the data, and returns a clear, professional response; without the rep ever touching a database.

---

## Data

Synthetic dataset of 100 orders and 37 shipments generated to mirror D365 F&O data structure.

**Orders table:** order_id, customer_id, customer_name, product, quantity, price, order_date, status

**Shipments table:** shipment_id, order_id, carrier, tracking_number, ship_date, estimated_delivery, status

Data is stored as CSV in S3 and queried via Athena; no database server required.

---

## Project Structure

```
Customer-Service-Agent/
├── README.md
├── data/
│   └── generate_data.py        # Synthetic data generator
│   └── shipments.csv           # Shipments sample data
│   └── orders.csv              # Orders sample data
├── lambda/
│   ├── get_order_status.py     # Lambda: order lookup tool
│   └── get_shipment_update.py  # Lambda: shipment tracking tool
└── athena/
    └── setup.sql               # Athena database and table setup
```

---

## Setup

### Prerequisites
- AWS account with Bedrock access (Claude Haiku 4.5 via AWS Marketplace)
- Python 3.12+
- AWS CLI configured

### 1. Generate synthetic data
```bash
cd data
python generate_data.py
```
Upload `orders.csv` and `shipments.csv` to an S3 bucket.

### 2. Set up Athena
Run the SQL in `athena/setup.sql` in the Athena query editor, pointing to your S3 bucket.

### 3. Deploy Lambda functions
- Create two Lambda functions in us-east-1 (Python 3.12)
- Attach an IAM role with S3, Athena, Bedrock, and CloudWatch permissions
- Deploy `lambda/get_order_status.py` and `lambda/get_shipment_update.py`

### 4. Create Bedrock Agent
- Region: us-east-1
- Model: Claude Haiku 4.5 (Global inference profile)
- Add two action groups pointing to the Lambda functions
- Grant the Bedrock execution role `bedrock:InvokeModel` and inference profile permissions

---

## Challenges & Lessons Learned

This project involved more AWS configuration than code, which turned out to be the real learning.

**Region availability**
Bedrock Agents with newer Anthropic models only works reliably in us-east-1. Always check regional service availability before starting infrastructure work.

**IAM permissions across services**
Bedrock Agents, Lambda, and Athena each require their own trust relationships and permission boundaries. The Bedrock execution role needs explicit `bedrock:InvokeModel` permissions and cross-region inference profile access - neither is attached by default. Debugging 403s across three services made IAM fundamentals very concrete.

**Lambda response format**
Bedrock Agents expects a specific response envelope from Lambda functions - `messageVersion`, `actionGroup`, `functionResponse` - that differs from standard Lambda invocation responses. The agent fails if this format is wrong. Reading the Bedrock documentation carefully and inspecting the agent trace resolved this.

**AWS Marketplace model subscriptions**
Newer Anthropic models on Bedrock require an AWS Marketplace subscription even for personal accounts. This wasn't obvious from the console and took time to diagnose. The error message points to IAM permissions, but the real fix is completing the Marketplace subscription flow.
