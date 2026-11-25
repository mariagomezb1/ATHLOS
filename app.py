"""
ATHLOS · Aplicación web para explorar la historia olímpica.
Punto de entrada con navegación multipágina.
"""
import streamlit as st
from src.data import inicializar_sesion

# ---- Configuración global de la página ----
st.set_page_config(
    page_title="ATHLOS · Historia Olímpica",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- Inicializar estado de sesión ----
inicializar_sesion()

# ---- Logo (si existe) ----
try:
    st.logo("assets/logo.png")
except Exception:
    pass

# ---- Navegación entre las 4 subpáginas ----
paginas = [
    st.Page("pages/inicio.py",    title="Inicio",    icon="🏠", default=True),
    st.Page("pages/explorar.py",  title="Explorar",  icon="🔍"),
    st.Page("pages/jugar.py",     title="Jugar",     icon="🎮"),
    st.Page("pages/mis_datos.py", title="Mis datos", icon="👤"),
]

pg = st.navigation(paginas)
pg.run()