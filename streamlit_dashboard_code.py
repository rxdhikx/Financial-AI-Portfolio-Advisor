
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json

# API URL
API_URL = "https://veqsxy23cc.execute-api.us-west-2.amazonaws.com/prod-1" #ENTER YOUR API_URL here from API Gateway POST Method's Invoke URL

# Streamlit App Title
st.title("LPL Financial AI Portfolio Advisor")

# Input Section
st.sidebar.header("Portfolio Input")
aapl = st.sidebar.number_input("AAPL Shares", value=100)
voo = st.sidebar.number_input("VOO Shares", value=50)
cash = st.sidebar.number_input("Cash ($)", value=5000)

# Button to Generate Recommendations
if st.sidebar.button("Generate AI Recommendations"):
    portfolio = {"AAPL": aapl, "VOO": voo, "Cash": cash}
    response = requests.post(API_URL, json={"portfolio": portfolio})
    
    if response.status_code == 200:
        # Parse the outer response
        outer_response = response.json()
        
        try:
            # Parse the 'body' field as JSON
            result = json.loads(outer_response["body"])
            
            # Display Rebalancing Recommendations
            st.header("Rebalancing Recommendations")
            if "rebalancing_recommendations" in result:
                for rec in result["rebalancing_recommendations"]:
                    st.write(f"- {rec}")
            else:
                st.error("No rebalancing recommendations found in the response.")
            
            # Display Optimal Allocation
            st.header("Optimal Allocation")
            if "optimal_allocation" in result:
                optimal_alloc = result["optimal_allocation"]
                st.write("Optimal allocation percentages:")
                for asset, value in optimal_alloc.items():
                    st.write(f"- **{asset}**: {value:.2f}%")
            else:
                st.error("No optimal allocation data found in the response.")
            
            # Display Risk Assessment
            st.header("Risk Assessment")
            if "risk_assessment" in result:
                risk_assessment = result["risk_assessment"]
                st.write(f"**Risk Score**: {risk_assessment['score']}")
                st.write(f"**Reason**: {risk_assessment['reason']}")
            else:
                st.error("No risk assessment data found in the response.")
            
            # Visualize Current Allocation
            st.header("Current Allocation")
            total_value = aapl + voo + cash
            if total_value > 0:
                fig = px.pie(
                    names=["AAPL", "VOO", "Cash"],
                    values=[aapl / total_value, voo / total_value, cash / total_value],
                    title="Current Portfolio Allocation"
                )
                st.plotly_chart(fig)
            else:
                st.warning("Total portfolio value is zero. Cannot display allocation.")
        
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse API response: {str(e)}")
            st.json(outer_response)  # Display the raw response for debugging
    else:
        st.error(f"Failed to fetch recommendations. Status code: {response.status_code}")
        st.json(response.json())  # Display the error response for debugging
