import streamlit as st

# Verifica si el usuario ha iniciado sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Funciones para iniciar y cerrar sesión
def login():
    st.session_state.logged_in = True
    st.experimental_rerun()  # Utiliza rerun para actualizar la página

def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()  # Utiliza rerun para actualizar la página

# Mostrar la página de inicio de sesión o el contenido principal según el estado de inicio de sesión
if st.session_state.logged_in:
    st.sidebar.title("Menú")
    selection = st.sidebar.radio("Navegación", ["Dashboard Match", "Dashboard Individual", "Formularios"])
    
    if selection == "Dashboard Match":
        st.title("Dashboard Match")
        # Llama a tu script para el dashboard de partidos aquí
        # exec(open("reports/dashboard_match.py").read())
    elif selection == "Dashboard Individual":
        st.title("Dashboard Individual")
        # Llama a tu script para el dashboard individual aquí
        # exec(open("reports/dashboard_ind.py").read())
    elif selection == "Formularios":
        st.title("Formularios")
        # Llama a tu script para los formularios aquí
        # exec(open("form/1_Form.py").read())

    if st.sidebar.button("Log out"):
        logout()
else:
    st.title("Log in")
    if st.button("Log in"):
        login()
