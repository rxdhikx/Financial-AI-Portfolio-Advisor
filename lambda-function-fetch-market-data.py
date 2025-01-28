#LAMBDA FUNCTION CODE FOR FETCH MARKET DATA


import yfinance as yf
import boto3
from datetime import datetime


def lambda_handler(event, context):
   try:
       # Fetch S&P 500 ETF data (VOO)
       data = yf.download(tickers="VOO", period="1d", interval="5m")
      
       # Save to S3
       s3 = boto3.client("s3")
       bucket_name = "lpl-realtime-market-data"  # CHANGE THIS
       filename = f"market-data-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.csv"
      
       # Save to /tmp (Lambda's writable directory)
       tmp_path = f"/tmp/{filename}"
       data.to_csv(tmp_path)
      
       # Upload to S3
       s3.upload_file(tmp_path, bucket_name, filename)
       return {"status": "success", "message": f"File {filename} uploaded to {bucket_name}"}
  
   except Exception as e:
       return {"status": "error", "message": str(e)}

