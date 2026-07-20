import csv
import os

from playwright.sync_api import sync_playwright

URL = "http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/"
ID_CMB_DEPARTAMENTO = "_ctl0_ContentPlaceHolder1_cmbDepartamento"
ID_CMB_MUNICIPIO = "_ctl0_ContentPlaceHolder1_cmbMunicipio"

DEPARTAMENTOS = [
    ("16", "ALTA VERAPAZ"), ("15", "BAJA VERAPAZ"), ("04", "CHIMALTENANGO"),
    ("20", "CHIQUIMULA"), ("00", "CIUDAD CAPITAL"), ("02", "EL PROGRESO"),
    ("05", "ESCUINTLA"), ("01", "GUATEMALA"), ("13", "HUEHUETENANGO"),
    ("18", "IZABAL"), ("21", "JALAPA"), ("22", "JUTIAPA"), ("17", "PETEN"),
    ("09", "QUETZALTENANGO"), ("14", "QUICHE"), ("11", "RETALHULEU"),
    ("03", "SACATEPEQUEZ"), ("12", "SAN MARCOS"), ("06", "SANTA ROSA"),
    ("07", "SOLOLA"), ("10", "SUCHITEPEQUEZ"), ("08", "TOTONICAPAN"),
    ("19", "ZACAPA"),
]

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_RAIZ = os.path.join(CARPETA_SCRIPT, "..")
SALIDA = os.path.join(CARPETA_RAIZ, "data", "catalogo_departamentos_municipios.csv")


def main():
    filas = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(60000)

        for cod_depto, nombre_depto in DEPARTAMENTOS:
            print(f"{cod_depto} {nombre_depto} ...")
            page.goto(URL, wait_until="networkidle")
            with page.expect_navigation(wait_until="networkidle"):
                page.select_option(f"#{ID_CMB_DEPARTAMENTO}", cod_depto)
            opciones = page.eval_on_selector_all(
                f"#{ID_CMB_MUNICIPIO} option",
                "els => els.map(e => [e.value, e.textContent.trim()])",
            )
            for cod_mun, nombre_mun in opciones:
                if cod_mun == "" or nombre_mun.upper() == "TODOS":
                    continue
                filas.append((cod_depto, nombre_depto, cod_mun, nombre_mun))
            print(f"  {len(opciones) - 1} municipios")

        browser.close()

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["COD_DEPARTAMENTO", "DEPARTAMENTO", "COD_MUNICIPIO", "MUNICIPIO"])
        w.writerows(filas)

    print(f"\nGuardado: {SALIDA}  ({len(filas)} municipios en {len(DEPARTAMENTOS)} departamentos)")


if __name__ == "__main__":
    main()
