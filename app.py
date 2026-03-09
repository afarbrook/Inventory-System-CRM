import streamlit as st
from utils.accounts import(
    login,
    createAccount
)

def showLoginPage():
    with st.form("login_form"):
        username = st.text_input("username")
        password = st.text_input("password")
        col1, col2 = st.columns(2)
        with col1:
            submit_login = st.form_submit_button("Log In")
        with col2:
            submit_create = st.form_submit_button("Create Account")

        if submit_login:
            if(login(username, password)):
                st.session_state["logged in"] = True
                st.session_state["username"] = username
                st.success("Login successful!")
                st.switch_page("pages/Dashboard.py")
            else:
                st.error("Invalid username of password. Please try again")
        if submit_create:
            createAccount(username, password)
            st.session_state["logged in"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
            st.switch_page("pages/Dashboard.py")


st.title("Welcome! Please log in.")

if("logged in" not in st.session_state):
    st.session_state["logged in"] = False
    showLoginPage()
    st.stop()
if(not st.session_state["logged in"]):
    showLoginPage()
    st.stop()
else:
    st.switch_page("pages/Dashboard.py")








