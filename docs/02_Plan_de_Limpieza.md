# Plan de limpieza (Actividad 4)

Para cada variable del conjunto: **problema encontrado**, **regla de corrección y por qué**, **riesgos asociados**.

Elaborado a partir del diagnóstico en `notebooks/01_diagnostico_datos_crudos.ipynb` y de [`01_Diagnostico_y_Plan_de_Limpieza.md`](01_Diagnostico_y_Plan_de_Limpieza.md). La ejecución está en los notebooks `02`–`04`; el registro consolidado en `data/registro_transformaciones.csv`.

---

## Principios transversales (aplican a todas las variables de texto)

| Aspecto | Regla | Riesgo |
| :--- | :--- | :--- |
| Valores faltantes / `NA` | Convertir vacíos y solo-espacios a `NA` explícito | Ninguno si no se imputa |
| Cadenas vacías y espacios | `strip` + colapso de espacios múltiples | Bajo: no cambia semántica |
| Placeholders (`N/A`, `NULL`, `-`, `.`, `SIN DATO`, `--`) | Tratar como faltante → `NA` | Bajo si el placeholder es inequívoco; riesgo de marcar un valor legítimo raro (mitigado con lista corta y revisión) |
| Mayúsculas | Dominio cerrado → mayúsculas defensivas; texto libre → no forzar si ya es consistente | Forzar mayúsculas en nombres propios podría alterar capitalización intencional |
| Tipos | Identificadores como texto; categóricas → `category` | Castear `CODIGO` a número perdería ceros a la izquierda |

---

## Filas completamente vacías (todas las variables)

| | |
| :--- | :--- |
| **Problema** | 23 filas 100% vacías (una por archivo/departamento), artefacto del GridView de la fuente |
| **Regla** | Eliminar solo filas donde **todas** las columnas de dato están vacías |
| **Por qué** | No aportan información y distorsionan conteos de faltantes |
| **Riesgo** | Eliminar una fila con algún dato real si el criterio es demasiado agresivo → se exige vacío en **todas** las columnas de contenido |

---

## CODIGO

| | |
| :--- | :--- |
| **Problema** | Ninguno material: cumple patrón `##-##-####-##`, es único en el 100% de filas útiles |
| **Regla** | Conservar como texto; verificar patrón y unicidad (prueba de calidad) |
| **Por qué** | Es el identificador primario del establecimiento en la fuente |
| **Riesgo** | Convertirlo a numérico destruiría ceros a la izquierda (ej. `03-...`) |

---

## DISTRITO

| | |
| :--- | :--- |
| **Problema** | 532 celdas vacías; conviven al menos 3 formatos (`01-01-0026`, `01-102`, etc.) |
| **Regla** | Trim/colapso de espacios; vacíos → `NA`. **No** forzar un único patrón numérico |
| **Por qué** | No hay catálogo oficial confiable en la extracción para rellenar dígitos faltantes |
| **Riesgo** | Imponer un formato único inventaría códigos falsos; dejar formatos mixtos limita comparaciones exactas por distrito (aceptable: se documenta como texto libre semi-estructurado) |

---

## DEPARTAMENTO

| | |
| :--- | :--- |
| **Problema** | Ninguno de dominio: 100% dentro del catálogo del sitio |
| **Regla** | Trim + mayúsculas defensivo; validar contra `data/catalogo_departamentos_municipios.csv`. Mantener `GUATEMALA` y `CIUDAD CAPITAL` separados |
| **Por qué** | Campo de `<select>`, no texto libre; la separación 00/01 es convención real de la fuente |
| **Riesgo** | Fusionar Capital con Guatemala crearía ~2,161 falsos “errores” de prefijo de `CODIGO` |

---

## MUNICIPIO

| | |
| :--- | :--- |
| **Problema** | Ninguno de dominio: 100% de pares `(DEPARTAMENTO, MUNICIPIO)` existen en el catálogo |
| **Regla** | Trim + mayúsculas; validar el **par** completo contra el catálogo |
| **Por qué** | Mismo argumento que `DEPARTAMENTO` |
| **Riesgo** | Validar solo el nombre del municipio sin departamento podría aceptar homónimos incorrectos |

---

## ESTABLECIMIENTO

| | |
| :--- | :--- |
| **Problema** | 1,392 filas con espacios dobles; 2,959 con comillas/apóstrofes (mezcla de comillas decorativas y apóstrofes ortográficos legítimos, p. ej. k'iche'); 5 vacíos |
| **Regla** | (1) Trim + colapso de espacios. (2) Regla automática para quitar comillas decorativas en borde de palabra/puntuación, preservando apóstrofes interiores. (3) Correcciones manuales documentadas para residuales. (4) No forzar cambio de estilo de mayúsculas si el campo ya es ~100% mayúsculas |
| **Por qué** | Normaliza formato sin inventar nombres; los casos ambiguos se revisan a mano |
| **Riesgo** | Una regla automática agresiva podría borrar un apóstrofe ortográfico → se limita por posición y se documentan excepciones manuales |

---

## DIRECCION

| | |
| :--- | :--- |
| **Problema** | Espacios dobles; abreviaturas inconsistentes (`Z.`/`ZONA`, `AV.`/`AVENIDA`, `CALZ.`/`CALZADA`, `KM`/`KM.`/`KILOMETRO`); 76 vacíos + placeholders (`--`, `.`, etc.) |
| **Regla** | Trim + colapso + mayúsculas consistentes; estandarizar solo las 4 abreviaturas de alta frecuencia hacia la forma dominante en el propio dataset; vacíos/placeholders → `NA` (sin imputar) |
| **Por qué** | Unifica lo que ya es frecuente sin reescribir direcciones enteras a un formato postal rígido |
| **Riesgo** | Estandarizar mal una abreviatura rara; no detectar un placeholder atípico → se usa lista corta de placeholders inequívocos |

---

## TELEFONO (y derivada TELEFONO_2)

| | |
| :--- | :--- |
| **Problema** | 946 vacíos; 9 con letras; 184 con más de un número; formatos sin guion / longitud incorrecta |
| **Regla** | Extraer dígitos; aceptar solo números de **exactamente 8 dígitos**; formatear `NNNN-NNNN`; si hay segundo número válido → `TELEFONO_2`; resto → `NA` |
| **Por qué** | Conserva información real sin inventar dígitos; casos ambiguos van a `NA` de forma conservadora |
| **Riesgo** | Descartar un número válido con formato raro; o guardar un segundo número que en realidad era fax/otro contacto sin etiquetar → mitigado documentando la regla y no fusionando filas |

---

## SUPERVISOR

| | |
| :--- | :--- |
| **Problema** | 535 vacíos; espacios dobles |
| **Regla** | Trim + colapso; vacíos → `NA`; **no imputar** nombres |
| **Por qué** | Nombre propio; inventar valores generaría datos falsos |
| **Riesgo** | Bajo en normalización; alto si se imputara (prohibido en este plan) |

---

## DIRECTOR

| | |
| :--- | :--- |
| **Problema** | Variable con más faltantes (~14.6% vacíos) + placeholders (`--`, `SIN DATO`, `-`, `.`); espacios dobles |
| **Regla** | Igual que `SUPERVISOR`: normalizar espacios; vacíos y placeholders → `NA`; no imputar |
| **Por qué** | Placeholders no son nombres válidos (guía Actividad 5.a.iv) |
| **Riesgo** | Un nombre real que coincida literalmente con un placeholder (extremadamente improbable) |

---

## NIVEL

| | |
| :--- | :--- |
| **Problema** | Ninguno: dominio cerrado = `{DIVERSIFICADO}` (filtro de descarga) |
| **Regla** | Trim + mayúsculas; castear a `category`; verificar dominio exacto |
| **Por qué** | Confirma que la extracción no mezcló otros niveles |
| **Riesgo** | Si apareciera otra categoría, el `assert` detiene el pipeline (deseable) |

---

## SECTOR

| | |
| :--- | :--- |
| **Problema** | Ninguno de inconsistencia tipográfica; dominio cerrado ya limpio |
| **Regla** | Trim + mayúsculas; `category`; dominio esperado: `COOPERATIVA`, `MUNICIPAL`, `OFICIAL`, `PRIVADO` |
| **Por qué** | Tipo apropiado para categórica de dominio cerrado |
| **Riesgo** | Recodificar categorías nuevas sin revisar → se rechazan por assert |

---

## AREA

| | |
| :--- | :--- |
| **Problema** | Incluye `SIN ESPECIFICAR` (categoría real, no placeholder a borrar) |
| **Regla** | Normalizar; `category`; dominio: `RURAL`, `SIN ESPECIFICAR`, `URBANA`. **No** convertir `SIN ESPECIFICAR` a `NA` |
| **Por qué** | La fuente distingue “sin especificar” de celda vacía |
| **Riesgo** | Tratar `SIN ESPECIFICAR` como faltante ocultaría una categoría administrativa real |

---

## STATUS

| | |
| :--- | :--- |
| **Problema** | Ninguno tipográfico; 5 categorías estables |
| **Regla** | Normalizar; `category`; dominio: `ABIERTA`, `CERRADA DEFINITIVAMENTE`, `CERRADA TEMPORALMENTE`, `TEMPORAL NOMBRAMIENTO`, `TEMPORAL TITULOS` |
| **Por qué** | Dominio cerrado de la fuente |
| **Riesgo** | Bajo |

---

## MODALIDAD

| | |
| :--- | :--- |
| **Problema** | Ninguno tipográfico |
| **Regla** | Normalizar; `category`; dominio: `BILINGUE`, `MONOLINGUE` |
| **Por qué** | Dominio cerrado |
| **Riesgo** | Bajo |

---

## JORNADA

| | |
| :--- | :--- |
| **Problema** | Incluye `SIN JORNADA` (categoría real) |
| **Regla** | Normalizar; `category`; dominio: `DOBLE`, `INTERMEDIA`, `MATUTINA`, `NOCTURNA`, `SIN JORNADA`, `VESPERTINA`. No recodificar `SIN JORNADA` → `NA` |
| **Por qué** | Misma lógica que `AREA` / `SIN ESPECIFICAR` |
| **Riesgo** | Confundir “sin jornada” con dato faltante |

---

## PLAN

| | |
| :--- | :--- |
| **Problema** | 13 categorías; varias formas de `SEMIPRESENCIAL` (con/sin detalle de días) que podrían parecer redundantes |
| **Regla** | Normalizar formato; `category`; **no unificar** las variantes de `SEMIPRESENCIAL` |
| **Por qué** | Sin criterio de dominio externo, unificar podría borrar diferencia real de modalidad |
| **Riesgo** | Fragmentación estadística (más categorías); se acepta a cambio de no destruir señal |

---

## DEPARTAMENTAL

| | |
| :--- | :--- |
| **Problema** | 26 valores; poco explorado en diagnóstico; posibles tildes/espacios |
| **Regla** | Trim + mayúsculas + colapso de espacios; vacíos → `NA` |
| **Por qué** | Normalización defensiva estándar |
| **Riesgo** | No hay catálogo externo validado en este proyecto; podrían quedar variantes sutiles no detectadas |

---

## ARCHIVO_ORIGEN (metadato técnico)

| | |
| :--- | :--- |
| **Problema** | No es variable del fenómeno; se agregó en la consolidación |
| **Regla** | Conservar sin cambios para trazabilidad |
| **Por qué** | Auditoría: saber de qué CSV por departamento salió cada fila |
| **Riesgo** | Ninguno si se documenta como metadato (no como atributo educativo) |

---

## Duplicados parciales (afecta filas; columnas derivadas)

| | |
| :--- | :--- |
| **Problema** | No hay duplicados exactos, pero sí nombres muy similares (RapidFuzz `token_sort_ratio` ≥ 90) |
| **Regla** | Agrupar pares similares; agregar `POSIBLE_DUPLICADO_GRUPO` y `NOTA_DUPLICADO` con triage (`NO ES DUPLICADO: ...` vs `REVISAR: ...`). **No eliminar ni fusionar** automáticamente. Detalle en `data/revision_posibles_duplicados.csv` |
| **Por qué** | La guía exige no borrar automático y documentar la decisión; un mismo colegio puede tener varios `CODIGO` legítimos por jornada/plan |
| **Riesgo** | Falsos positivos (nombres parecidos distintos) o falsos negativos (umbral alto) → se mitiga con nota de triage y archivo de revisión |

---

## Variables derivadas previstas

| Variable | Justificación breve |
| :--- | :--- |
| `TELEFONO_2` | Conservar segundo número cuando la celda original traía más de uno |
| `POSIBLE_DUPLICADO_GRUPO` | Identificador de clúster de similitud para revisión |
| `NOTA_DUPLICADO` | Decisión/triage documentada por fila marcada |

Todas deben aparecer en el Libro de Códigos ([`03_Libro_de_Codigos.md`](03_Libro_de_Codigos.md)).

---

## Orden de ejecución planificado

1. **Fase 1** (`notebooks/02_...`): filas vacías + identificadores/categóricas de dominio cerrado  
2. **Fase 2** (`notebooks/03_...`): texto libre (`ESTABLECIMIENTO`, `DIRECCION`, `SUPERVISOR`, `DIRECTOR`)  
3. **Fase 3** (`notebooks/04_...`): teléfono, duplicados parciales, validación, informe, CSV final  

Utilidades compartidas: `scripts/limpieza_utils.py`.
