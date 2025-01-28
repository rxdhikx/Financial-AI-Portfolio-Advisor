## Project Name: AI Financial Portfolio Advisor 

# Portfolio Rebalancing System with AWS and Machine Learning

This project is a portfolio rebalancing system that fetches real-time market data, analyzes client portfolios using machine learning, and provides rebalancing recommendations. The system is built using AWS services (Lambda, S3, EventBridge, SageMaker, API Gateway, IAM) and Streamlit for the user interface.

---

## **Project Overview**

The system performs the following tasks:
1. **Fetches Real-Time Market Data**: Using a Lambda function (`fetch-market-data`), it retrieves stock market data every 5 minutes and stores it in an S3 bucket.
2. **Generates Synthetic Client Portfolios**: A synthetic dataset of client portfolios is created using SageMaker and stored in S3.
3. **Trains an XGBoost Model**: The XGBoost model is trained on the client portfolio data to predict rebalancing decisions (e.g., buy/sell amounts).
4. **Rebalances Portfolios**: A second Lambda function (`rebalance_portfolio`) uses the trained model to recommend portfolio adjustments.
5. **Displays Results in a Dashboard**: A Streamlit app connects to the system via an API Gateway to display recommendations and market data.

---

## **Files in the Repository**

1. **Lambda Functions**:
   - `lambda-function-fetch-market-data.py`: Fetches real-time market data and saves it to S3.
   - `lambda-function-rebalancing-portfolio.py`: Analyzes client portfolios and recommends rebalancing actions.

2. **Streamlit Dashboard**:
   - `streamlit_dashboard_code.py`: Code for the Streamlit app that displays portfolio recommendations and market data.

3. **Synthetic Data Generation**:
   - `synthetic_data.ipynb`: Jupyter notebook to generate synthetic client portfolio data.
   - `synthetic_portfolios.csv`: Sample synthetic client portfolio data.

4. **Machine Learning Model**:
   - `xgboost_model.ipynb`: Jupyter notebook to train the XGBoost model for portfolio rebalancing.

---

## **How to Use**

### **Prerequisites**
- AWS account with access to Lambda, S3, EventBridge, SageMaker, API Gateway, and IAM.
- Python 3.x with libraries: `boto3`, `pandas`, `yfinance`, `streamlit`, `xgboost`.
- Streamlit installed (`pip install streamlit`).

### **Steps to Run the Project**

1. **Set Up AWS Services**:
   - Create an S3 bucket to store market data and client portfolios.
   - Create two Lambda functions (`fetch-market-data` and `rebalance_portfolio`) and configure their IAM roles.
   - Set up EventBridge to trigger the `fetch-market-data` Lambda every 5 minutes.
   - Deploy the XGBoost model using SageMaker and note the endpoint ARN.
   - Create an API Gateway to trigger the `rebalance_portfolio` Lambda.


2. **Upload Synthetic Data**:
   - Upload `synthetic_portfolios.csv` to your S3 bucket.

3. **Run the Streamlit App**:
   - Update the API Gateway Invoke URL in `streamlit_dashboard_code.py`.
   - Run the Streamlit app using the command:
     ```bash
     streamlit run streamlit_dashboard_code.py
     ```

4. **Test the System**:
   - Check the S3 bucket for updated market data.
   - Use the Streamlit app to view portfolio recommendations.

---

## **AWS Architecture Diagram**

![AWS Architecture Diagram](https://via.placeholder.com/800x400.png)  
*(Replace with your actual diagram)*

---

## **Contributing**

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
