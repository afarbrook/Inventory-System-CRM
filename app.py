import streamlit as st
from utils.accounts import(
    login,
    createAccount,
    checkAdmin
)

if("logged in" not in st.session_state):
    st.session_state["logged in"] = False


def showLoginPage():
    st.title("Welcome! Please log in.")
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
                st.session_state["logged in"]  = True
                st.session_state["username"]   = username
                st.session_state["admin"]      = checkAdmin()
                st.rerun()
            else:
                st.error("Invalid username of password. Please try again")
        if submit_create:
            createAccount(username, password)
            st.session_state["logged in"] = True
            st.session_state["username"]  = username
            st.session_state["admin"]     = checkAdmin()
            st.rerun()

if not st.session_state["logged in"]:
    # Pass only the login page so sidebar shows nothing
    pg = st.navigation({"Account": [st.Page(showLoginPage, title="Log In")]})
    pg.run()
    st.stop()
# --------------pages set up --------------------------------------
home      = st.Page("app.py",                title="Log In Page")
dashboard = st.Page("pages/Dashboard.py",    title="Dashboard")
auditLog  = st.Page("pages/AuditLog.py",     title="Audit Log")
edit      = st.Page("pages/Edit.py",         title="Edit Inventory")
imports   = st.Page("pages/Import.py",       title="Import File")
reports   = st.Page("pages/Reports.py",      title="Extract Reports")
search    = st.Page("pages/Search.py",       title="Search Database")
# -----------------------------------------------------------------
if st.session_state["admin"]:
    pg = st.navigation([dashboard, auditLog, edit, imports, reports, search])
else:
    pg = st.navigation([dashboard, imports, reports, search])
pg.run()







