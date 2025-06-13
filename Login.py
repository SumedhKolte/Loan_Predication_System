import streamlit as st
import pandas as pd
import hashlib
from pathlib import Path

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

def create_user_table():
    try:
        df = pd.read_csv('users.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['username', 'password'])
        df.to_csv('users.csv', index=False)
    return df

def add_user(username, password):
    df = create_user_table()
    if username in df['username'].values:
        return False
    hashed_password = make_hashes(password)
    df.loc[len(df)] = [username, hashed_password]
    df.to_csv('users.csv', index=False)
    return True

def login_user(username, password):
    df = create_user_table()
    if username in df['username'].values:
        stored_password = df[df['username'] == username]['password'].iloc[0]
        return check_hashes(password, stored_password)
    return False

def login_page():
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            border-radius: 10px;
            /* Remove the background-color and adjust box-shadow */
            box-shadow: none;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .centered-text {
            text-align: center;
            margin-bottom: 20px;
            color: white;  /* Make the title text white */
        }
        /* Style for the subheader */
        .stSubheader {
            color: white !important;
        }
        /* Style for input labels */
        .stTextInput > label {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="centered-text">Welcome to Loan Prediction System</h1>', unsafe_allow_html=True)

    menu = ["Login", "SignUp"]
    choice = st.selectbox("", menu)

    if choice == "Login":
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("Login Section")

        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            if login_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Logged In as {}".format(username))
                st.rerun()

            else:
                st.error("Incorrect Username/Password")

        st.markdown('</div>', unsafe_allow_html=True)

    elif choice == "SignUp":
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')

        if st.button("SignUp"):
            if new_password == confirm_password:
                if add_user(new_user, new_password):
                    st.success("You have successfully created an account")
                    st.info("Go to Login Menu to login")
                else:
                    st.error("Username already exists")
            else:
                st.error("Passwords don't match")

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    login_page()