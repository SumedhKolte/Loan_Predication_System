import streamlit as st
import numpy as np
import pandas as pd

def main():
    # Set page config
    st.set_page_config(page_title="EMI Calculator", page_icon="💰")
    
    # Add custom CSS for better UI
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📊 Loan EMI Calculator")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        loan_amount = st.number_input(
            label="Loan Amount (₹)",
            min_value=10000,
            max_value=10000000,
            value=100000,
            step=10000,
            help="Enter the loan amount you wish to borrow"
        )
        
        tenure_years = st.number_input(
            label="Loan Tenure (Years)",
            min_value=1,
            max_value=30,
            value=5,
            help="Enter loan tenure in years"
        )
    
    with col2:
        interest_rate = st.slider(
            label="Interest Rate (%)",
            min_value=5.0,
            max_value=20.0,
            value=10.0,
            step=0.1,
            help="Select the annual interest rate"
        )
    
    if st.button("Calculate EMI", key="calculate_btn"):
        r = interest_rate/(12*100)
        n = tenure_years * 12
        emi = loan_amount * r * ((1+r)**n)/((1+r)**n - 1)
        total_payment = emi * n
        total_interest = total_payment - loan_amount
        
        st.markdown("---")
        st.subheader("Loan Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Monthly EMI", value=f"₹{emi:,.2f}")
        with col2:
            st.metric(label="Total Interest", value=f"₹{total_interest:,.2f}")
        with col3:
            st.metric(label="Total Payment", value=f"₹{total_payment:,.2f}")
        
        # Show amortization schedule
        st.markdown("---")
        st.subheader("Amortization Schedule")
        
        schedule = []
        balance = loan_amount
        for month in range(1, n+1):
            interest = balance * r
            principal = emi - interest
            balance = balance - principal
            schedule.append({
                "Month": month,
                "EMI": f"₹{emi:,.2f}",
                "Principal": f"₹{principal:,.2f}",
                "Interest": f"₹{interest:,.2f}",
                "Balance": f"₹{balance:,.2f}"
            })
        
        df = pd.DataFrame(schedule)
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()