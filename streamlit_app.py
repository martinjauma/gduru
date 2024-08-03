import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard_match = st.Page(
    "reports/dashboard_match.py", title="Dashboard Macht", icon=":material/dashboard:", default=True
)
dashboard_ind = st.Page(
    "reports/dashboard_ind.py", title="Dashboard Individual", icon=":material/dashboard:", default=False
)
form = st.Page("form/1_Form.py", title="Formularios", icon=":material/bug_report:")



if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard_match,dashboard_ind],
            "Form": [form]

        }
    )
else:
    pg = st.navigation([login_page])

pg.run()