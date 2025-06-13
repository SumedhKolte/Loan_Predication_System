import streamlit as st
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
from Login import login_page  # Update import to use pages directory

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Check if user is logged in
if not st.session_state['logged_in']:
    login_page()
else:
    # Update model loading with error handling
    try:
        model_path = Path(__file__).parent.parent / 'model.pkl'
        scaler_path = Path(__file__).parent.parent / 'scaler.pkl'
        
        if not model_path.exists():
            st.error(f"Model file not found at {model_path}")
            st.stop()
        elif not scaler_path.exists():
            st.error(f"Scaler file not found at {scaler_path}")
            st.stop()
        else:
            # Use pickle instead of pk alias
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.stop()

    # Update data file path
    df = pd.read_csv('bank_data.csv')  # Changed to relative path

    # Update navigation URLs to use relative paths
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Navigation Menu</div>', unsafe_allow_html=True)
        
        # Update URLs to use relative paths
        st.link_button(
            "💰 Compare Rates",
            url="Compare_Rates",  # Remove http://localhost:8502
            use_container_width=True,
        )
        
        st.link_button(
            "🧮 EMI Calculator",
            url="EMI_Calculator",  # Remove http://localhost:8503
            use_container_width=True,
        )
        
        st.link_button(
            "📄 Document Verification",
            url="Document_Verification",  # Remove http://localhost:8504
            use_container_width=True,
        )
        
        # Separator
        st.markdown('---')
        
        # Logout button
        if st.button('🚪 Logout', key='logout', use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # Add custom CSS for the sidebar buttons
    st.markdown("""
        <style>
        /* Sidebar styling */
        .sidebar-title {
            text-align: center;
            padding: 10px 0;
            font-size: 20px;
            font-weight: bold;
            border-bottom: 2px solid #4CAF50;
            margin-bottom: 20px;
        }
        
        /* Link button styling */
        .stButton>button, .element-container.css-1p1nwyz.e1f1d6gn0 > div {
            background-color: #4CAF50 !important;
            color: white !important;
            border: none !important;
            padding: 10px 15px !important;
            font-size: 16px !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            margin-bottom: 10px !important;
            transition: all 0.3s ease !important;
            text-align: left !important;
            width: 100% !important;
        }
        
        .stButton>button:hover, .element-container.css-1p1nwyz.e1f1d6gn0 > div:hover {
            background-color: #388e3c !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        }
        
        /* Active button state */
        .stButton>button:active, .element-container.css-1p1nwyz.e1f1d6gn0 > div:active {
            transform: translateY(0px);
        }
        </style>
    """, unsafe_allow_html=True)

    st.header('Loan Prediction App')

    # Update the CSS section with these additional styles:
    st.markdown("""
        <style>
        .button-container {
            display: flex;
            gap: 35px;
            margin-bottom: 20px;
            justify-content: flex-start;
            align-items: center;
        }
        
        /* Style for Streamlit's default button */
        .stButton > button {
            background-color: #4CAF50 !important;
            color: white !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            border: none !important;
            cursor: pointer !important;
            width: 180px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease-in-out !important;
        }

        .stButton > button:hover {
            background-color: #388e3c !important;
            transform: scale(1.05);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15) !important;
        }
        
        .redirect-button {
            background-color: #4CAF50;
            color: white !important;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none !important;
            display: inline-block;
            font-size: 16px;
            font-weight: 600;
            width: 180px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease-in-out;
            margin-top: 30px;
        }

        .redirect-button:hover {
            background-color: #388e3c;
            transform: scale(1.05);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
            color: white !important;
            text-decoration: none !important;
        }

        .redirect-button i {
            margin-right: 8px;
            transition: transform 0.3s ease-in-out;
        }

        .redirect-button:hover i {
            transform: rotate(360deg);
        }

        /* Keep your existing popup styles */
        .popup {
            padding: 15px 25px;
            border-radius: 10px;
            margin: 20px 0;
            font-weight: 600;
            font-size: 18px;
            text-align: center;
        }
        
        .popup.approved {
            background-color: #4CAF50;
            color: white;
        }
        
        .popup.rejected {
            background-color: #f44336;
            color: white;
        }

        /* Popup animation */
        @keyframes slideInAndFade {
            0% { transform: translate(-50%, -100%); opacity: 0; }
            10% { transform: translate(-50%, 20px); opacity: 1; }
            90% { transform: translate(-50%, 20px); opacity: 1; }
            100% { transform: translate(-50%, -100%); opacity: 0; }
        }

        .popup {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            min-width: 350px;
            padding: 20px 30px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 18px;
            text-align: center !important;  /* Force center alignment */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            animation: slideInAndFade 3s ease-in-out forwards;
        }

        .popup > div {
            width: 100%;
            text-align: center !important;
        }

        .popup-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
        }

        .popup span {
            font-size: 24px;
            display: block;
            margin-bottom: 10px;
            text-align: center;
        }

        .popup br + span {
            display: inline-block;
            margin: 5px 0;
        }

        /* Update the bullet points styling */
        .popup ul {
            list-style-position: inside;
            padding-left: 0;
            text-align: left;
            margin: 10px auto;
            width: fit-content;
        }

        .popup li {
            text-align: left;
            margin: 5px 0;
        }

        /* Dismissible popup styling */
        .popup-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 998;
            display: none;
        }
        
        .popup.rejected {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #fff;
            padding: 25px;
            border-radius: 15px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: 999;
            animation: fadeIn 0.3s ease-out;
            color: #333;
        }
        
        .popup-close {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            cursor: pointer;
            color: #666;
            background: transparent;
            border: none;
            border-radius: 50%;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .popup-close:hover {
            background-color: rgba(244, 67, 54, 0.1);
            color: #f44336;
        }

        /* Update the popup header styling */
        .popup-header {
            position: relative;
            padding-right: 40px;  /* Make space for the close button */
        }
        
        .sidebar-title {
        text-align: center;
        padding: 10px 0;
        font-size: 20px;
        font-weight: bold;
        border-bottom: 2px solid #4CAF50;
        margin-bottom: 20px;
        }
        
        /* Update sidebar button styles */
        .stButton > button {
            width: 100% !important;
            margin-bottom: 10px !important;
            text-align: left !important;
            padding: 12px 15px !important;
        }
        </style>

        <!-- Add Font Awesome for icons -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    """, unsafe_allow_html=True)

    # First update the CSS for the button container:
    st.markdown("""
        <style>
        .button-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 20px 0;
            padding: 10px 0;
        }
        
        .redirect-button {
            margin-top: 0 !important;  /* Remove top margin */
        }
        </style>
    """, unsafe_allow_html=True)

    # Update input elements with proper labels
    no_of_dep = st.slider(
        label='Number of Dependents',
        min_value=0,
        max_value=5,
        help='Select the number of dependents'
    )

    grad = st.selectbox(
        label='Education Status',
        options=['Graduated', 'Not Graduated'],
        help='Select your education status'
    )

    self_emp = st.selectbox(
        label='Self Employed',
        options=['Yes', 'No'],
        help='Are you self employed?'
    )

    Annual_Income = st.slider(
        label='Annual Income (₹)',
        min_value=0,
        max_value=10000000,
        help='Select your annual income'
    )

    Loan_Amount = st.slider(
        label='Loan Amount (₹)',
        min_value=0,
        max_value=10000000,
        help='Select the loan amount you need'
    )

    Loan_Dur = st.slider(
        label='Loan Duration (Years)',
        min_value=0,
        max_value=20,
        help='Select the loan duration in years'
    )

    Cibil = st.slider(
        label='CIBIL Score',
        min_value=0,
        max_value=900,
        help='Enter your CIBIL score'
    )

    Assets = st.slider(
        label='Assets Value (₹)',
        min_value=0,
        max_value=10000000,
        help='Enter the total value of your assets'
    )

    if grad =='Graduated':
        grad_s =0
    else:
        grad_s = 1

    if self_emp =='No':
        emp_s =0
    else:
        emp_s = 1
        

    st.markdown('<div class="button-row">', unsafe_allow_html=True)

    # Left side - Predict button
    col1, col2 = st.columns([1, 6])
    with col1:
        predict_clicked = st.button("🔍 Predict", key="predict_button")

    if predict_clicked:
        if Annual_Income == 0:
            st.error("Annual Income cannot be zero")
        else:
            pred_data = pd.DataFrame(
                [[no_of_dep,grad_s,emp_s,Annual_Income,Loan_Amount,Loan_Dur,Cibil,Assets]],
                columns=['no_of_dependents','education','self_employed','income_annum',
                        'loan_amount','loan_term','cibil_score','Assets']
            )
            pred_data = scaler.transform(pred_data)
            predict = model.predict(pred_data)
            
            if predict[0] == 1:
                # Approved loan case - keep as is
                loan_ratio = Loan_Amount / Annual_Income
                suggestions = []
                
                if loan_ratio > 0.5:
                    suggestions.append("Consider taking a smaller loan amount for better manageability")
                if Loan_Dur > 15:
                    suggestions.append("Long loan duration may result in higher interest payments")
                if Cibil < 700:
                    suggestions.append("Improve your CIBIL score for better interest rates")
                    
                # For approved loans:
                st.markdown(
                    f'''
                    <div class="result-container result-approved">
                        <div class="result-header">
                            <span>✅</span>
                            <h3>Loan Approved</h3>
                        </div>
                        <div class="result-content">
                            <strong>Loan Details:</strong>
                            <ul>
                                <li>Loan Amount: ₹{Loan_Amount:,.2f}</li>
                                <li>Duration: {Loan_Dur} years</li>
                                <li>Monthly Income: ₹{Annual_Income/12:,.2f}</li>
                            </ul>
                            <strong>Suggestions:</strong>
                            <ul>
                                {" ".join([f"<li>{s}</li>" for s in suggestions]) if suggestions 
                                else "<li>You have a strong application!</li>"}
                            </ul>
                        </div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
            else:
                # Rejection case
                reasons = []
                
                # Check rejection conditions
                if Loan_Amount / Annual_Income > 0.8:
                    reasons.append("Loan amount too high compared to annual income")
                if Annual_Income < Loan_Amount * 0.3:
                    reasons.append("Income is too low compared to loan amount")
                if Cibil < 500:
                    reasons.append("Low CIBIL score")
                if Assets < Loan_Amount * 0.5:
                    reasons.append("Insufficient assets for loan security")
                
                if not reasons:
                    reasons.append("Multiple factors don't meet our lending criteria")

                # Display rejection message in the same style as approval
                st.markdown(
                    f'''
                    <div class="result-container result-rejected">
                        <div class="result-header">
                            <span>❌</span>
                            <h3>Loan Application Rejected</h3>
                        </div>
                        <div class="result-content">
                            <strong>Application Details:</strong>
                            <ul>
                                <li>Requested Amount: ₹{Loan_Amount:,.2f}</li>
                                <li>CIBIL Score: {Cibil}</li>
                                <li>Income to Loan Ratio: {(Loan_Amount/Annual_Income*100):.1f}%</li>
                            </ul>
                            <strong>Reasons for Rejection:</strong>
                            <ul>
                                {"".join([f"<li>{r}</li>" for r in reasons])}
                            </ul>
                        </div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

    # Right side - Compare Rates button
    with col2:
        st.markdown(
            '''
            <div style="display: flex; justify-content: flex-end;">
                <a href="http://localhost:8502" target="_self" class="redirect-button">
                    <i class="fas fa-sync-alt"></i> Compare Rates
                </a>
            </div>
            ''',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)