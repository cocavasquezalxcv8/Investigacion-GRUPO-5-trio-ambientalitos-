# Entregable 3 — Matriz FAIR (Wilkinson et al., 2016)

Escala: Cumple = 2, Parcial = 1, No = 0 (15 subprincipios, máximo 30). 

**Estado inicial** = los PDF institucionales tal como se descargaron. 

**Estado final** = este repositorio una vez publicado con release y DOI.



|Principio|Subprincipio|Estado inicial (fuente)|Puntuación|Mejora en este repositorio|Punto final|
|-|-|-|-|-|-|
|**F**|F1 Identificador persistente único|PDF con ISBN (978-612-48999-5-9 y -6-6); sin DOI; sin ID por tabla|1|DOI de Zenodo para el release; `pagina\_pdf` + `tabla` identifican cada dato|2|
||F2 Metadatos ricos|Metadatos editoriales; las tablas no tienen metadatos|1|Diccionario de datos, `CITATION.cff`, README|2|
||F3 Metadatos incluyen el ID del dato|No aplica a las tablas del PDF|0|Los metadatos citan el DOI y los archivos|2|
||F4 Indexado en recurso buscable|Repositorio institucional (no verificado en buscadores)|1|GitHub + Zenodo|2|
|**A**|A1 Recuperable por protocolo estándar|Descarga web (HTTPS) del PDF|2|HTTPS en GitHub/Zenodo|2|
||A1.1 Protocolo abierto y gratuito|Sí|2|Sí|2|
||A1.2 Autenticación si es necesaria|Sin autenticación para descargar|2|Sin autenticación|2|
||A2 Metadatos persisten sin el dato|Sin garantía declarada|0|Zenodo conserva metadatos y hash SHA-256 en `reports/`|2|
|**I**|I1 Lenguaje formal y compartido|Tablas en PDF (no legibles por máquina)|0|CSV UTF-8 con encabezados|2|
||I2 Vocabularios FAIR|Departamentos oficiales; nombres científicos con autoría; datum solo en mapas|1|Nombres de columnas documentados; taxonomía **pendiente** de WFO/POWO; datum no declarado en Piuray|1|
||I3 Referencias cualificadas|Sin enlaces entre tablas|0|`indicadores\_altoandino\_cusco.csv` enlaza cada valor con fuente, tabla y página|1|
|**R**|R1 Atributos precisos y relevantes|Metodología descrita en texto|1|Banderas de calidad y diccionario|2|
||R1.1 Licencia clara|**No declarada** en el texto de los PDF|0|Código MIT y docs CC BY 4.0; los datos extraídos siguen sin licencia explícita de la fuente|1|
||R1.2 Procedencia detallada|Describe 61 documentos y 1537 puntos (Bofedales) y el diseño de parcelas (Piuray)|1|`decisiones\_curaduria.csv`, hash, commits|2|
||R1.3 Estándares de la comunidad|Cita guías del MINAM|1|IPCC, EPSG/WGS84, ISO 8601|1|
||**Total**||**13 / 30**||**26 / 30**|

**Limitación.** FAIR no implica "abierto". Mientras la fuente no declare licencia, la redistribución de las tablas extraídas se limita a datos agregados con cita; confirmar condiciones con INAIGEM.



La evaluación de los 15 subprincipios FAIR (Wilkinson et al., 2016) muestra que los documentos institucionales, tal como se descargaron, cumplían 13 de 30 puntos (43 %). Tras la curaduría y la organización del repositorio, la puntuación esperada es de 26 de 30 (87 %).



Por principio, los resultados fueron los siguientes:



Localizable (F): de 3 a 8 de 8 puntos. Los PDF tienen ISBN, pero no un identificador por tabla; el repositorio incorpora DOI, diccionario de datos y metadatos.

Accesible (A): de 6 a 8 de 8. Los PDF ya se descargaban por web sin autenticación; se agrega la conservación de los metadatos y del hash de cada archivo.

Interoperable (I): de 1 a 4 de 6. Las tablas, que estaban dentro de PDF y no eran legibles por máquina, se convirtieron a CSV con encabezados y se enlazaron con su fuente y página de origen.

Reutilizable (R): de 3 a 6 de 8. Se documentaron la procedencia y las decisiones de curaduría, pero la licencia de uso no está declarada en las fuentes.



La mayor mejora se logró en interoperabilidad y localizabilidad, que dependen del tratamiento de los datos. Persisten tres limitaciones: la licencia depende de la institución fuente (R1.1), los nombres de especies siguen pendientes de verificación en World Flora Online o Plants of the World Online (I2), y el estudio de Piuray no declara el datum.



La puntuación final es esperada y se confirmará una vez publicado el repositorio con su release y su DOI en Zenodo. La escala de puntos (Cumple = 2, Parcial = 1, No = 0) es un instrumento del grupo para mostrar el antes y el después, y no una calificación oficial.



