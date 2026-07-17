# Diagnóstico del estado inicial y Plan de limpieza

**Fuente:** Buscador de Establecimientos Educativos, MINEDUC — http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/
**Filtro aplicado:** Nivel Escolar = `DIVERSIFICADO`, todos los departamentos, todos los municipios, todos los sectores, planes y modalidades.
**Fecha de extracción:** 2026-07-16
**Archivo crudo consolidado:** `establecimientos_diversificado_crudo.csv` (generado por `scripts/01_consolidar_crudo.py`)
**Código del diagnóstico:** `scripts/02_diagnostico.py` (todas las tablas y estadísticas de esta sección se generan con ese script)

---

## 1. Descripción del conjunto de datos

El sitio del MINEDUC no ofrece un botón de descarga masiva: solo permite buscar por **un departamento a la vez** y devuelve el resultado como una tabla HTML en la misma página. Por eso la obtención se hizo en **23 consultas** (una por cada "departamento" que ofrece el combo, ya que el sistema separa **Guatemala** en dos entradas independientes: `GUATEMALA` y `CIUDAD CAPITAL`, con código de departamento `01` y `00` respectivamente — el país tiene oficialmente 22 departamentos, pero el catálogo del MINEDUC usa 23 códigos por esta razón administrativa).

De esas 23 consultas:
- **2** se guardaron ya como CSV limpio (`GUATEMALA`, `ALTA_VERAPAZ`), extraído directamente del DOM del navegador.
- **21** se guardaron como la página HTML completa porque el sitio lanzó un error de cliente al momento de generar el resultado (`Control '...grvHistorial' of type 'GridView' must be placed inside a form tag with runat=server`). La tabla de resultados, sin embargo, quedó embebida dentro del HTML y fue recuperada con un parser hecho a la medida (`scripts/01_consolidar_crudo.py`), sin perder registros.

**Cada fila representa una autorización (código) de un establecimiento educativo** para impartir el nivel Diversificado en una jornada/plan/modalidad específicos. Un mismo colegio puede aparecer varias veces con códigos distintos si tiene más de una jornada o plan autorizados — esto **no es un duplicado**, es una característica real del diseño de la fuente.

### Variables originales (17, tal como las entrega el sitio)

| # | Variable | Descripción |
|---|---|---|
| 1 | CODIGO | Identificador único del establecimiento-autorización, formato `DD-DD-NNNN-NN` |
| 2 | DISTRITO | Código de distrito educativo |
| 3 | DEPARTAMENTO | Departamento donde está ubicado el establecimiento |
| 4 | MUNICIPIO | Municipio donde está ubicado |
| 5 | ESTABLECIMIENTO | Nombre del centro educativo |
| 6 | DIRECCION | Dirección física |
| 7 | TELEFONO | Teléfono(s) de contacto |
| 8 | SUPERVISOR | Nombre del supervisor educativo asignado |
| 9 | DIRECTOR | Nombre del director del establecimiento |
| 10 | NIVEL | Nivel escolar (constante = DIVERSIFICADO, por el filtro aplicado) |
| 11 | SECTOR | OFICIAL / PRIVADO / MUNICIPAL / COOPERATIVA |
| 12 | AREA | URBANA / RURAL / SIN ESPECIFICAR |
| 13 | STATUS | Estado de la autorización (abierta, cerrada, etc.) |
| 14 | MODALIDAD | MONOLINGUE / BILINGUE |
| 15 | JORNADA | Turno (matutina, vespertina, etc.) |
| 16 | PLAN | Plan de estudios (diario, sabatino, a distancia, etc.) |
| 17 | DEPARTAMENTAL | Región/dirección departamental de educación a la que reporta |

Se agregó una **18ª columna técnica, `ARCHIVO_ORIGEN`**, que no viene del sitio: guarda de qué archivo/departamento consultado proviene cada fila, para poder auditar el proceso. No forma parte de las variables del fenómeno y se documentará como tal en el Libro de Códigos.

---

## 2. Diagnóstico del estado inicial (Actividad 3)

Todas las cifras de esta sección se obtuvieron ejecutando `scripts/02_diagnostico.py` sobre el crudo consolidado.

### a. Número de registros y variables

| Métrica | Valor |
|---|---|
| Filas totales extraídas (23 archivos) | **11,890** |
| Filas 100% vacías (artefacto del GridView HTML, una por archivo) | **23** |
| Filas con al menos un dato (registros útiles) | **11,867** |
| Variables originales de la fuente | **17** |
| Variables en el archivo consolidado | **18** (+ `ARCHIVO_ORIGEN`) |

> Las 23 filas vacías se reportan como hallazgo del diagnóstico; **aún no se eliminan** (eso pertenece a la ejecución de la limpieza).

### b. Tipo de dato de cada variable

Al cargar el CSV con `dtype=str`, todas las columnas llegan como texto. El tipo **esperado** para el análisis se anota a la derecha (se corregirá en la limpieza).

| Variable | Tipo actual (crudo) | Tipo esperado |
|---|---|---|
| CODIGO | texto (`str`) | texto categórico / identificador |
| DISTRITO | texto (`str`) | texto (código de distrito) |
| DEPARTAMENTO | texto (`str`) | categórica |
| MUNICIPIO | texto (`str`) | categórica |
| ESTABLECIMIENTO | texto (`str`) | texto |
| DIRECCION | texto (`str`) | texto |
| TELEFONO | texto (`str`) | texto (formato telefónico; no numérico) |
| SUPERVISOR | texto (`str`) | texto |
| DIRECTOR | texto (`str`) | texto |
| NIVEL | texto (`str`) | categórica |
| SECTOR | texto (`str`) | categórica |
| AREA | texto (`str`) | categórica |
| STATUS | texto (`str`) | categórica |
| MODALIDAD | texto (`str`) | categórica |
| JORNADA | texto (`str`) | categórica |
| PLAN | texto (`str`) | categórica |
| DEPARTAMENTAL | texto (`str`) | categórica |
| ARCHIVO_ORIGEN | texto (`str`) | texto técnico (trazabilidad) |

### c. Cantidad y porcentaje de valores faltantes por variable

Definición usada: celda vacía, `NA` o solo espacios. Calculado sobre las **11,867** filas útiles.

| Variable | Faltantes | % faltante |
|---|---:|---:|
| DIRECTOR | 1,732 | 14.60 |
| TELEFONO | 946 | 7.97 |
| SUPERVISOR | 535 | 4.51 |
| DISTRITO | 532 | 4.48 |
| DIRECCION | 76 | 0.64 |
| ESTABLECIMIENTO | 5 | 0.04 |
| CODIGO | 0 | 0.00 |
| DEPARTAMENTO | 0 | 0.00 |
| MUNICIPIO | 0 | 0.00 |
| NIVEL | 0 | 0.00 |
| SECTOR | 0 | 0.00 |
| AREA | 0 | 0.00 |
| STATUS | 0 | 0.00 |
| MODALIDAD | 0 | 0.00 |
| JORNADA | 0 | 0.00 |
| PLAN | 0 | 0.00 |
| DEPARTAMENTAL | 0 | 0.00 |

Además, hay **faltantes disfrazados** que el conteo anterior no marca como vacíos: **41** celdas de `DIRECTOR` con valor `"--"`.

### d. Cantidad de valores únicos por variable

| Variable | Valores únicos |
|---|---:|
| CODIGO | 11,867 |
| DIRECCION | 7,440 |
| TELEFONO | 6,572 |
| ESTABLECIMIENTO | 6,313 |
| DIRECTOR | 5,517 |
| DISTRITO | 1,682 |
| SUPERVISOR | 1,281 |
| MUNICIPIO | 352 |
| DEPARTAMENTAL | 26 |
| DEPARTAMENTO | 23 |
| PLAN | 13 |
| JORNADA | 6 |
| STATUS | 5 |
| SECTOR | 4 |
| AREA | 3 |
| MODALIDAD | 2 |
| NIVEL | 1 |

### e. Cantidad de registros duplicados exactos

| Métrica | Valor |
|---|---|
| Filas involucradas en duplicados exactos (todas las columnas de datos iguales) | **0** |
| Grupos de duplicados exactos | **0** |
| Filas con `CODIGO` repetido | **0** |

### f. Variables con valores fuera de dominio o inconsistentes

| Variable / cruce | Hallazgo (generado por código) |
|---|---|
| `TELEFONO` | 9 registros con letras; 49 con menos de 8 dígitos (fuera del dominio telefónico esperado) |
| `DISTRITO` | 70 valores incompletos fuera de patrón (ej. `01-`, `17-`, `10-`) |
| `DIRECTOR` | 41 valores `"--"` (placeholder, no nombre real) |
| `MUNICIPIO` | 352 valores únicos (más que el catálogo oficial de municipios; posibles variantes o errores) |
| `CODIGO` ↔ `DEPARTAMENTO` | 2,161 filas donde el mapa naive `prefijo→departamento` no coincide: todas corresponden a `CIUDAD CAPITAL` (prefijo `00`), que es convención de la fuente, no error de digitación |
| `NIVEL` | 0 filas distintas de `DIVERSIFICADO` |

### g. Variables con formatos inconsistentes

| Variable | Inconsistencia de formato |
|---|---|
| `TELEFONO` | 10,670 con 8 dígitos; 184 celdas con varios números (`-` `/` `,`); 9 con letras; 49 cortos; 946 vacíos |
| `DISTRITO` | Conviven 3+ formatos: `DD-DDD` (5,039), `DD-DD-DDDD` (6,226), vacío (532), incompletos (70) |
| `ESTABLECIMIENTO` | 2,962 registros con comillas simples/dobles (decorativas vs apóstrofes ortográficos reales) |
| `DIRECCION` | Texto libre; 10 filas con minúsculas sueltas; abreviaturas mixtas (`ZONA`/`Z.`, `KM`/`KILOMETRO`) |
| `DEPARTAMENTAL` | 26 valores; mezcla nombres con y sin tilde (`PETÉN` vs patrones sin tilde en otras columnas) frente a `DEPARTAMENTO` sin tilde en varios casos |
| `CODIGO` | Formato consistente: **11,867 / 11,867** cumplen `##-##-####-##` |

### h. Problemas potenciales de calidad de datos (resumen)

1. **Faltantes reales y disfrazados** concentrados en `DIRECTOR`, `TELEFONO`, `SUPERVISOR`, `DISTRITO`.
2. **Formato telefónico heterogéneo** (múltiples números, letras, longitudes inválidas).
3. **`DISTRITO` con varios patrones** e incompletos.
4. **Texto libre** (`ESTABLECIMIENTO`, `DIRECCION`) con comillas, posibles tipografías y abreviaturas no estandarizadas.
5. **Categorías de `PLAN`** potencialmente solapadas (`SEMIPRESENCIAL` y variantes con detalle de días).
6. **Duplicados parciales potenciales** (mismo colegio con nombre/dirección escritos distinto); no hay duplicados exactos.
7. **Caso especial `CIUDAD CAPITAL` / código `00`** que no debe tratarse como inconsistencia falsa.
8. **Limitación metodológica:** en 21/23 archivos la extracción HTML ya colapsó espacios; estadísticas de espacios dobles sobre el consolidado pueden subestimar el problema de la fuente original.

---

## 3. Plan de limpieza (Actividad 4)

Para **cada variable**: problema encontrado, regla de corrección (y por qué), y riesgos.

### CODIGO

| | |
|---|---|
| **a. Problemas** | Ninguno de formato: 100% cumple `##-##-####-##`. Unicidad verificada (0 repetidos). |
| **b. Regla** | Validar el patrón y la unicidad; opcionalmente derivar `COD_DEPARTAMENTO`, `COD_MUNICIPIO`, `COD_CORRELATIVO`, `COD_NIVEL` **solo si se justifican** para el análisis. Funciona porque el patrón ya es estable en el 100% del crudo. |
| **c. Riesgos** | Crear derivadas sin necesidad añade columnas que hay que mantener en el Libro de Códigos; no alterar el `CODIGO` original. |

### DISTRITO

| | |
|---|---|
| **a. Problemas** | Tres formatos principales + 532 vacíos + 70 incompletos (`01-`, etc.). |
| **b. Regla** | Documentar los formatos; marcar vacíos e incompletos como faltantes (`NA`); **no forzar** un único patrón artificial. Se trata como texto/código tal como lo entrega la fuente, salvo invalidar incompletos. Evita inventar códigos. |
| **c. Riesgos** | Normalizar a un solo patrón puede fabricar códigos falsos si el significado de `DD-DDD` vs `DD-DD-DDDD` difiere por departamento. |

### DEPARTAMENTO

| | |
|---|---|
| **a. Problemas** | 23 valores (incluye `CIUDAD CAPITAL`). Sin faltantes. Consistencia con prefijo de `CODIGO` requiere mapear `00` → `CIUDAD CAPITAL`, no a `GUATEMALA`. |
| **b. Regla** | Validar contra catálogo de departamentos MINEDUC (23 entradas); trim; mayúsculas; documentar `CIUDAD CAPITAL` como valor válido de dominio. |
| **c. Riesgos** | Tratar `CIUDAD CAPITAL` como error generaría 2,161 “correcciones” falsas. |

### MUNICIPIO

| | |
|---|---|
| **a. Problemas** | 352 valores únicos (más que el catálogo oficial); posibles variantes de escritura. |
| **b. Regla** | Cruzar contra catálogo oficial municipio–departamento; listar no coincidentes para revisión manual; unificar solo variantes evidentes (misma entidad, distinta escritura) documentando cada mapeo. |
| **c. Riesgos** | Unificar de más puede mezclar municipios distintos; no eliminar filas por municipio no catalogado sin revisión. |

### ESTABLECIMIENTO

| | |
|---|---|
| **a. Problemas** | 5 vacíos; 2,962 con comillas; posibles tipografías; candidatos a duplicado parcial. |
| **b. Regla** | Trim + colapsar espacios; conservar mayúsculas de la fuente; quitar solo comillas decorativas de alias; **conservar** apóstrofes en nombres mayas (`K'AMOLB'E`); detectar pares similares (`ESTABLECIMIENTO`+`DIRECCION`) con Jaro-Winkler/RapidFuzz **sin fusionar automáticamente**. |
| **c. Riesgos** | Borrar apóstrofes reales destruye ortografía; fusionar por similitud puede unir jornadas/sedes legítimamente distintas. |

### DIRECCION

| | |
|---|---|
| **a. Problemas** | 76 vacíos; texto libre; 10 filas con minúsculas; abreviaturas mixtas; 1 placeholder `"--"`. |
| **b. Regla** | Trim; mayúsculas; estandarizar abreviaturas frecuentes a una forma; marcar vacíos/`"--"` como `NA`; no forzar formato postal estricto. |
| **c. Riesgos** | Sobre-normalizar puede borrar referencias útiles (lotes, “a un costado de…”). |

### TELEFONO

| | |
|---|---|
| **a. Problemas** | 946 vacíos; 184 multi-número; 9 con letras; 49 con &lt;8 dígitos. |
| **b. Regla** | Separar múltiples números (p. ej. `TELEFONO_2`); limpiar no dígitos; formato `NNNN-NNNN` solo si hay 8 dígitos; marcar vacíos, letras no recuperables y cortos como `NA`. No imputar números. |
| **c. Riesgos** | Separar mal puede cortar un número válido; inventar dígitos introduce datos falsos. |

### SUPERVISOR

| | |
|---|---|
| **a. Problemas** | 535 vacíos (4.51%). |
| **b. Regla** | Trim; mayúsculas consistentes; vacíos → `NA`. No imputar nombres. |
| **c. Riesgos** | Imputar o “corregir” nombres sin evidencia altera la fuente. |

### DIRECTOR

| | |
|---|---|
| **a. Problemas** | 1,732 vacíos (14.60%) + 41 `"--"`. |
| **b. Regla** | Tratar `""` y `"--"` como `NA`; trim; mayúsculas. No imputar. |
| **c. Riesgos** | Dejar `"--"` como nombre válido distorsiona análisis de cobertura de dato. |

### NIVEL

| | |
|---|---|
| **a. Problemas** | Ninguno: único valor `DIVERSIFICADO` (filtro de extracción). |
| **b. Regla** | Verificar que no cambie; mantener como categórica constante. |
| **c. Riesgos** | Ninguno relevante si el filtro se mantiene. |

### SECTOR

| | |
|---|---|
| **a. Problemas** | Dominio cerrado limpio: `COOPERATIVA`, `MUNICIPAL`, `OFICIAL`, `PRIVADO`. Sin faltantes ni variantes de escritura. |
| **b. Regla** | Validar pertenencia al dominio; trim. Sin unificación adicional. |
| **c. Riesgos** | Bajo; no inventar categorías nuevas. |

### AREA

| | |
|---|---|
| **a. Problemas** | Dominio: `URBANA`, `RURAL`, `SIN ESPECIFICAR`. Sin faltantes ni variantes. |
| **b. Regla** | Validar dominio; trim. No recodificar `SIN ESPECIFICAR` a `NA` salvo justificación explícita (es categoría de la fuente). |
| **c. Riesgos** | Convertir `SIN ESPECIFICAR` a faltante pierde una categoría intencional del MINEDUC. |

### STATUS

| | |
|---|---|
| **a. Problemas** | 5 categorías coherentes; sin faltantes ni variantes ortográficas detectadas. |
| **b. Regla** | Validar dominio; trim. Sin fusionar estados distintos. |
| **c. Riesgos** | Unificar “cerrada temporalmente/definitivamente” perdería semántica real. |

### MODALIDAD

| | |
|---|---|
| **a. Problemas** | Solo `BILINGUE` / `MONOLINGUE`. Sin faltantes ni variantes. |
| **b. Regla** | Validar dominio; trim. |
| **c. Riesgos** | Bajo. |

### JORNADA

| | |
|---|---|
| **a. Problemas** | 6 valores (`MATUTINA`, `VESPERTINA`, `NOCTURNA`, `DOBLE`, `INTERMEDIA`, `SIN JORNADA`). Sin faltantes. |
| **b. Regla** | Validar dominio; trim. Conservar `SIN JORNADA` como categoría de la fuente (no convertir automáticamente a `NA` sin evidencia). |
| **c. Riesgos** | Tratar `SIN JORNADA` como error puede ser incorrecto si la fuente lo usa a propósito. |

### PLAN

| | |
|---|---|
| **a. Problemas** | 13 categorías; posibles solapes entre `SEMIPRESENCIAL` y variantes con detalle de días/fin de semana. |
| **b. Regla** | Documentar las 13; **mantener separadas** las variantes de semipresencial salvo evidencia de que son el mismo valor mal tipificado; trim. |
| **c. Riesgos** | Unificar pierde información real sobre modalidad/días. |

### DEPARTAMENTAL

| | |
|---|---|
| **a. Problemas** | 26 valores (más que 23 departamentos): Guatemala se parte en NORTE/OCCIDENTE/ORIENTE/SUR; Quiché tiene `QUICHÉ` y `QUICHÉ NORTE`; uso inconsistente de tildes respecto a `DEPARTAMENTO`. |
| **b. Regla** | Normalizar tildes de forma consistente; validar lista oficial de direcciones departamentales MINEDUC; no fusionar regiones distintas de Guatemala/Quiché. |
| **c. Riesgos** | Fusionar “GUATEMALA NORTE” con “GUATEMALA” borraría la partición administrativa real. |

### ARCHIVO_ORIGEN (técnica)

| | |
|---|---|
| **a. Problemas** | No es variable del fenómeno; solo trazabilidad de extracción. |
| **b. Regla** | Conservarla en el crudo y en el pipeline para auditoría; puede omitirse del CSV analítico final si el Libro de Códigos lo declara. |
| **c. Riesgos** | Eliminarla demasiado pronto dificulta reproducir de qué consulta salió cada fila. |

### Riesgos generales (aplican a todo el plan)

- Sobre-normalizar texto libre puede destruir información real.
- Fusionar por similitud de cadenas sin revisión manual puede combinar registros legítimamente distintos.
- Tratar `00` / `CIUDAD CAPITAL` como error genera correcciones falsas.
- La extracción HTML ya colapsó espacios en 21/23 archivos; hay que documentarlo al interpretar “limpieza de espacios”.

---

## 4. Próximos pasos (fuera del alcance de este documento)

Este documento cubre el **diagnóstico** y el **plan de limpieza** (Actividades 3 y 4 de la guía). La ejecución de la limpieza (5), tabla de transformaciones (6), pruebas de validación (7), informe antes/después (8), CSV limpio (9) y Libro de Códigos (10) quedan para los siguientes entregables.
