# Portfolio Rebalancing System - Project Report

---

## **Introduction**

This project aims to automate portfolio rebalancing using real-time market data and machine learning. The system fetches market data, analyzes client portfolios, and provides rebalancing recommendations through a user-friendly dashboard.

---

## **Objectives**

1. Fetch and store real-time market data.
2. Generate synthetic client portfolio data for testing.
3. Train a machine learning model (XGBoost) to predict rebalancing decisions.
4. Provide rebalancing recommendations via a Streamlit dashboard.

---

## **System Architecture**

The system is built using the following AWS services and components:

1. **Lambda Functions**:
   - `fetch-market-data`: Fetches market data every 5 minutes using `yfinance` and stores it in S3.
   - `rebalance_portfolio`: Uses the trained XGBoost model to recommend portfolio adjustments.

2. **S3 Buckets**:
   - Stores real-time market data and client portfolio data.

3. **EventBridge**:
   - Triggers the `fetch-market-data` Lambda every 5 minutes.

4. **SageMaker**:
   - Generates synthetic client portfolio data.
   - Trains and deploys the XGBoost model.

5. **API Gateway**:
   - Connects the `rebalance_portfolio` Lambda to the Streamlit app.

6. **Streamlit**:
   - Displays portfolio recommendations and market data in a dashboard.

---

## **Implementation Details**

### **1. Fetching Market Data**
- The `fetch-market-data` Lambda function uses the `yfinance` library to fetch stock market data.
- The data is saved as a CSV file in an S3 bucket (`lpl-realtime-market-data`).
- EventBridge triggers this Lambda every 5 minutes to ensure the data is up-to-date.

### **2. Generating Synthetic Data**
- Using SageMaker, a Jupyter notebook (`synthetic_data.ipynb`) generates synthetic client portfolio data.
- The data is saved as `synthetic_portfolios.csv` and uploaded to S3.

### **3. Training the XGBoost Model**
- The `xgboost_model.ipynb` notebook trains an XGBoost model on the synthetic client portfolio data.
- The trained model is deployed as an endpoint using SageMaker.

### **4. Rebalancing Portfolios**
- The `rebalance_portfolio` Lambda function uses the trained XGBoost model to analyze client portfolios and recommend rebalancing actions.

### **5. Streamlit Dashboard**
- The Streamlit app (`streamlit_dashboard_code.py`) connects to the system via API Gateway.
- It displays portfolio recommendations and market data in a user-friendly interface.

---

## **Results**

- Real-time market data is successfully fetched and stored in S3 every 5 minutes.
- Synthetic client portfolio data is generated and used to train the XGBoost model.
- The model provides accurate rebalancing recommendations.
- The Streamlit dashboard effectively displays the results.

---

## **Challenges and Solutions**

1. **Challenge**: Lambda function dependencies (e.g., `yfinance`, `pandas`).  
   **Solution**: Created a custom Lambda layer with the required libraries.

2. **Challenge**: Ensuring real-time data updates.  
   **Solution**: Used EventBridge to trigger the Lambda function every 5 minutes.

3. **Challenge**: Connecting the Streamlit app to AWS.  
   **Solution**: Used API Gateway to create a REST API for the `rebalance_portfolio` Lambda.

---

## **Future Enhancements**

1. Add support for more asset types (e.g., bonds, cryptocurrencies).
2. Implement user authentication for the Streamlit app.
3. Optimize the XGBoost model for better performance.

---

## **Conclusion**

This project demonstrates how AWS services and machine learning can be used to automate portfolio rebalancing. The system is scalable, efficient, and provides actionable insights for investors.

---

## **References**

- AWS Documentation: https://docs.aws.amazon.com/
- Streamlit Documentation: https://docs.streamlit.io/
- XGBoost Documentation: https://xgboost.readthedocs.io/

---
