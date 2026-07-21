# Libro de Códigos

**Conjunto:** Establecimientos educativos de Guatemala — nivel diversificado  
**Versión del conjunto limpio:** `1.0`  
**Archivo:** `data/establecimientos_diversificado_limpio.csv`  
**Fecha de extracción de la fuente:** 2026-07-18  
**Fecha de generación del conjunto limpio:** 2026-07-19 (salida de `notebooks/04_limpieza_fase3_telefono_duplicados_final.ipynb`)  
**Fuente:** Ministerio de Educación de Guatemala (MINEDUC) — Buscador de Establecimientos Educativos  
**URL:** http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/  
**Filtro de descarga:** `NIVEL ESCOLAR = DIVERSIFICADO` (código de nivel `46` en el sitio)  
**Cobertura geográfica:** 23 entidades del combo del sitio (22 departamentos oficiales + `CIUDAD CAPITAL` como entidad separada de `GUATEMALA`)  
**Registros:** 11,867 filas  
**Variables:** 21 columnas  

Este libro describe metadatos necesarios para analizar el conjunto limpio. Complementa el plan en [`02_Plan_de_Limpieza.md`](02_Plan_de_Limpieza.md) y el registro en `data/registro_transformaciones.csv`.

---

## Metadatos generales del conjunto

| Campo | Valor |
| :--- | :--- |
| Nombre del dataset | `establecimientos_diversificado_limpio` |
| Formato | CSV, encoding `utf-8-sig`, separador coma |
| Unidad de observación | Un registro de autorización/establecimiento en el buscador MINEDUC (identificado por `CODIGO`) |
| Idioma de los valores | Español (mayúsculas, sin tildes en la mayoría de campos de la fuente) |
| Catálogo de referencia geo | `data/catalogo_departamentos_municipios.csv` (extraído del propio sitio) |
| Licencia / uso | Datos públicos gubernamentales; uso académico del curso CC3084 |

---

## Resumen de columnas

| # | Variable | Tipo analítico | Origen | Derivada |
| ---: | :--- | :--- | :--- | :---: |
| 1 | `CODIGO` | texto / ID | Fuente | No |
| 2 | `DISTRITO` | texto | Fuente | No |
| 3 | `DEPARTAMENTO` | categórica | Fuente | No |
| 4 | `MUNICIPIO` | categórica | Fuente | No |
| 5 | `ESTABLECIMIENTO` | texto | Fuente | No |
| 6 | `DIRECCION` | texto | Fuente | No |
| 7 | `TELEFONO` | texto (formato fijo) | Fuente | No |
| 8 | `TELEFONO_2` | texto (formato fijo) | Derivada | **Sí** |
| 9 | `SUPERVISOR` | texto | Fuente | No |
| 10 | `DIRECTOR` | texto | Fuente | No |
| 11 | `NIVEL` | categórica | Fuente | No |
| 12 | `SECTOR` | categórica | Fuente | No |
| 13 | `AREA` | categórica | Fuente | No |
| 14 | `STATUS` | categórica | Fuente | No |
| 15 | `MODALIDAD` | categórica | Fuente | No |
| 16 | `JORNADA` | categórica | Fuente | No |
| 17 | `PLAN` | categórica | Fuente | No |
| 18 | `DEPARTAMENTAL` | categórica / texto controlado | Fuente | No |
| 19 | `POSIBLE_DUPLICADO_GRUPO` | ID de clúster | Derivada | **Sí** |
| 20 | `NOTA_DUPLICADO` | texto de triage | Derivada | **Sí** |
| 21 | `ARCHIVO_ORIGEN` | metadato técnico | Consolidación | No* |

\*No es variable del fenómeno educativo; es metadato de trazabilidad agregado al consolidar los CSV crudos.

---

## Diccionario variable por variable

Para cada variable se documentan: descripción, tipo de dato, dominio permitido, valores posibles (cuando aplica), tratamiento de limpieza, y si es derivada.

---

### 1. CODIGO

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Identificador único del establecimiento en el buscador MINEDUC |
| **Tipo de dato** | Texto (`string`). No convertir a numérico |
| **Dominio permitido** | Patrón `##-##-####-##` (dos dígitos – dos – cuatro – dos). El último bloque `46` corresponde al nivel diversificado en la fuente |
| **Valores posibles** | 11,867 códigos distintos (uno por fila) |
| **Tratamiento** | Sin transformación de contenido; verificación de patrón y unicidad |
| **Derivada** | No |
| **Faltantes** | No admite `NA` en el conjunto limpio |

---

### 2. DISTRITO

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Código o etiqueta de distrito escolar asociado al establecimiento |
| **Tipo de dato** | Texto libre semi-estructurado |
| **Dominio permitido** | Cualquier cadena no vacía tras normalización; o `NA` |
| **Valores posibles** | Múltiples formatos coexisten (ej. `01-01-0026`, `01-102`). No se forzó un único patrón |
| **Tratamiento** | Trim, colapso de espacios, vacíos → `NA` |
| **Derivada** | No |
| **Faltantes** | 532 (~4.5%) |

---

### 3. DEPARTAMENTO

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Entidad geográfica según el combo del sitio MINEDUC |
| **Tipo de dato** | Categórica (`category` en pandas; texto en CSV) |
| **Dominio permitido** | Valores del catálogo del sitio (23 entidades) |
| **Valores posibles** | `ALTA VERAPAZ`, `BAJA VERAPAZ`, `CHIMALTENANGO`, `CHIQUIMULA`, `CIUDAD CAPITAL`, `EL PROGRESO`, `ESCUINTLA`, `GUATEMALA`, `HUEHUETENANGO`, `IZABAL`, `JALAPA`, `JUTIAPA`, `PETEN`, `QUETZALTENANGO`, `QUICHE`, `RETALHULEU`, `SACATEPEQUEZ`, `SAN MARCOS`, `SANTA ROSA`, `SOLOLA`, `SUCHITEPEQUEZ`, `TOTONICAPAN`, `ZACAPA` |
| **Tratamiento** | Trim + mayúsculas; validación contra catálogo. Se mantienen `CIUDAD CAPITAL` y `GUATEMALA` separados |
| **Derivada** | No |
| **Faltantes** | 0 |

---

### 4. MUNICIPIO

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Municipio (o zona capitalina) del establecimiento |
| **Tipo de dato** | Categórica / texto controlado |
| **Dominio permitido** | Par `(DEPARTAMENTO, MUNICIPIO)` debe existir en `data/catalogo_departamentos_municipios.csv` |
| **Valores posibles** | 352 valores distintos en el limpio (incluye zonas de Ciudad Capital, ej. `ZONA 1` …) |
| **Tratamiento** | Trim + mayúsculas; validación del par completo |
| **Derivada** | No |
| **Faltantes** | 0 |

---

### 5. ESTABLECIMIENTO

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Nombre del establecimiento educativo |
| **Tipo de dato** | Texto |
| **Dominio permitido** | Texto no vacío tras limpieza; o `NA` |
| **Valores posibles** | Texto libre (5,778 nombres distintos) |
| **Tratamiento** | Colapso de espacios; remoción de comillas decorativas con regla automática + correcciones manuales documentadas; se preservan apóstrofes ortográficos legítimos |
| **Derivada** | No |
| **Faltantes** | Mínimos (celdas vacías originales) |

---

### 6. DIRECCION

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Dirección física reportada |
| **Tipo de dato** | Texto |
| **Dominio permitido** | Texto libre; o `NA` |
| **Valores posibles** | Texto libre |
| **Tratamiento** | Espacios; mayúsculas; abreviaturas `Z.`→`ZONA`, `AV.`→`AVENIDA`, `CALZ.`→`CALZADA`, `KILOMETRO`/`KM`→`KM.`; placeholders → `NA` |
| **Derivada** | No |
| **Faltantes** | 82 (vacíos + placeholders) |

---

### 7. TELEFONO

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Teléfono principal del establecimiento |
| **Tipo de dato** | Texto con formato fijo |
| **Dominio permitido** | `NNNN-NNNN` (exactamente 8 dígitos) o `NA` |
| **Valores posibles** | Números de 8 dígitos formateados; no se validó operador ni prefijo geográfico más allá de longitud |
| **Tratamiento** | Extracción de dígitos; rechazo de letras / longitudes ≠ 8; formato `NNNN-NNNN` |
| **Derivada** | No |
| **Faltantes** | 1,052 |

---

### 8. TELEFONO_2 *(derivada)*

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Segundo teléfono cuando la celda original de `TELEFONO` contenía más de un número válido |
| **Tipo de dato** | Texto con formato fijo |
| **Dominio permitido** | `NNNN-NNNN` o `NA` |
| **Valores posibles** | Igual que `TELEFONO` |
| **Tratamiento / cálculo** | Se toma el segundo bloque de 8 dígitos válido hallado en la celda cruda de teléfono |
| **Utilidad** | Evita descartar un contacto real que venía concatenado en un solo campo |
| **Derivada** | **Sí** |
| **Faltantes** | Alta (solo se llena cuando existía segundo número; 121 registros afectados en el log de transformación) |

---

### 9. SUPERVISOR

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Nombre del supervisor reportado |
| **Tipo de dato** | Texto |
| **Dominio permitido** | Texto libre o `NA` |
| **Valores posibles** | Texto libre |
| **Tratamiento** | Espacios; vacíos → `NA`; sin imputación |
| **Derivada** | No |
| **Faltantes** | 535 |

---

### 10. DIRECTOR

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Nombre del director reportado |
| **Tipo de dato** | Texto |
| **Dominio permitido** | Texto libre o `NA` |
| **Valores posibles** | Texto libre |
| **Tratamiento** | Espacios; vacíos y placeholders (`--`, `SIN DATO`, `-`, `.`, etc.) → `NA`; sin imputación |
| **Derivada** | No |
| **Faltantes** | ~1,831 (vacíos + placeholders marcados) |

---

### 11. NIVEL

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Nivel educativo del registro |
| **Tipo de dato** | Categórica |
| **Dominio permitido** | Exactamente `DIVERSIFICADO` |
| **Valores posibles** | `DIVERSIFICADO` |
| **Tratamiento** | Normalización defensiva + casteo a category |
| **Derivada** | No |

---

### 12. SECTOR

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Sector institucional |
| **Tipo de dato** | Categórica |
| **Dominio permitido** | Conjunto cerrado |
| **Valores posibles** | `COOPERATIVA`, `MUNICIPAL`, `OFICIAL`, `PRIVADO` |
| **Tratamiento** | Normalización + category |
| **Derivada** | No |

---

### 13. AREA

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Área geográfica de ubicación (urbana/rural) |
| **Tipo de dato** | Categórica |
| **Dominio permitido** | Conjunto cerrado |
| **Valores posibles** | `RURAL`, `SIN ESPECIFICAR`, `URBANA` |
| **Tratamiento** | Normalización + category. `SIN ESPECIFICAR` **no** se convierte a `NA` |
| **Derivada** | No |

---

### 14. STATUS

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Estado operativo / administrativo del establecimiento |
| **Tipo de dato** | Categórica |
| **Dominio permitido** | Conjunto cerrado |
| **Valores posibles** | `ABIERTA`, `CERRADA DEFINITIVAMENTE`, `CERRADA TEMPORALMENTE`, `TEMPORAL NOMBRAMIENTO`, `TEMPORAL TITULOS` |
| **Tratamiento** | Normalización + category |
| **Derivada** | No |

---

### 15. MODALIDAD

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Modalidad lingüística |
| **Tipo de dato** | Categórica |
| **Dominio permitido** | Conjunto cerrado |
| **Valores posibles** | `BILINGUE`, `MONOLINGUE` |
| **Tratamiento** | Normalización + category |
| **Derivada** | No |

---

### 16. JORNADA

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Jornada de atención |
| **Tipo de dato** | Categórica |
| **Dominio permitido** | Conjunto cerrado |
| **Valores posibles** | `DOBLE`, `INTERMEDIA`, `MATUTINA`, `NOCTURNA`, `SIN JORNADA`, `VESPERTINA` |
| **Tratamiento** | Normalización + category. `SIN JORNADA` no se convierte a `NA` |
| **Derivada** | No |

---

### 17. PLAN

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Plan o modalidad de estudio |
| **Tipo de dato** | Categórica |
| **Dominio permitido** | 13 categorías de la fuente (sin unificación) |
| **Valores posibles** | `A DISTANCIA`, `DIARIO(REGULAR)`, `DOMINICAL`, `FIN DE SEMANA`, `INTERCALADO`, `IRREGULAR`, `MIXTO`, `SABATINO`, `SEMIPRESENCIAL`, `SEMIPRESENCIAL (DOS DIAS A LA SEMANA)`, `SEMIPRESENCIAL (FIN DE SEMANA)`, `SEMIPRESENCIAL (UN DIA A LA SEMANA)`, `VIRTUAL A DISTANCIA` |
| **Tratamiento** | Normalización + category; **no** se colapsaron variantes de `SEMIPRESENCIAL` |
| **Derivada** | No |

---

### 18. DEPARTAMENTAL

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Dirección / dependencia departamental reportada por la fuente |
| **Tipo de dato** | Texto controlado (26 valores) |
| **Dominio permitido** | Valores observados tras normalización |
| **Valores posibles** | Incluye, entre otros: `GUATEMALA NORTE`, `GUATEMALA SUR`, `GUATEMALA ORIENTE`, `GUATEMALA OCCIDENTE`, y nombres por departamento (algunos con tilde según la fuente, ej. `PETÉN`, `QUICHÉ`) |
| **Tratamiento** | Trim + mayúsculas + colapso de espacios |
| **Derivada** | No |

---

### 19. POSIBLE_DUPLICADO_GRUPO *(derivada)*

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Identificador de clúster de posibles duplicados parciales por similitud de nombre |
| **Tipo de dato** | Texto / entero como string; `NA` si la fila no pertenece a ningún clúster |
| **Dominio permitido** | Entero de grupo ≥ 1, o vacío/`NA` |
| **Valores posibles** | 745 grupos; 2,947 filas marcadas |
| **Cálculo** | RapidFuzz `token_sort_ratio` ≥ 90 entre nombres dentro del mismo municipio; agrupación en clústeres |
| **Utilidad** | Facilitar revisión humana sin borrar filas |
| **Derivada** | **Sí** |
| **Detalle auxiliar** | `data/revision_posibles_duplicados.csv` |

---

### 20. NOTA_DUPLICADO *(derivada)*

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Nota de triage sobre el tipo de posible duplicado |
| **Tipo de dato** | Texto |
| **Dominio permitido** | Combinaciones de etiquetas de triage; o vacío/`NA` |
| **Valores posibles (etiquetas base)** | |
| | `NO ES DUPLICADO: mismo colegio con jornada/plan distintos (autorización legítima independiente)` |
| | `REVISAR: nombre muy similar, confirmar manualmente` |
| | `REVISAR: posible duplicado verdadero (nombre, dirección, jornada y plan coinciden)` |
| | (pueden concatenarse con ` | ` cuando aplican varias) |
| **Utilidad** | Documentar la decisión analítica sin eliminar registros |
| **Derivada** | **Sí** |

---

### 21. ARCHIVO_ORIGEN *(metadato técnico)*

| Campo | Contenido |
| :--- | :--- |
| **Descripción** | Nombre del CSV crudo por departamento del que proviene la fila |
| **Tipo de dato** | Texto |
| **Dominio permitido** | Uno de los 23 archivos en `data/raw/` |
| **Valores posibles** | Ej. `00_CIUDAD_CAPITAL_DIVERSIFICADO.csv`, `01_GUATEMALA_DIVERSIFICADO.csv`, … |
| **Tratamiento** | Sin cambios |
| **Derivada** | No (metadato de pipeline, no del fenómeno) |
| **Fuente / versión** | Agregado por `scripts/01_consolidar_crudo.py` |

---

## Tratamiento global de valores especiales

| Caso | Tratamiento en el limpio |
| :--- | :--- |
| `NA` / celda vacía / solo espacios | `NA` (celda vacía en CSV) |
| `N/A`, `NULL`, `-`, `.`, `SIN DATO`, `--` | `NA` (donde se aplicó la lista de placeholders) |
| Espacios iniciales/finales / múltiples | Eliminados / colapsados |
| Duplicados exactos | No había; se valida que sigan en 0 |
| Duplicados parciales | Marcados, no eliminados |

---

## Control de versiones del conjunto

| Versión | Fecha | Cambios |
| :--- | :--- | :--- |
| `1.0` | 2026-07-19 | Primera versión limpia reproducible (fases 1–3) |

Cualquier regeneración del CSV debe actualizar este número de versión y la fecha en este libro.

---

## Cómo citar / reproducir

1. Clonar el repositorio.  
2. Instalar dependencias (`requirements.txt`).  
3. Ejecutar notebooks `01`→`04` en orden (o partir de los CSV ya generados en `data/`).  
4. El artefacto analítico principal es `data/establecimientos_diversificado_limpio.csv` descrito por este libro.
