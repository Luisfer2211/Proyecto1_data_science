# Proyecto 1 — Obtención y Limpieza de Datos

Establecimientos educativos de Guatemala (nivel **diversificado**), fuente MINEDUC.

**Curso:** CC3084 Data Science · UVG · Semestre II-2026  
**Repo:** https://github.com/Luisfer2211/Proyecto1_data_science

## Entregables principales

| Artefacto | Ubicación |
| :--- | :--- |
| Datos crudos por departamento | `data/raw/` |
| Crudo consolidado | `data/establecimientos_diversificado_crudo.csv` |
| **Datos limpios (CSV final)** | `data/establecimientos_diversificado_limpio.csv` |
| Registro de transformaciones | `data/registro_transformaciones.csv` |
| Diagnóstico + principios | `docs/01_Diagnostico_y_Plan_de_Limpieza.md` |
| **Plan de limpieza (Actividad 4)** | `docs/02_Plan_de_Limpieza.md` |
| **Libro de códigos** | `docs/03_Libro_de_Codigos.md` y `docs/03_Libro_de_Codigos.pdf` |
| Presentación | `Diagnostico-y-Limpieza-de-Datos.pdf` |
| Diagnóstico (código) | `notebooks/01_diagnostico_datos_crudos.ipynb` |
| Limpieza fases 1–3 | `notebooks/02_*.ipynb` … `04_*.ipynb` |

## Requisitos

```bash
pip install -r requirements.txt
playwright install chromium
```

Solo necesitas Playwright/Chromium si vas a **re-descargar** del sitio MINEDUC. Para reproducir diagnóstico/limpieza sobre los CSV ya guardados, basta con `pandas`, `rapidfuzz`, `ipykernel` y Jupyter.

## Reproducir el pipeline

Orden recomendado:

1. *(Opcional)* Descarga cruda: `python scripts/00_descargar_crudo.py`
2. *(Opcional)* Catálogo geo: `python scripts/00b_descargar_catalogo.py`
3. Consolidar crudo: `python scripts/01_consolidar_crudo.py`
4. Diagnóstico script: `python scripts/02_diagnostico.py`  
   o notebook: `notebooks/01_diagnostico_datos_crudos.ipynb`
5. Limpieza: ejecutar en orden  
   - `notebooks/02_limpieza_fase1_identificadores.ipynb`  
   - `notebooks/03_limpieza_fase2_texto_libre.ipynb`  
   - `notebooks/04_limpieza_fase3_telefono_duplicados_final.ipynb`

El notebook 04 genera el CSV limpio, el registro consolidado de transformaciones, las pruebas de validación (Actividad 7) y el informe antes/después (Actividad 8).

## Estructura

```
data/
  raw/                          # 23 CSV + manifiesto
  interim/                      # salidas intermedias por fase
  establecimientos_diversificado_crudo.csv
  establecimientos_diversificado_limpio.csv
  catalogo_departamentos_municipios.csv
  registro_transformaciones.csv
  revision_posibles_duplicados.csv
docs/                           # plan + codebook
notebooks/                      # diagnóstico y limpieza
scripts/                        # descarga, consolidación, utils
```

## Integrantes

Luis Palacios · Hugo Barillas · Jose Lopez
