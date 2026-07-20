import os
import re

import pandas as pd

CARPETA = os.path.join(os.path.dirname(__file__), "..")
RUTA_CRUDO = os.path.join(CARPETA, "data", "establecimientos_diversificado_crudo.csv")

pd.set_option("display.width", 160)
pd.set_option("display.max_colwidth", 60)


def es_vacio(valor):
    if pd.isna(valor):
        return True
    return str(valor).strip() == ""


def main():
    df = pd.read_csv(RUTA_CRUDO, encoding="utf-8-sig", dtype=str, keep_default_na=False)

    print("=" * 70)
    print("1) DIMENSIONES")
    print("=" * 70)
    print(f"Registros (filas): {len(df)}")
    print(f"Variables (columnas): {df.shape[1]}")
    print(f"Columnas: {list(df.columns)}")

    print("\n" + "=" * 70)
    print("2) FILAS COMPLETAMENTE VACIAS (artefacto de extraccion HTML)")
    print("=" * 70)
    cols_dato = [c for c in df.columns if c != "ARCHIVO_ORIGEN"]
    vacias = df[cols_dato].apply(lambda col: col.map(es_vacio)).all(axis=1)
    print(f"Filas totalmente vacias: {vacias.sum()}")

    df_datos = df.loc[~vacias].copy()
    print(f"Filas utiles despues de descartar vacias: {len(df_datos)}")

    print("\n" + "=" * 70)
    print("3) TIPO DE DATO ACTUAL POR VARIABLE (todo llega como texto/object)")
    print("=" * 70)
    print(df_datos.dtypes)

    print("\n" + "=" * 70)
    print("4) VALORES FALTANTES POR VARIABLE (NA + cadena vacia + solo espacios)")
    print("=" * 70)
    filas = []
    n = len(df_datos)
    for col in cols_dato:
        faltantes = df_datos[col].map(es_vacio).sum()
        filas.append((col, faltantes, round(100 * faltantes / n, 2)))
    tabla_na = pd.DataFrame(filas, columns=["variable", "faltantes", "pct_faltante"])
    tabla_na = tabla_na.sort_values("pct_faltante", ascending=False)
    print(tabla_na.to_string(index=False))

    print("\n" + "=" * 70)
    print("5) VALORES UNICOS POR VARIABLE")
    print("=" * 70)
    filas = []
    for col in cols_dato:
        filas.append((col, df_datos[col].nunique()))
    tabla_uniq = pd.DataFrame(filas, columns=["variable", "valores_unicos"])
    print(tabla_uniq.to_string(index=False))

    print("\n" + "=" * 70)
    print("6) DUPLICADOS EXACTOS (todas las columnas de datos iguales)")
    print("=" * 70)
    dup_exactos = df_datos.duplicated(subset=cols_dato, keep=False)
    print(f"Filas involucradas en duplicados exactos: {dup_exactos.sum()}")
    print(f"Grupos de duplicados exactos: {df_datos.loc[dup_exactos, cols_dato].drop_duplicates().shape[0]}")

    print("\n" + "=" * 70)
    print("6b) DUPLICADOS POR CODIGO DE ESTABLECIMIENTO (clave que deberia ser unica)")
    print("=" * 70)
    dup_codigo = df_datos["CODIGO"].duplicated(keep=False) & (df_datos["CODIGO"].str.strip() != "")
    print(f"Filas con CODIGO repetido: {dup_codigo.sum()}")
    print(df_datos.loc[dup_codigo, ["CODIGO", "ESTABLECIMIENTO", "MUNICIPIO", "JORNADA", "PLAN"]].sort_values("CODIGO").head(10).to_string(index=False))

    print("\n" + "=" * 70)
    print("7) CATEGORIAS DE VARIABLES DE DOMINIO CERRADO (¿cuantas versiones distintas de cada categoria?)")
    print("=" * 70)
    for col in ["DEPARTAMENTO", "SECTOR", "AREA", "STATUS", "MODALIDAD", "JORNADA", "PLAN", "NIVEL"]:
        vals = sorted(df_datos[col].unique())
        print(f"\n-- {col} ({len(vals)} valores distintos) --")
        print(vals)

    print("\n" + "=" * 70)
    print("8) FORMATO DE TELEFONO (muestra de inconsistencias)")
    print("=" * 70)
    tel = df_datos["TELEFONO"].str.strip()
    solo_digitos = tel.str.fullmatch(r"\d{8}")
    print(f"Telefonos con formato 'estandar' de 8 digitos: {solo_digitos.sum()} / {len(tel)}")
    con_letras = tel.str.contains(r"[A-Za-z]", regex=True, na=False)
    print(f"Telefonos con letras: {con_letras.sum()}")
    multiples = tel.str.contains(r"[-/,]", regex=True, na=False)
    print(f"Celdas con mas de un telefono (separadores - / ,): {multiples.sum()}")
    cortos = tel.str.replace(r"\D", "", regex=True).str.len().lt(8) & (tel != "")
    print(f"Telefonos con menos de 8 digitos (sin contar vacios): {cortos.sum()}")
    print("Ejemplos:")
    print(tel[(con_letras | multiples | cortos) & (tel != "")].drop_duplicates().head(10).to_string())

    print("\n" + "=" * 70)
    print("9) FORMATO DE CODIGO DE ESTABLECIMIENTO (##-##-####-##)")
    print("=" * 70)
    patron_codigo = re.compile(r"^\d{2}-\d{2}-\d{4}-\d{2}$")
    codigo_ok = df_datos["CODIGO"].map(lambda x: bool(patron_codigo.match(x.strip())))
    print(f"Codigos que cumplen el patron: {codigo_ok.sum()} / {len(df_datos)}")
    print("Ejemplos que NO cumplen:")
    print(df_datos.loc[~codigo_ok, "CODIGO"].drop_duplicates().head(10).to_string(index=False))

    print("\n" + "=" * 70)
    print("10) NORMALIZACION DE TEXTO: espacios, mayus/minus mixtas, caracteres raros")
    print("=" * 70)
    for col in ["ESTABLECIMIENTO", "DIRECCION", "MUNICIPIO", "DEPARTAMENTO", "SUPERVISOR", "DIRECTOR"]:
        s = df_datos[col]
        con_espacio_extremo = s.str.strip() != s
        con_espacio_doble = s.str.contains(r"  ", regex=True, na=False)
        vacio_tras_strip = s.str.strip().eq("") & (s != "")
        print(f"{col:16s} | espacios inicio/fin: {con_espacio_extremo.sum():5d} | espacios dobles: {con_espacio_doble.sum():5d} | '--' u otros placeholders: {(s.str.strip()=='--').sum():4d}")

    print("\n" + "=" * 70)
    print("11) CONSISTENCIA ENTRE VARIABLES: CODIGO vs DEPARTAMENTO/MUNICIPIO/NIVEL")
    print("=" * 70)
    depto_map = {
        "01": "GUATEMALA", "00": "GUATEMALA", "02": "EL PROGRESO", "03": "SACATEPEQUEZ",
        "04": "CHIMALTENANGO", "05": "ESCUINTLA", "06": "SANTA ROSA", "07": "SOLOLA",
        "08": "TOTONICAPAN", "09": "QUETZALTENANGO", "10": "SUCHITEPEQUEZ", "11": "RETALHULEU",
        "12": "SAN MARCOS", "13": "HUEHUETENANGO", "14": "QUICHE", "15": "BAJA VERAPAZ",
        "16": "ALTA VERAPAZ", "17": "PETEN", "18": "IZABAL", "19": "ZACAPA", "20": "CHIQUIMULA",
        "21": "JALAPA", "22": "JUTIAPA",
    }
    prefijo = df_datos["CODIGO"].str.slice(0, 2)
    esperado = prefijo.map(depto_map)
    inconsistente = (esperado.notna()) & (esperado != df_datos["DEPARTAMENTO"].str.strip())
    print(f"Filas donde el prefijo del CODIGO no concuerda con DEPARTAMENTO: {inconsistente.sum()}")
    if inconsistente.sum():
        print(df_datos.loc[inconsistente, ["CODIGO", "DEPARTAMENTO"]].drop_duplicates().head(10).to_string(index=False))

    nivel_distinto = df_datos["NIVEL"].str.strip() != "DIVERSIFICADO"
    print(f"\nFilas donde NIVEL no es DIVERSIFICADO (no deberia haber ninguna): {nivel_distinto.sum()}")


if __name__ == "__main__":
    main()
