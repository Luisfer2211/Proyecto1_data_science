
import os
import re

import pandas as pd

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_RAIZ = os.path.join(CARPETA_SCRIPT, "..")
CARPETA_DATA = os.path.join(CARPETA_RAIZ, "data")
CARPETA_INTERIM = os.path.join(CARPETA_DATA, "interim")


# ademas de cadena vacia / solo espacios.
PLACEHOLDERS_FALTANTE = {"N/A", "NA", "NULL", "-", ".", "SIN DATO", "--"}


def es_vacio(valor):
    """True si el valor es NaN, cadena vacia, o solo espacios en blanco."""
    if pd.isna(valor):
        return True
    return str(valor).strip() == ""


def es_faltante(valor):
    """es_vacio() + placeholders conocidos (N/A, NULL, -, ., Sin dato, --)."""
    if es_vacio(valor):
        return True
    return str(valor).strip().upper() in PLACEHOLDERS_FALTANTE


def normalizar_espacios(serie: pd.Series) -> pd.Series:
    """Trim + colapsa espacios internos multiples a uno solo. Preserva NA."""
    return serie.map(lambda v: re.sub(r"\s+", " ", str(v).strip()) if pd.notna(v) else v)


def marcar_faltantes_como_na(serie: pd.Series, tratar_placeholders=True) -> pd.Series:
    """Convierte celdas vacias/placeholder a pd.NA real (no cadena vacia)."""
    test = es_faltante if tratar_placeholders else es_vacio
    return serie.map(lambda v: pd.NA if test(v) else v)


class RegistroTransformaciones:
    """Acumula filas para la tabla de transformaciones (Actividad 6) de una fase."""

    def __init__(self, fase: str):
        self.fase = fase
        self.filas = []

    def registrar(self, variable, problema_detectado, transformacion, registros_afectados, justificacion):
        self.filas.append(
            {
                "fase": self.fase,
                "variable": variable,
                "problema_detectado": problema_detectado,
                "transformacion": transformacion,
                "registros_afectados": int(registros_afectados),
                "justificacion": justificacion,
            }
        )
        print(f"[{self.fase}] {variable}: {transformacion} -> {registros_afectados} registros afectados")

    def a_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.filas,
            columns=["fase", "variable", "problema_detectado", "transformacion", "registros_afectados", "justificacion"],
        )

    def guardar(self, ruta_csv):
        os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)
        self.a_dataframe().to_csv(ruta_csv, index=False, encoding="utf-8-sig")
        print(f"Registro de transformaciones de {self.fase} guardado en: {ruta_csv}")
