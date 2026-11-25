"""
Modulo de carga de datos y gestion de sesion de ATHLOS.
"""
from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "datos.csv"


@st.cache_data(show_spinner="Cargando historia olimpica...")
def cargar_datos():
    """Carga data/datos.csv. Retorna None si hay error."""
    try:
        if not DATA_PATH.exists():
            return None
        df = pd.read_csv(DATA_PATH)
        if "Medal" in df.columns:
            df["Medal"] = df["Medal"].fillna("Sin medalla")
        return df
    except Exception:
        return None


def verificar_datos():
    """Carga datos y detiene la app si no existen."""
    df = cargar_datos()
    if df is None or df.empty:
        st.error("No se encontro data/datos.csv. Ejecuta data/limpieza.ipynb primero.")
        st.stop()
    return df


def estadisticas_generales(df):
    """Calcula indicadores generales del dataset."""
    if df is None or df.empty:
        return {"registros": 0, "atletas": 0, "paises": 0,
                "deportes": 0, "ediciones": 0, "anio_min": 0, "anio_max": 0}
    return {
        "registros": int(len(df)),
        "atletas": int(df["Name"].nunique()) if "Name" in df.columns else 0,
        "paises": int(df["NOC"].nunique()) if "NOC" in df.columns else 0,
        "deportes": int(df["Sport"].nunique()) if "Sport" in df.columns else 0,
        "ediciones": int(df["Games"].nunique()) if "Games" in df.columns else 0,
        "anio_min": int(df["Year"].min()) if "Year" in df.columns else 0,
        "anio_max": int(df["Year"].max()) if "Year" in df.columns else 0,
    }


def inicializar_sesion():
    """Inicializa las variables de session_state usadas por la app."""
    defaults = {
        "partidas": [],
        "puntaje_acumulado": 0,
        "mejor_puntaje": 0,
        "registros_consultados": 0,
        "vistos": set(),
        "juego": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def guardar_partida(puntaje, total):
    """Guarda una partida terminada en el historial."""
    partida = {
        "orden": len(st.session_state.partidas) + 1,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "puntaje": int(puntaje),
        "total": int(total),
        "porcentaje": round(puntaje / total * 100, 1) if total else 0.0,
    }
    st.session_state.partidas.append(partida)
    st.session_state.puntaje_acumulado += int(puntaje)
    st.session_state.mejor_puntaje = max(st.session_state.mejor_puntaje, int(puntaje))


class Pregunta:
    """Representa una pregunta de la Trivia Olimpica."""

    def __init__(self, enunciado, opciones, correcta, categoria):
        self.enunciado = enunciado
        self.opciones = opciones
        self.correcta = correcta
        self.categoria = categoria

    def es_correcta(self, respuesta):
        return str(respuesta) == str(self.correcta)

    def __repr__(self):
        return f"<Pregunta [{self.categoria}] {self.enunciado}>"