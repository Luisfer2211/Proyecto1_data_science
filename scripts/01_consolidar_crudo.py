import glob
import os

import pandas as pd

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_RAIZ = os.path.join(CARPETA_SCRIPT, "..")
CARPETA_RAW = os.path.join(CARPETA_RAIZ, "data", "raw")
SALIDA = os.path.join(CARPETA_RAIZ, "data", "establecimientos_diversificado_crudo.csv")

COLUMNAS = [
    "CODIGO", "DISTRITO", "DEPARTAMENTO", "MUNICIPIO", "ESTABLECIMIENTO",
    "DIRECCION", "TELEFONO", "SUPERVISOR", "DIRECTOR", "NIVEL", "SECTOR",
    "AREA", "STATUS", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL",
]


def main():
    archivos = sorted(glob.glob(os.path.join(CARPETA_RAW, "*_DIVERSIFICADO.csv")))
    if not archivos:
        raise SystemExit(
            f"No se encontraron archivos *_DIVERSIFICADO.csv en {CARPETA_RAW}. "
            "Corre primero scripts/00_descargar_crudo.py."
        )

    piezas = []
    resumen = []
    for ruta in archivos:
        nombre = os.path.basename(ruta)
        df = pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding="utf-8-sig")
        if list(df.columns) != COLUMNAS:
            raise ValueError(f"{nombre}: columnas inesperadas -> {list(df.columns)}")
        df["ARCHIVO_ORIGEN"] = nombre
        piezas.append(df)
        resumen.append((nombre, len(df)))

    crudo = pd.concat(piezas, ignore_index=True)

    print(f"{'Archivo':40s} {'Filas':>8s}")
    total = 0
    for nombre, n in resumen:
        print(f"{nombre:40s} {n:8d}")
        total += n
    print("-" * 50)
    print(f"{'TOTAL':40s} {total:8d}")

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    crudo.to_csv(SALIDA, index=False, encoding="utf-8-sig")
    print(f"\nGuardado: {SALIDA}")
    print(f"Filas totales: {len(crudo)}  |  Columnas: {crudo.shape[1]}")


if __name__ == "__main__":
    main()
