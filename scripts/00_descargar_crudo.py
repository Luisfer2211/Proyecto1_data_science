import argparse
import csv
import datetime as dt
import os
import sys
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

URL = "http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/"
NIVEL_DIVERSIFICADO = "46"

ID_CMB_DEPARTAMENTO = "_ctl0_ContentPlaceHolder1_cmbDepartamento"
ID_CMB_NIVEL = "_ctl0_ContentPlaceHolder1_cmbNivel"
ID_BTN_CONSULTAR = "_ctl0_ContentPlaceHolder1_IbtnConsultar"
ID_TABLA_RESULTADO = "_ctl0_ContentPlaceHolder1_dgResultado"

COLUMNAS = [
    "CODIGO", "DISTRITO", "DEPARTAMENTO", "MUNICIPIO", "ESTABLECIMIENTO",
    "DIRECCION", "TELEFONO", "SUPERVISOR", "DIRECTOR", "NIVEL", "SECTOR",
    "AREA", "STATUS", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL",
]

# Los 23 "departamentos" que ofrece el combo del sitio (Guatemala aparece
# separado en GUATEMALA=01 y CIUDAD CAPITAL=00; el pais tiene 22
# departamentos oficiales, ver docs/01_Diagnostico_y_Plan_de_Limpieza.md).
DEPARTAMENTOS = [
    ("16", "ALTA_VERAPAZ"),
    ("15", "BAJA_VERAPAZ"),
    ("04", "CHIMALTENANGO"),
    ("20", "CHIQUIMULA"),
    ("00", "CIUDAD_CAPITAL"),
    ("02", "EL_PROGRESO"),
    ("05", "ESCUINTLA"),
    ("01", "GUATEMALA"),
    ("13", "HUEHUETENANGO"),
    ("18", "IZABAL"),
    ("21", "JALAPA"),
    ("22", "JUTIAPA"),
    ("17", "PETEN"),
    ("09", "QUETZALTENANGO"),
    ("14", "QUICHE"),
    ("11", "RETALHULEU"),
    ("03", "SACATEPEQUEZ"),
    ("12", "SAN_MARCOS"),
    ("06", "SANTA_ROSA"),
    ("07", "SOLOLA"),
    ("10", "SUCHITEPEQUEZ"),
    ("08", "TOTONICAPAN"),
    ("19", "ZACAPA"),
]

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_RAIZ = os.path.join(CARPETA_SCRIPT, "..")
CARPETA_RAW = os.path.join(CARPETA_RAIZ, "data", "raw")


def extraer_tabla(html_bytes):
    html = html_bytes.decode("utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    tabla = soup.find(id=ID_TABLA_RESULTADO)
    if tabla is None:
        return None

    filas = []
    for tr in tabla.find_all("tr"):
        celdas = [td.get_text(strip=True) for td in tr.find_all("td")]
        if not celdas:
            continue
        # La primera celda es el icono/enlace de "seleccionar establecimiento"
        celdas = celdas[1:]
        if celdas == COLUMNAS:
            continue  # fila de encabezado
        if len(celdas) != len(COLUMNAS):
            continue  # fila decorativa/ajena a los datos
        filas.append(celdas)
    return filas


def descargar_departamento(page, codigo, nombre, reintentos, espera):
    for intento in range(1, reintentos + 1):
        try:
            page.goto(URL, wait_until="networkidle", timeout=60000)
            with page.expect_navigation(wait_until="networkidle", timeout=60000):
                page.select_option(f"#{ID_CMB_DEPARTAMENTO}", codigo)
            page.select_option(f"#{ID_CMB_NIVEL}", NIVEL_DIVERSIFICADO)
            with page.expect_navigation(wait_until="networkidle", timeout=60000) as nav_info:
                page.click(f"#{ID_BTN_CONSULTAR}")
            respuesta = nav_info.value
            cuerpo = respuesta.body()
            filas = extraer_tabla(cuerpo)
            if filas is None:
                raise RuntimeError("no se encontro la tabla de resultados en la respuesta")
            return filas
        except (PWTimeout, RuntimeError) as e:
            print(f"  [intento {intento}/{reintentos}] {nombre}: {e}", file=sys.stderr)
            if intento == reintentos:
                raise
            time.sleep(espera * intento)  # backoff simple
    return []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo", help="Codigos de departamento separados por coma, para probar con pocos (ej. 03,00)")
    ap.add_argument("--reintentos", type=int, default=4, help="Reintentos por departamento si falla (default 4)")
    ap.add_argument("--espera", type=float, default=2.5, help="Segundos de espera entre departamentos (default 2.5)")
    ap.add_argument("--headless", action="store_true", default=True)
    args = ap.parse_args()

    deptos = DEPARTAMENTOS
    if args.solo:
        codigos = {c.strip() for c in args.solo.split(",")}
        deptos = [d for d in DEPARTAMENTOS if d[0] in codigos]
        if not deptos:
            sys.exit(f"Ningun codigo de --solo coincide con la lista conocida: {args.solo}")

    os.makedirs(CARPETA_RAW, exist_ok=True)
    fecha_extraccion = dt.date.today().isoformat()

    manifiesto = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        page = browser.new_page()
        page.set_default_timeout(60000)

        for i, (codigo, nombre) in enumerate(deptos):
            print(f"[{i + 1}/{len(deptos)}] {nombre} (cod {codigo}) ...")
            try:
                filas = descargar_departamento(page, codigo, nombre, args.reintentos, args.espera)
            except Exception as e:
                print(f"  FALLO DEFINITIVO: {nombre}: {e}", file=sys.stderr)
                manifiesto.append((codigo, nombre, "ERROR", 0, str(e), fecha_extraccion))
                continue

            ruta_salida = os.path.join(CARPETA_RAW, f"{codigo}_{nombre}_DIVERSIFICADO.csv")
            with open(ruta_salida, "w", newline="", encoding="utf-8-sig") as f:
                escritor = csv.writer(f)
                escritor.writerow(COLUMNAS)
                escritor.writerows(filas)

            print(f"  OK: {len(filas)} filas -> {os.path.relpath(ruta_salida, CARPETA_RAIZ)}")
            manifiesto.append((codigo, nombre, "OK", len(filas), "", fecha_extraccion))

            if i < len(deptos) - 1:
                time.sleep(args.espera)

        browser.close()

    ruta_manifiesto = os.path.join(CARPETA_RAW, "manifiesto_descarga.csv")
    with open(ruta_manifiesto, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f)
        escritor.writerow(["CODIGO", "DEPARTAMENTO", "ESTADO", "FILAS", "ERROR", "FECHA_EXTRACCION"])
        escritor.writerows(manifiesto)

    total = sum(m[3] for m in manifiesto)
    fallidos = [m for m in manifiesto if m[2] != "OK"]
    print("\n" + "=" * 60)
    print(f"Total de filas descargadas: {total}")
    print(f"Departamentos con error: {len(fallidos)}")
    for m in fallidos:
        print(f"  - {m[1]} ({m[0]}): {m[4]}")
    print(f"Manifiesto: {os.path.relpath(ruta_manifiesto, CARPETA_RAIZ)}")


if __name__ == "__main__":
    main()
