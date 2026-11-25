"""Pagina 'Mis datos': estadisticas del usuario durante la sesion."""
import pandas as pd
import plotly.express as px
import streamlit as st

st.markdown("# Mis datos")
st.caption("Tu actividad dentro de ATHLOS durante esta sesion.")

for k, v in {"partidas": [], "puntaje_acumulado": 0, "mejor_puntaje": 0,
             "registros_consultados": 0}.items():
    if k not in st.session_state:
        st.session_state[k] = v

partidas = st.session_state["partidas"]
sin_actividad = len(partidas) == 0 and st.session_state["registros_consultados"] == 0

if sin_actividad:
    st.info(
        "Aun no has jugado ni explorado registros. "
        "Ve a Jugar o Explorar para que aparezcan tus estadisticas."
    )
    st.stop()

st.markdown("## Resumen de actividad")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Partidas jugadas", len(partidas))
c2.metric("Puntaje acumulado", f"{st.session_state['puntaje_acumulado']} pts")
c3.metric("Mejor puntaje", f"{st.session_state['mejor_puntaje']} pts")
c4.metric("Registros consultados", st.session_state["registros_consultados"])

if partidas:
    df_partidas = pd.DataFrame(partidas)
    st.markdown("## Estadisticas de juego")
    c1, c2 = st.columns(2)
    c1.metric("Promedio por partida", f"{df_partidas['puntaje'].mean():.1f} pts")
    c2.metric("Mejor porcentaje",     f"{df_partidas['porcentaje'].max():.1f}%")

    st.markdown("## Historial de partidas")
    st.dataframe(
        df_partidas[["orden", "fecha", "puntaje", "total", "porcentaje"]],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("## Evolucion de tus resultados")
    fig = px.line(
        df_partidas, x="orden", y="porcentaje", markers=True,
        title="Porcentaje de acierto por partida",
        labels={"orden": "Partida", "porcentaje": "Porcentaje (%)"},
    )
    fig.update_traces(line_color="#FFD700", marker=dict(size=10, color="#FFD700"))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#F1F5F9", yaxis_range=[0, 105],
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aun no has jugado ninguna partida. Ve a Jugar para comenzar.")
    