import streamlit as st
import pandas as pd

# Load the CSV data
try:
    df = pd.read_csv('./bank_data.csv')  # Updated path
except FileNotFoundError:
    st.error("Bank data file not found. Please ensure bank_data.csv is in the root directory.")
    st.stop()

# Set page title and icon
st.set_page_config(
    page_title="Loan Rate Comparison", 
    page_icon="🏦", 
    layout="wide"
)

# Add header with custom styling
st.markdown(
    """
    <style>
    .main {background-color: #f7f9fd;}
    .stButton > button {background-color: #4CAF50; color: white; font-size: 18px; border-radius: 12px; padding: 10px 24px;}
    .stSelectbox, .stSlider, .stDataFrame {border-radius: 12px;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏦 Compare Bank Loan Interest Rates 🏦")
st.markdown("### Find the best bank with the lowest interest rates for your preferred loan type.")

# Dropdown to select loan type with proper label
loan_type = st.selectbox(
    label="Select Loan Type",  # Added proper label
    options=["Home Loan", "Personal Loan", "Business Loan"],
    key="loan_type_selector"
)

# Mapping loan type to column name
loan_column_mapping = {
    "Home Loan": "home_loan_rate",
    "Personal Loan": "personal_loan_rate",
    "Business Loan": "business_loan_rate"
}

# Get the selected column name
loan_column = loan_column_mapping[loan_type]

# Filter banks with valid interest rates for the selected loan type
filtered_df = df[df[loan_column] != '-'][['name_of_lender', loan_column]].dropna()
filtered_df[loan_column] = pd.to_numeric(filtered_df[loan_column])

# Find the best bank with the lowest interest rate
if not filtered_df.empty:
    best_bank = filtered_df.loc[filtered_df[loan_column].idxmin()]
    st.success(
        f"🏦 Best Bank for **{loan_type}**: **{best_bank['name_of_lender']}** with Rate: **{best_bank[loan_column]}%**"
    )
else:
    st.error("❗ No data available for the selected loan type.")

# Display full comparison table with proper labels
st.markdown("### 📊 Full Interest Rate Comparison")
display_df = filtered_df.rename(columns={
    'name_of_lender': 'Bank Name',
    loan_column: "Interest Rate (%)"
})

# Use streamlit's dataframe with proper column configuration
st.dataframe(
    display_df,
    column_config={
        "Bank Name": st.column_config.TextColumn(
            "Bank Name",
            help="Name of the lending institution"
        ),
        "Interest Rate (%)": st.column_config.NumberColumn(
            "Interest Rate (%)",
            help="Annual interest rate",
            format="%.2f%%",
        ),
    },
    hide_index=True,
)

# Footer
st.markdown("---")
st.markdown(
    "💡 **Tip:** Compare different loan types and choose the most affordable option!"
)
