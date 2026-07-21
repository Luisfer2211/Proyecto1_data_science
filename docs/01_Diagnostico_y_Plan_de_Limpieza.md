# Diagnóstico y contexto del plan de limpieza

**Curso:** CC3084 - Data Science · UVG · Semestre II-2026  
**Proyecto 1:** Obtención y Limpieza de Datos  
**Fuente:** [Buscador de Establecimientos Educativos — MINEDUC](http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)  
**Filtro:** `NIVEL ESCOLAR = DIVERSIFICADO`  
**Fecha de extracción:** 2026-07-18 (ver `data/raw/manifiesto_descarga.csv`)

Este documento resume el diagnóstico (Actividad 3) y los principios que alimentan el plan variable por variable en [`02_Plan_de_Limpieza.md`](02_Plan_de_Limpieza.md). El análisis detallado con tablas generadas por código está en `notebooks/01_diagnostico_datos_crudos.ipynb`.

---

## 1. Obtención de los datos

El sitio del MINEDUC no ofrece API ni descarga masiva: solo permite consultar **un departamento a la vez**. Se automatizaron 23 consultas con Playwright (`scripts/00_descargar_crudo.py`):

| Código | Entidad en el combo del sitio |
| :--- | :--- |
| 00 | CIUDAD CAPITAL |
| 01 | GUATEMALA |
| 02–22 | Resto de departamentos del país |

**Nota metodológica importante:** el catálogo del sitio trata `CIUDAD CAPITAL` (prefijo `00`) como entidad separada de `GUATEMALA` (prefijo `01`), aunque geográficamente correspondan al mismo departamento oficial. En este proyecto se **respetan como categorías distintas**, porque así aparecen en la fuente y el prefijo de `CODIGO` es 100% consistente con esa convención.

Cada descarga se guardó en `data/raw/<COD>_<NOMBRE>_DIVERSIFICADO.csv`. Luego `scripts/01_consolidar_crudo.py` unió todo en `data/establecimientos_diversificado_crudo.csv` y agregó la columna técnica `ARCHIVO_ORIGEN`.

Resultado bruto consolidado: **11,890 filas × 18 columnas** (17 de la fuente + `ARCHIVO_ORIGEN`). Tras quitar 23 filas 100% vacías (artefacto del GridView, una por archivo): **11,867 filas útiles**.

---

## 2. Resumen del diagnóstico (Actividad 3)

| Hallazgo | Magnitud |
| :--- | ---: |
| Registros útiles | 11,867 |
| Variables originales de la fuente | 17 |
| Duplicados exactos | 0 |
| `CODIGO` únicos | 11,867 (100%) |
| Variables con al menos un faltante | 6 |
| Teléfonos vacíos | 946 (7.97%) |
| Directores vacíos / placeholders | ~14.6% |
| Pares (DEPARTAMENTO, MUNICIPIO) fuera de catálogo | 0 |
| Formatos distintos en `DISTRITO` | 3 |
| `TELEFONO` con letras | 9 |
| `TELEFONO` con más de un número en la celda | 184 |
| `TELEFONO` con menos de 8 dígitos | 49 |
| Espacios dobles en `ESTABLECIMIENTO` | 1,392 |
| Filas con comillas/apóstrofes en nombre | 2,959 |
| Pares de nombres similares (exploratorio) | ~1,814 |

Todas las variables llegan como texto (`object`). No hay fechas ni cantidades verdaderas: el problema de tipo es que variables categóricas de dominio cerrado (`SECTOR`, `AREA`, `STATUS`, etc.) están guardadas como texto genérico.

---

## 3. Principios del plan de limpieza

1. **Faltante no recuperable → `NA` explícito.** No se imputan nombres, direcciones ni teléfonos.
2. **Nunca fusionar ni eliminar duplicados automáticamente.** Se marcan y documentan; la guía exige revisión caso por caso.
3. **Respetar categorías reales de la fuente.** `CIUDAD CAPITAL` ≠ error tipográfico de `GUATEMALA`. Las variantes de `SEMIPRESENCIAL` en `PLAN` no se unifican sin evidencia de dominio.
4. **Preservar información original cuando sea posible.** Ejemplo: segundo teléfono → columna derivada `TELEFONO_2`, no se descarta.
5. **Toda transformación queda en el registro** (`data/registro_transformaciones.csv`) y es reproducible desde los notebooks.

El detalle por variable (problema → regla → riesgo) está en [`02_Plan_de_Limpieza.md`](02_Plan_de_Limpieza.md).
