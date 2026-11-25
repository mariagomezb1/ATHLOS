"""
Generadores de preguntas para la Trivia Olimpica ATHLOS.
"""
import random
import pandas as pd
from src.data import Pregunta


def _opciones_distractoras(opciones_reales, correcta, n=3):
    candidatas = [o for o in opciones_reales if str(o) != str(correcta)]
    random.shuffle(candidatas)
    return [str(x) for x in candidatas[:n]]


def pregunta_deporte(df):
    sub = df.dropna(subset=["Name", "Sport", "Games"])
    if sub.empty:
        return None
    fila = sub.sample(1).iloc[0]
    deportes = df["Sport"].dropna().unique().tolist()
    distractores = _opciones_distractoras(deportes, fila["Sport"])
    if len(distractores) < 3:
        return None
    opciones = [fila["Sport"]] + distractores
    random.shuffle(opciones)
    return Pregunta(
        f"En que deporte compitio {fila['Name']} en {fila['Games']}?",
        opciones, fila["Sport"], "Deporte",
    )


def pregunta_pais(df):
    sub = df.dropna(subset=["Name", "NOC"])
    if sub.empty:
        return None
    fila = sub.sample(1).iloc[0]
    nocs = df["NOC"].dropna().unique().tolist()
    distractores = _opciones_distractoras(nocs, fila["NOC"])
    if len(distractores) < 3:
        return None
    opciones = [fila["NOC"]] + distractores
    random.shuffle(opciones)
    return Pregunta(
        f"A que pais (NOC) represento {fila['Name']} en {fila['Games']}?",
        opciones, fila["NOC"], "Pais",
    )


def pregunta_edad(df):
    sub = df.dropna(subset=["Name", "Age", "Games"])
    if sub.empty:
        return None
    fila = sub.sample(1).iloc[0]
    edad = int(fila["Age"])
    opciones = {edad}
    intentos = 0
    while len(opciones) < 4 and intentos < 50:
        intentos += 1
        delta = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        cand = edad + delta
        if 10 <= cand <= 80:
            opciones.add(cand)
    if len(opciones) < 4:
        return None
    opciones = [str(o) for o in opciones]
    random.shuffle(opciones)
    return Pregunta(
        f"Que edad tenia {fila['Name']} en {fila['Games']}?",
        opciones, str(edad), "Edad",
    )


def pregunta_medallas(df):
    oro = df[df["Medal"] == "Gold"]
    if oro.empty:
        return None
    anio = random.choice(oro["Year"].unique().tolist())
    sub = oro[oro["Year"] == anio]
    conteo = sub["NOC"].value_counts()
    if len(conteo) < 4:
        return None
    noc = random.choice(conteo.index[: min(10, len(conteo))].tolist())
    correcta = int(conteo[noc])
    opciones = {correcta}
    intentos = 0
    while len(opciones) < 4 and intentos < 50:
        intentos += 1
        delta = random.choice([-3, -2, -1, 1, 2, 3, 4, 5])
        cand = correcta + delta
        if cand > 0:
            opciones.add(cand)
    if len(opciones) < 4:
        return None
    opciones = [str(o) for o in opciones]
    random.shuffle(opciones)
    return Pregunta(
        f"Cuantas medallas de ORO gano {noc} en los Juegos de {int(anio)}?",
        opciones, str(correcta), "Medallas",
    )


def generar_preguntas(df, n=10):
    """Genera n preguntas variadas usando los 4 generadores."""
    generadores = [pregunta_deporte, pregunta_pais, pregunta_edad, pregunta_medallas]
    preguntas = []
    intentos = 0
    while len(preguntas) < n and intentos < n * 10:
        intentos += 1
        try:
            p = random.choice(generadores)(df)
            if p is not None:
                preguntas.append(p)
        except Exception:
            continue
    return preguntas