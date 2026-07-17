# Proyecto 1 — Obtención y Limpieza de Datos

**Curso:** CC3084 Data Science (UVG) · Semestre II-2026  
**Fuente:** [Buscador de Establecimientos MINEDUC](http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)  
**Filtro:** Nivel escolar = DIVERSIFICADO

## Fase 1 (este entregable)

- Descripción del set crudo (filas y variables)
- Variables que más limpieza necesitan
- Estrategia de limpieza por variable

Documento principal: [`docs/01_Diagnostico_y_Plan_de_Limpieza.md`](docs/01_Diagnostico_y_Plan_de_Limpieza.md)

## Estructura

| Ruta | Contenido |
|---|---|
| `*_DIVERSIFICADO.csv` | Datos crudos por departamento (23 archivos) |
| `establecimientos_diversificado_crudo.csv` | Crudo consolidado |
| `scripts/01_consolidar_crudo.py` | Une los 23 archivos en el consolidado |
| `scripts/02_diagnostico.py` | Diagnóstico reproducible (tablas y estadísticas) |
| `docs/01_Diagnostico_y_Plan_de_Limpieza.md` | Diagnóstico + plan de limpieza |

## Cómo reproducir el diagnóstico

```bash
python scripts/01_consolidar_crudo.py
python scripts/02_diagnostico.py
```

Requisito: `pandas`.
