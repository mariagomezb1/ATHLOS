"""
ATHLOS - Aplicacion web para explorar la historia olimpica.
Punto de entrada con navegacion multipagina.
"""
import streamlit as st
from src.data import inicializar_sesion


st.set_page_config(
    page_title="ATHLOS - Historia Olimpica",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

inicializar_sesion()

try:
    st.sidebar.image("assets/logo.png", use_container_width=True)
except Exception:
    st.sidebar.markdown("## ATHLOS")

paginas = [
    st.Page("pages/inicio.py",    title="Inicio",    icon="🏠", default=True),
    st.Page("pages/explorar.py",  title="Explorar",  icon="🔍"),
    st.Page("pages/jugar.py",     title="Jugar",     icon="🎮"),
    st.Page("pages/mis_datos.py", title="Mis datos", icon="👤"),
]

pg = st.navigation(paginas)
pg.run()