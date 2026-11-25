"""Pagina de inicio: presentacion, KPIs, equipo y creditos."""
import streamlit as st
from src.data import verificar_datos, estadisticas_generales

df = verificar_datos()
stats = estadisticas_generales(df)

col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    try:
        st.image("assets/logo.png", width=140)
    except Exception:
        st.markdown("<h1 style='font-size:70px;'>🏅</h1>", unsafe_allow_html=True)
with col_titulo:
    st.markdown("# ATHLOS")
    st.markdown("### *La historia de los Juegos Olimpicos, contada por sus protagonistas.*")
    st.write("Explora, analiza y juega con mas de un siglo de hazanas deportivas.")

st.divider()

st.markdown("## Sobre los datos")
st.markdown(
    f"ATHLOS usa el historico de atletas y resultados de los Juegos Olimpicos "
    f"(fuente: Kaggle - 120 years of Olympic history), con ediciones entre "
    f"**{stats['anio_min']}** y **{stats['anio_max']}**."
)

st.markdown("## Indicadores generales")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros totales", f"{stats['registros']:,}")
c2.metric("Atletas unicos",   f"{stats['atletas']:,}")
c3.metric("Paises (NOC)",     f"{stats['paises']}")
c4.metric("Deportes",         f"{stats['deportes']}")

st.divider()

st.markdown("## Que puedes hacer?")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Explorar")
    st.write("Filtra por pais, deporte, anio, medalla y temporada.")
    if st.button("Ir a Explorar", key="btn_explorar"):
        st.switch_page("pages/explorar.py")
with col2:
    st.markdown("### Jugar")
    st.write("Pon a prueba tu conocimiento con la Trivia Olimpica.")
    if st.button("Ir a Jugar", key="btn_jugar"):
        st.switch_page("pages/jugar.py")
with col3:
    st.markdown("### Mis datos")
    st.write("Consulta tu historial de partidas y progreso.")
    if st.button("Ir a Mis datos", key="btn_misdatos"):
        st.switch_page("pages/mis_datos.py")

st.divider()

st.markdown("## Equipo desarrollador")
st.write("Estudiantes de Ingenieria Industrial - Universidad de Antioquia")
colA, colB = st.columns(2)
with colA:
    try:
        st.image("assets/foto_estudiante_1.jpg", width=180)
    except Exception:
        st.info("Foto estudiante 1")
    st.markdown("**Maria Clara Gomez**")
    st.caption("Ingenieria Industrial - Analisis de datos")
with colB:
    try:
        st.image("assets/foto_estudiante_2.jpg", width=180)
    except Exception:
        st.info("Foto estudiante 2")
    st.markdown("**Daniel Montoya**")
    st.caption("Ingenieria Industrial - Desarrollo y UX")

st.divider()

st.markdown("## Creditos y licencias")
st.markdown(
    "- **Datos:** 120 years of Olympic history (Kaggle, dominio publico)\n"
    "- **Fotografias:** archivo personal de los integrantes\n"
    "- **Logo:** diseno propio\n"
    "- **Codigo:** licencia MIT (ver docs/LICENSE.md)"
)
