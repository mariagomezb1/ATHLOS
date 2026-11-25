"""Pagina de exploracion: filtros, tabla, detalle, estadisticas y graficos."""
import pandas as pd
import plotly.express as px
import streamlit as st
from src.data import verificar_datos

df = verificar_datos()

st.markdown("# Explorar los datos")
st.caption("Filtra, selecciona un registro y descubre su historia.")

with st.sidebar:
    st.markdown("### Filtros")
    sexos = sorted(df["Sex"].dropna().unique().tolist()) if "Sex" in df.columns else []
    sexo_sel = st.multiselect("Sexo", sexos, default=sexos)

    nocs = sorted(df["NOC"].dropna().unique().tolist()) if "NOC" in df.columns else []
    noc_sel = st.multiselect("Pais (NOC)", nocs, default=[])

    deportes = sorted(df["Sport"].dropna().unique().tolist()) if "Sport" in df.columns else []
    deporte_sel = st.multiselect("Deporte", deportes, default=[])

    temporadas = sorted(df["Season"].dropna().unique().tolist()) if "Season" in df.columns else []
    temporada_sel = st.multiselect("Temporada", temporadas, default=temporadas)

    anio_min, anio_max = int(df["Year"].min()), int(df["Year"].max())
    rango_anios = st.slider("Rango de anios", anio_min, anio_max, (anio_min, anio_max))

    medallas = ["Gold", "Silver", "Bronze", "Sin medalla"]
    medalla_sel = st.multiselect("Medalla", medallas, default=medallas)

filtrado = df.copy()
if sexo_sel and "Sex" in filtrado.columns:
    filtrado = filtrado[filtrado["Sex"].isin(sexo_sel)]
if noc_sel:
    filtrado = filtrado[filtrado["NOC"].isin(noc_sel)]
if deporte_sel:
    filtrado = filtrado[filtrado["Sport"].isin(deporte_sel)]
if temporada_sel:
    filtrado = filtrado[filtrado["Season"].isin(temporada_sel)]
filtrado = filtrado[(filtrado["Year"] >= rango_anios[0]) & (filtrado["Year"] <= rango_anios[1])]
if medalla_sel:
    filtrado = filtrado[filtrado["Medal"].isin(medalla_sel)]

st.markdown(f"**Registros que coinciden con los filtros:** `{len(filtrado):,}`")

if filtrado.empty:
    st.warning("No hay registros con los filtros seleccionados.")
    st.stop()

st.markdown("### Tabla de registros")
columnas_mostrar = [c for c in ["Name", "Sex", "Age", "NOC", "Year", "Sport", "Event", "Medal"]
                    if c in filtrado.columns]
evento = st.dataframe(
    filtrado[columnas_mostrar].head(500),
    on_select="rerun",
    selection_mode="single-row",
    use_container_width=True,
    hide_index=True,
    height=350,
)

st.markdown("### Detalle del registro")
if evento.selection.rows:
    idx = evento.selection.rows[0]
    reg = filtrado.iloc[idx]

    clave = f"{reg.get('Name','')}-{reg.get('Year','')}-{reg.get('Event','')}"
    if clave not in st.session_state["vistos"]:
        st.session_state["vistos"].add(clave)
        st.session_state["registros_consultados"] += 1

    c1, c2, c3 = st.columns(3)
    c1.metric("Atleta", reg.get("Name", "N/D"))
    c2.metric("Pais (NOC)", reg.get("NOC", "N/D"))
    c3.metric("Medalla", reg.get("Medal", "Sin medalla"))

    c4, c5, c6 = st.columns(3)
    c4.metric("Deporte", reg.get("Sport", "N/D"))
    c5.metric("Anio", int(reg.get("Year", 0)) if pd.notna(reg.get("Year")) else "N/D")
    c6.metric("Edad", int(reg["Age"]) if pd.notna(reg.get("Age")) else "N/D")

    st.write(f"**Evento:** {reg.get('Event', 'N/D')}")
else:
    st.info("Haz clic en una fila de la tabla para ver el detalle.")

st.markdown("### Estadisticas descriptivas")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros filtrados", f"{len(filtrado):,}")
c2.metric("Atletas unicos",     f"{filtrado['Name'].nunique():,}" if "Name" in filtrado else "-")
c3.metric("Paises representados",f"{filtrado['NOC'].nunique()}"     if "NOC"  in filtrado else "-")
edad_prom = filtrado["Age"].dropna().mean() if "Age" in filtrado else 0
c4.metric("Edad promedio", f"{edad_prom:.1f} anios" if edad_prom else "-")

st.markdown("### Visualizaciones")

if "Medal" in filtrado.columns and "NOC" in filtrado.columns:
    con_medalla = filtrado[filtrado["Medal"].isin(["Gold", "Silver", "Bronze"])]
    if not con_medalla.empty:
        top = con_medalla.groupby(["NOC", "Medal"]).size().reset_index(name="Cantidad")
        top_paises = top.groupby("NOC")["Cantidad"].sum().nlargest(10).index
        top = top[top["NOC"].isin(top_paises)]
        fig1 = px.bar(
            top, x="NOC", y="Cantidad", color="Medal", barmode="stack",
            title="Top 10 paises por medallas",
            color_discrete_map={"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"},
        )
        fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           font_color="#F1F5F9")
        st.plotly_chart(fig1, use_container_width=True)

if "Age" in filtrado.columns:
    edades = filtrado["Age"].dropna()
    if not edades.empty:
        fig2 = px.histogram(
            edades, nbins=25, title="Distribucion de edades",
            labels={"value": "Edad", "count": "Cantidad"},
            color_discrete_sequence=["#4A90E2"],
        )
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           font_color="#F1F5F9")
        st.plotly_chart(fig2, use_container_width=True)
        