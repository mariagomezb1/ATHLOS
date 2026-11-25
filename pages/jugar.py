"""Pagina del juego: Trivia Olimpica ATHLOS."""
import streamlit as st
from src.data import verificar_datos, guardar_partida
from src.juego import generar_preguntas

df = verificar_datos()

st.markdown("# Trivia Olimpica ATHLOS")
st.caption("Demuestra cuanto sabes de la historia de los Juegos Olimpicos.")

with st.expander("Instrucciones del juego", expanded=st.session_state.get("juego") is None):
    st.markdown(
        """
        1. La trivia tiene **10 preguntas** generadas a partir de los datos reales.
        2. Cada pregunta tiene **4 opciones** y una sola respuesta correcta.
        3. Cada acierto suma **10 puntos** (maximo: 100 puntos).
        4. Al final veras tu puntaje y podras iniciar otra partida.
        5. Tus estadisticas se conservan durante la sesion en la pagina Mis datos.
        """
    )


def iniciar_juego():
    preguntas = generar_preguntas(df, n=10)
    if not preguntas:
        st.error("No fue posible generar preguntas. Verifica los datos.")
        return
    st.session_state["juego"] = {
        "preguntas": preguntas,
        "indice": 0,
        "puntaje": 0,
        "respuestas": [],
        "guardado": False,
        "mostrar_feedback": False,
        "ultimo_acierto": False,
    }


if st.session_state.get("juego") is None:
    if st.button("Comenzar partida", type="primary", use_container_width=True):
        iniciar_juego()
        st.rerun()
    st.stop()

juego = st.session_state["juego"]
preguntas = juego["preguntas"]
indice = juego["indice"]

# --- Juego terminado ---
if indice >= len(preguntas):
    if not juego["guardado"]:
        guardar_partida(juego["puntaje"], len(preguntas))
        juego["guardado"] = True

    total = len(preguntas)
    puntaje = juego["puntaje"]
    porcentaje = round(puntaje / (total * 10) * 100, 1)

    st.markdown("## Partida terminada!")
    c1, c2, c3 = st.columns(3)
    c1.metric("Puntaje", f"{puntaje} / {total * 10}")
    c2.metric("Correctas", f"{puntaje // 10} / {total}")
    c3.metric("Porcentaje", f"{porcentaje}%")

    if porcentaje >= 80:
        st.balloons()
        st.success("Excelente! Eres un experto olimpico.")
    elif porcentaje >= 50:
        st.info("Buen trabajo! Sigue practicando.")
    else:
        st.warning("Puedes mejorar. Intentalo de nuevo!")

    with st.expander("Ver respuestas detalladas"):
        for i, (p, r) in enumerate(zip(preguntas, juego["respuestas"]), 1):
            ok = r == p.correcta
            st.markdown(f"**{i}.** {'[OK]' if ok else '[X]'} {p.enunciado}")
            st.caption(f"Tu respuesta: {r} - Correcta: {p.correcta}")

    if st.button("Jugar otra vez", type="primary", use_container_width=True):
        st.session_state["juego"] = None
        st.rerun()
    st.stop()

# --- Pregunta actual ---
pregunta = preguntas[indice]
progreso = indice / len(preguntas)

st.progress(progreso, text=f"Pregunta {indice + 1} de {len(preguntas)}")
st.caption(f"Categoria: {pregunta.categoria} - Puntaje actual: {juego['puntaje']} pts")
st.markdown(f"### {pregunta.enunciado}")

if juego["mostrar_feedback"]:
    if juego["ultimo_acierto"]:
        st.success(f"Correcto! La respuesta era {pregunta.correcta}.")
    else:
        st.error(f"Incorrecto. La respuesta correcta era {pregunta.correcta}.")
    if st.button("Siguiente pregunta", type="primary", use_container_width=True):
        juego["indice"] += 1
        juego["mostrar_feedback"] = False
        st.rerun()
else:
    respuesta = st.radio(
        "Selecciona tu respuesta:",
        pregunta.opciones,
        key=f"resp_{indice}",
        index=None,
    )
    col_ok, col_skip = st.columns(2)
    with col_ok:
        enviar = st.button("Responder", disabled=respuesta is None,
                           type="primary", use_container_width=True)
    with col_skip:
        saltar = st.button("Saltar pregunta", use_container_width=True)

    if enviar:
        acierto = pregunta.es_correcta(respuesta)
        juego["respuestas"].append(respuesta)
        if acierto:
            juego["puntaje"] += 10
        juego["ultimo_acierto"] = acierto
        juego["mostrar_feedback"] = True
        st.rerun()

    if saltar:
        juego["respuestas"].append("(sin respuesta)")
        juego["ultimo_acierto"] = False
        juego["mostrar_feedback"] = True
        st.rerun()
        