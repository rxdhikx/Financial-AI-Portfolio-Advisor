#LAMBDA FUNCTION CODE FOR REBALANCING PORTFOLIO


import json
import boto3
import pandas as pd


s3 = boto3.client("s3")
sagemaker = boto3.client("sagemaker-runtime", region_name="us-west-2")
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")


def lambda_handler(event, context):
   try:
       # Check if 'portfolio' exists in the event
       if "portfolio" not in event:
           return {
               "statusCode": 400,
               "body": json.dumps({"error": "Missing 'portfolio' in event"})
           }
      
       portfolio = event["portfolio"]
      
       # Validate portfolio structure
       if not isinstance(portfolio, dict) or not all(isinstance(key, str) and isinstance(value, (int, float)) for key, value in portfolio.items()):
           return {
               "statusCode": 400,
               "body": json.dumps({"error": "Invalid 'portfolio' structure"})
           }
      
       # Get latest market data
       market_response = s3.list_objects_v2(Bucket="lpl-realtime-market-data")
       latest_file = market_response["Contents"][-1]["Key"]
       market_data = s3.get_object(Bucket="lpl-realtime-market-data", Key=latest_file)
       df_market = pd.read_csv(market_data["Body"])
      
       # Prepare input for SageMaker
       input_data = pd.DataFrame([{
           "portfolio_value": sum(portfolio.values()),
           "aapl_alloc": portfolio["AAPL"] / sum(portfolio.values()),
           "voo_alloc": portfolio["VOO"] / sum(portfolio.values()),
           "market_volatility": df_market["Close"].std()  # Example metric
       }]).to_csv(index=False, header=False)
       print("Input data to SageMaker:", input_data)  # Log the input data
      
       # Get AI prediction from SageMaker
       response = sagemaker.invoke_endpoint(
           EndpointName="portfolio-rebalancing-endpoint",
           ContentType="text/csv",
           Body=input_data
       )
       response_body = response["Body"].read().decode()
       print("SageMaker response:", response_body)  # Log the response
      
       # Parse the SageMaker response
       try:
           optimal_alloc = json.loads(response_body)
           if isinstance(optimal_alloc, float):
               # Handle case where response is a single float
               optimal_alloc = {
                   "AAPL": optimal_alloc,
                   "VOO": (1 - optimal_alloc) / 2,
                   "Cash": (1 - optimal_alloc) / 2
               }
           elif not isinstance(optimal_alloc, dict):
               raise ValueError("SageMaker response is not a dictionary")
       except Exception as e:
           return {
               "statusCode": 500,
               "body": json.dumps({"error": f"Invalid SageMaker response: {str(e)}"})
           }
      
       # Generate rebalancing recommendations
       recommendations = []
       total_value = sum(portfolio.values())
       for asset in ["AAPL", "VOO", "Cash"]:
           current = portfolio[asset] / total_value
           target = optimal_alloc[asset]
           action = "Buy" if current < target else "Sell"
           recommendations.append(f"{action} ${abs(target - current) * total_value:.2f} of {asset}")
      
       # Use Claude 3 Sonnet for risk assessment
       prompt = f"""
       Calculate a risk score (1-10) for this portfolio:
       {json.dumps(portfolio)}
       Consider market volatility and client goals. Respond in JSON format: {{"score": X, "reason": "..."}}.
       """
      
       # Call Claude 3 Sonnet
       bedrock_response = bedrock.invoke_model(
           modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",  # Updated model ID
           contentType="application/json",
           accept="application/json",
           body=json.dumps({
               "anthropic_version": "bedrock-2023-05-31",
               "max_tokens": 200,
               "top_k": 250,
               "stop_sequences": [],
               "temperature": 1,
               "top_p": 0.999,
               "messages": [
                   {
                       "role": "user",
                       "content": [
                           {
                               "type": "text",
                               "text": prompt
                           }
                       ]
                   }
               ]
           })
       )
      
       # Parse Claude 3 response
       bedrock_body = bedrock_response["body"].read().decode()
       print("Claude 3 response:", bedrock_body)  # Log the response
       risk_assessment = json.loads(bedrock_body)["content"][0]["text"]
       risk_assessment = json.loads(risk_assessment)  # Parse the JSON string
      
       # Return combined results
       return {
           "statusCode": 200,
           "body": json.dumps({
               "rebalancing_recommendations": recommendations,
               "optimal_allocation": optimal_alloc,
               "risk_assessment": risk_assessment
           })
       }
  
   except Exception as e:
       return {
           "statusCode": 500,
           "body": json.dumps({"error": str(e)})
       }










# import json
# import boto3
# import pandas as pd


# def lambda_handler(event, context):
#     try:
#         # Example portfolio (replace with real data)
#         portfolio = {"AAPL": 100, "VOO": 50, "Cash": 5000}
      
#         # Fetch latest market data from S3
#         s3 = boto3.client("s3")
#         response = s3.get_object(
#             Bucket="lpl-realtime-market-data",
#             Key="market-data-2025-01-26-06-08.csv"  # Replace with your CSV file name
#         )
#         market_data = pd.read_csv(response["Body"])
      
#         # Simple rebalancing logic (example)
#         total_value = sum(portfolio.values())
#         target_allocation = {"AAPL": 0.4, "VOO": 0.4, "Cash": 0.2}
#         recommendations = []
      
#         for asset, qty in portfolio.items():
#             target_qty = total_value * target_allocation[asset]
#             action = "Buy" if qty < target_qty else "Sell"
#             recommendations.append(f"{action} {abs(target_qty - qty)} of {asset}")
      
#         # Use Claude 3 Sonnet for risk assessment
#         bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")
      
#         # Prepare the prompt for Claude 3 Sonnet
#         prompt = f"""
#         Calculate a risk score (1-10) for this portfolio:
#         {json.dumps(portfolio)}
#         Consider market volatility and client goals. Respond in JSON format: {{"score": X, "reason": "..."}}.
#         """
      
#         # Call Claude 3 Sonnet
#         response = bedrock.invoke_model(
#             modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",  # Your model ID
#             contentType="application/json",  # Required
#             accept="application/json",  # Required
#             body=json.dumps({
#                 "anthropic_version": "bedrock-2023-05-31",  # Required
#                 "max_tokens": 200,  # Adjust as needed
#                 "top_k": 250,  # Adjust as needed
#                 "stop_sequences": [],  # Optional
#                 "temperature": 1,  # Adjust as needed
#                 "top_p": 0.999,  # Adjust as needed
#                 "messages": [
#                     {
#                         "role": "user",
#                         "content": [
#                             {
#                                 "type": "text",
#                                 "text": prompt
#                             }
#                         ]
#                     }
#                 ]
#             })
#         )
      
#         # Parse the response
#         result = json.loads(response["body"].read())
#         risk_score = json.loads(result["content"][0]["text"])
      
#         # Combine rebalancing recommendations and risk assessment
#         return {
#             "statusCode": 200,
#             "body": json.dumps({
#                 "rebalancing_recommendations": recommendations,
#                 "risk_assessment": risk_score
#             })
#         }
  
#     except Exception as e:
#         return {
#             "statusCode": 500,
#             "body": json.dumps({"error": str(e)})
#         }

