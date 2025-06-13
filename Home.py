import streamlit as st

st.set_page_config(
    page_title="Loan Prediction System",
    page_icon="🏦",
    layout="wide"
)

st.title("Welcome to Loan Prediction System")
st.markdown("""
This system helps you:
- Apply for loans
- Compare interest rates
- Calculate EMI
- Verify documents
""")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.info("Please login to access all features")