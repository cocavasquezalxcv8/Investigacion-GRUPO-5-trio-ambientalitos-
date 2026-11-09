# Entregable 2 — Informe de curaduría

## 

## 1\. Material curado

Dos informes institucionales en PDF: **Inventario Nacional de Bofedales 2023** y **Servicios ecosistémicos de regulación hídrica en la cuenca Piuray (2024)**. De ellos se extrajeron 6 archivos CSV a tablas con página de origen. Ninguna tabla trae registros por parcela: son tablas resumen (superficie por departamento, puntos de validación, cobertura de cuenca y lista de especies).

## 2\. Diagnóstico inicial

Se aplicaron 21 pruebas; **7 generaron alerta**.

|tabla|prueba|descripción|casos|resultado|detalle|
|-|-|-|-:|-|-|
|Bof. T5.1|P1|Departamentos duplicados|0|OK||
|Bof. T5.1|P2|Valores faltantes|0|OK||
|Bof. T5.1|P3|Superficies no positivas|0|OK||
|Bof. T5.1|P4|Ranking no decreciente en superficie|0|OK||
|Bof. T5.1|P5|% nacional recalculado difiere > 0.02 pp (total 910,398.16 ha)|0|OK||
|Bof. T5.1|P6|Suma de % nacional distinta de 100 (±0.05)|0|OK|suma=99.99|
|Bof. T4.8|P1|Total por departamento ≠ bofedal + no bofedal|3|ALERTA|Cusco(52 vs 54);Apurímac(223 vs 221);Arequipa(550 vs 223)|
|Bof. T4.8|P2|Suma de columnas ≠ total general impreso (1537)|0|OK|suma b+nb=1537; suma totales impresos=1864|
|Bof. Cusco|P1|Categoría con superficie mayor al total de Cusco|0|OK||
|Bof. Cusco|P2|% departamental de concesiones recalculado difiere > 0.1|0|OK|recalculado=29.86|
|Piuray C7|P1|Suma de % impreso ≠ 100|0|OK|suma=100|
|Piuray C7|P2|% recalculado difiere > 0.5 del impreso|0|OK|área total=46.40 km2|
|Piuray C7|P3|Vegetación natural (pastizal+ matorral) ≥ 50 % (el texto del informe afirma < 50 %)|0|OK|recalculado=43.5 %|
|Piuray C8|P1|Pares formación-especie duplicados|0|OK||
|Piuray C8|P2|Nombres que no inician con binomio|0|OK||
|Piuray C8|P3|Especies repetidas en varias formaciones (informativo)|12|ALERTA|únicas=23 de 40 filas|
|Piuray C8|P4|Nombres aceptados verificados en WFO/POWO|23|ALERTA|pendiente: verificación manual con fecha de consulta|
|Bof. T5.1|P-VAR|Variables mínimas para carbono ausentes (de 12)|12|ALERTA|dap\_cm,altura\_m,area\_parcela,lat,lon,este,norte,datum,fecha\_campo,profundidad\_turba\_cm,densidad\_aparente,carbono\_organico\_pct|
|Bof. T4.8|P-VAR|Variables mínimas para carbono ausentes (de 12)|12|ALERTA|dap\_cm,altura\_m,area\_parcela,lat,lon,este,norte,datum,fecha\_campo,profundidad\_turba\_cm,densidad\_aparente,carbono\_organico\_pct|
|Piuray C7|P-VAR|Variables mínimas para carbono ausentes (de 12)|12|ALERTA|dap\_cm,altura\_m,area\_parcela,lat,lon,este,norte,datum,fecha\_campo,profundidad\_turba\_cm,densidad\_aparente,carbono\_organico\_pct|
|Piuray C8|P-VAR|Variables mínimas para carbono ausentes (de 12)|12|ALERTA|dap\_cm,altura\_m,area\_parcela,lat,lon,este,norte,datum,fecha\_campo,profundidad\_turba\_cm,densidad\_aparente,carbono\_organico\_pct|

## 3\. Hallazgos

1. **Error verificable en la fuente (Bofedales, Tabla 4.8):** tres totales por departamento no coinciden con la suma de sus componentes (Cusco 52 vs 54; Apurímac 223 vs 221; Arequipa 550 vs 223). Las columnas "bofedal" (910) y "no bofedal" (627) suman exactamente el total general impreso (1537), por lo que el error está en los totales de fila. Se adoptó el total recalculado y se conservó el impreso.
2. **Consistencia interna positiva (Bofedales, Tabla 5.1):** el porcentaje nacional recalculado coincide con el impreso en las 19 filas; la superficie total es 910,398.16 ha.
3. **Redondeo (Piuray, Cuadro 7):** los porcentajes están redondeados a enteros; las diferencias con el recálculo son ≤ 0,5 pp. Vegetación natural (pastizal + matorral) = 43.5 % de 46.4 km², coherente con el texto del informe (< 50 %).
4. **Taxonomía no verificada (Piuray, Cuadro 8):** 23 especies únicas en 40 filas; 12 aparecen en más de una formación.
5. **Ausencia estructural de variables:** ninguna tabla contiene coordenadas, datum, fecha de campo, DAP, altura, profundidad de turba, densidad aparente ni carbono orgánico (prueba P-VAR).



## 4\. Reglas aplicadas

|script|regla|id afectado|acción|justificación|
|-:|-|-|-|-|
|3|C1\_pct\_nacional|Tabla 5.1|verificado, sin cambios|% nacional recalculado coincide con el impreso en las 19 filas (tolerancia 0.02 pp). Suma impresa 99.99 por redondeo.|
|3|C2\_total\_inconsistente|T4.8-Cusco|adoptar total recalculado (original conservado)|Total impreso 52 ≠ 18+36=54. Las columnas bofedal (910) y no bofedal (627) suman el total general impreso (1537), por lo que el error está en el total de la fila y no en los componentes. Confirmar con INAIGEM si es posible.|
|3|C2\_total\_inconsistente|T4.8-Apurímac|adoptar total recalculado (original conservado)|Total impreso 223 ≠ 119+102=221. Las columnas bofedal (910) y no bofedal (627) suman el total general impreso (1537), por lo que el error está en el total de la fila y no en los componentes. Confirmar con INAIGEM si es posible.|
|3|C2\_total\_inconsistente|T4.8-Arequipa|adoptar total recalculado (original conservado)|Total impreso 550 ≠ 125+98=223. Las columnas bofedal (910) y no bofedal (627) suman el total general impreso (1537), por lo que el error está en el total de la fila y no en los componentes. Confirmar con INAIGEM si es posible.|
|3|C3\_categorias\_solapadas|Cusco 5.3/5.6/5.7|marcar flag\_no\_sumar|ANP, comunidades y concesiones se solapan espacialmente; sumarlas generaría doble conteo.|
|3|C4\_redondeo\_pct|Piuray C7|sin cambios; bandera|La fuente redondea porcentajes a enteros; las diferencias con el recálculo son ≤ 0.5 pp.|
|3|C5\_taxonomia|Piuray C8 (23 spp.)|marcar flag\_tax\_pendiente|No se asigna nombre aceptado sin consultar World Flora Online / Plants of the World Online; ver data/external/equivalencias\_taxonomicas.csv.|

Principio: los **errores verificables** se corrigen con justificación y el original se conserva; los **valores inciertos** solo se marcan.



## 5\. Resultado

* Tablas curadas y base integrada (formato largo, con fuente, tabla y página de cada valor).
* Datum: no se transformó nada porque ninguna tabla contiene coordenadas. Bofedales declara WGS84 geográfico solo en sus mapas; Piuray no declara datum.



## 6\. Aptitud de los datos para investigación

|magnitud|estimable\_con\_datos\_publicados|motivo|
|-|-|-|
|Extensión del ecosistema (ha)|SI (departamental)|Bofedales T5.1: Cusco 100 393.01 ha|
|Reserva de carbono del suelo (Mg C/ha)|NO|No hay profundidad, densidad aparente ni %C|
|Reserva de carbono total (Mg C)|NO|Requiere reserva por ha × superficie|
|Cambio de existencias (Mg C/año)|NO|No hay remediciones publicadas|
|Secuestro neto / tasa de captura|NO|Requiere cambio de existencias o flujos|
|Emisiones (inventario GEI)|NO|No hay datos de actividad ni factores de emisión|
|Elegibilidad en estándares (adicionalidad, permanencia)|NO EVALUABLE|No se emiten créditos; fuera del alcance|

**Conclusión.** Los datos son aptos para caracterizar la **extensión** de bofedales en Cusco y la composición de cobertura en una cuenca; **no** son aptos para estimar reservas, cambios de existencias ni secuestro de carbono.



## 7\. Limitaciones

* Extracción desde PDF: requiere verificación manual de filas (ver `docs/05`).
* Los puntos de validación de Cusco son pocos (54, de los cuales 18 son bofedal) frente a 100,393 ha.
* Piuray no incluye la clase "bofedal": describe pastizales de puna.

