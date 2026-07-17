"""
Consolida los 23 archivos crudos (uno por departamento) descargados del
buscador de establecimientos del MINEDUC (nivel escolar = DIVERSIFICADO)
en un unico archivo CSV de datos crudos.

Dos formatos de entrada conviven en la carpeta:
  1. CSV limpio ya tabulado (columnas entre comillas, separadas por coma).
  2. Pagina HTML completa guardada con extension .csv (el sitio del MINEDUC
     lanzo un error de cliente al momento de guardar, pero la tabla de
     resultados igual quedo incrustada en el HTML). Se extrae la tabla
     con un parser HTML nativo (html.parser), sin dependencias externas.

El resultado es 100% reproducible: solo requiere los 23 CSV originales
en esta carpeta y la libreria estandar de Python + pandas.
"""

import csv
import glob
import os
from html.parser import HTMLParser

import pandas as pd

CARPETA = os.path.join(os.path.dirname(__file__), "..")
COLUMNAS = [
    "CODIGO", "DISTRITO", "DEPARTAMENTO", "MUNICIPIO", "ESTABLECIMIENTO",
    "DIRECCION", "TELEFONO", "SUPERVISOR", "DIRECTOR", "NIVEL", "SECTOR",
    "AREA", "STATUS", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL",
]


class TableExtractor(HTMLParser):
    """Extrae todas las filas <tr>/<td> de un HTML, sin importar el <table> al que pertenezcan."""

    def __init__(self):
        super().__init__()
        self.rows = []
        self._current_row = None
        self._current_cell = None
        self._in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._current_row = []
        elif tag == "td":
            self._in_cell = True
            self._current_cell = []

    def handle_endtag(self, tag):
        if tag == "td" and self._in_cell:
            text = "".join(self._current_cell)
            text = " ".join(text.split())  # colapsa espacios/saltos de linea
            self._current_row.append(text)
            self._in_cell = False
            self._current_cell = None
        elif tag == "tr" and self._current_row is not None:
            self.rows.append(self._current_row)
            self._current_row = None

    def handle_data(self, data):
        if self._in_cell:
            self._current_cell.append(data)


def es_html(ruta):
    with open(ruta, encoding="latin-1") as f:
        inicio = f.read(200)
    return inicio.strip().startswith("<script>") or "<!DOCTYPE" in inicio


def leer_csv_limpio(ruta):
    # Estos archivos se generaron con un Blob JS en UTF-8 (descarga vía navegador)
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        lector = csv.reader(f)
        filas = list(lector)
    encabezado = filas[0]
    # La primera columna del CSV exportado desde el DOM viene vacia (celda de seleccion)
    datos = [fila[1:] for fila in filas[1:] if len(fila) > 1]
    return pd.DataFrame(datos, columns=COLUMNAS)


def leer_html_incrustado(ruta):
    # Estos archivos son la pagina ASP.NET original (codificada en Windows-1252)
    with open(ruta, encoding="cp1252") as f:
        contenido = f.read()
    parser = TableExtractor()
    parser.feed(contenido)
    filas = [f for f in parser.rows if len(f) == len(COLUMNAS)]
    # Descarta la fila de encabezado si quedo mezclada (CODIGO, DISTRITO, ...)
    filas = [f for f in filas if f[0] != "CODIGO"]
    return pd.DataFrame(filas, columns=COLUMNAS)


def main():
    archivos = sorted(glob.glob(os.path.join(CARPETA, "*_DIVERSIFICADO.csv")))
    piezas = []
    resumen = []
    for ruta in archivos:
        nombre = os.path.basename(ruta)
        if es_html(ruta):
            df = leer_html_incrustado(ruta)
            origen = "HTML incrustado (recuperado)"
        else:
            df = leer_csv_limpio(ruta)
            origen = "CSV limpio"
        df["ARCHIVO_ORIGEN"] = nombre
        piezas.append(df)
        resumen.append((nombre, origen, len(df)))

    crudo = pd.concat(piezas, ignore_index=True)

    print(f"{'Archivo':35s} {'Origen':28s} {'Filas':>8s}")
    total = 0
    for nombre, origen, n in resumen:
        print(f"{nombre:35s} {origen:28s} {n:8d}")
        total += n
    print("-" * 75)
    print(f"{'TOTAL':35s} {'':28s} {total:8d}")

    salida = os.path.join(CARPETA, "establecimientos_diversificado_crudo.csv")
    crudo.to_csv(salida, index=False, encoding="utf-8-sig")
    print(f"\nGuardado: {salida}")
    print(f"Filas totales: {len(crudo)}  |  Columnas: {crudo.shape[1]}")


if __name__ == "__main__":
    main()
