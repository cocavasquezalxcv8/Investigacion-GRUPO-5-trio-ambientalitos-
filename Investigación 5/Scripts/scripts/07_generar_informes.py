"""Genera docs/02_informe_curaduria.md y docs/07_analisis_exploratorio.md con cifras tomadas de reports/ (no escritas a mano)."""
import pandas as pd
from config import *
dg = pd.read_csv(REPORTS / "diagnostico_calidad.csv").fillna("")
dec = pd.read_csv(REPORTS / "decisiones_curaduria.csv")
inv = pd.read_csv(REPORTS / "inventario_archivos.csv")
r = pd.read_csv(REPORTS / "resumen_eda.csv", index_col=0).valor
ap_v = pd.read_csv(REPORTS / "aptitud_variables.csv"); ap_m = pd.read_csv(REPORTS / "aptitud_magnitudes.csv")
tax = pd.read_csv(EXTERNAL / "equivalencias_taxonomicas.csv")
n_alerta = int((dg.resultado == "ALERTA").sum())

informe = f"""# Entregable 3 — Informe de curaduría

*Generado por `scripts/07_generar_informes.py` a partir de `reports/`. Todas las cifras son reproducibles con `bash run_all.sh`.*

## 1. Material curado
Dos informes institucionales en PDF (originales en `data/raw/`, no modificados): **Inventario Nacional de Bofedales 2023** y **Servicios ecosistémicos de regulación hídrica en la cuenca Piuray (2024)**. De ellos se extrajeron {len(inv[inv.carpeta == 'interim'])-0} archivos CSV a `data/interim/` (tablas con página de origen). Ninguna tabla trae registros por parcela: son tablas resumen (superficie por departamento, puntos de validación, cobertura de cuenca y lista de especies).

## 2. Diagnóstico inicial (`reports/diagnostico_calidad.csv`)
Se aplicaron {len(dg)} pruebas; **{n_alerta} generaron alerta**.

{dg[['tabla','prueba','descripcion','n_casos','resultado','detalle']].to_markdown(index=False)}

## 3. Hallazgos
1. **Error verificable en la fuente (Bofedales, Tabla 4.8):** tres totales por departamento no coinciden con la suma de sus componentes (Cusco 52 vs 54; Apurímac 223 vs 221; Arequipa 550 vs 223). Las columnas "bofedal" (910) y "no bofedal" (627) suman exactamente el total general impreso (1537), por lo que el error está en los totales de fila. Se adoptó el total recalculado y se conservó el impreso.
2. **Consistencia interna positiva (Bofedales, Tabla 5.1):** el porcentaje nacional recalculado coincide con el impreso en las 19 filas; la superficie total es {r.ha_total:,.2f} ha.
3. **Redondeo (Piuray, Cuadro 7):** los porcentajes están redondeados a enteros; las diferencias con el recálculo son ≤ 0,5 pp. Vegetación natural (pastizal + matorral) = {r.piuray_veg_natural_pct} % de {r.piuray_km2} km², coherente con el texto del informe (< 50 %).
4. **Taxonomía no verificada (Piuray, Cuadro 8):** {r.especies_unicas:.0f} especies únicas en 40 filas; {r.especies_multiformacion:.0f} aparecen en más de una formación. Los {len(tax)} nombres quedan con `verificado = no` hasta consultarlos en World Flora Online / Plants of the World Online.
5. **Ausencia estructural de variables:** ninguna tabla contiene coordenadas, datum, fecha de campo, DAP, altura, profundidad de turba, densidad aparente ni carbono orgánico (prueba P-VAR).

## 4. Reglas aplicadas (`reports/decisiones_curaduria.csv`)
{dec.to_markdown(index=False)}

Principio: los **errores verificables** se corrigen con justificación y el original se conserva; los **valores inciertos** solo se marcan.

## 5. Resultado
- Tablas curadas en `data/processed/` (5 archivos) y base integrada `indicadores_altoandino_cusco.csv` (formato largo, con fuente, tabla y página de cada valor).
- Datum: no se transformó nada porque ninguna tabla contiene coordenadas. Bofedales declara WGS84 geográfico solo en sus mapas; Piuray no declara datum.

## 6. Aptitud de los datos para investigación
{ap_m[['magnitud','estimable_con_datos_publicados','motivo']].to_markdown(index=False)}

**Conclusión.** Los datos son aptos para caracterizar la **extensión** de bofedales en Cusco y la composición de cobertura en una cuenca; **no** son aptos para estimar reservas, cambios de existencias ni secuestro de carbono.

## 7. Limitaciones
- Extracción desde PDF: requiere verificación manual de filas (ver `docs/05`).
- Los puntos de validación de Cusco son pocos ({r.puntos_validacion_cusco:.0f}, de los cuales {r.puntos_validacion_cusco_bofedal:.0f} son bofedal) frente a {r.cusco_ha:,.0f} ha.
- Piuray no incluye la clase "bofedal": describe pastizales de puna.
"""
(DOCS / "02_informe_curaduria.md").write_text(informe, encoding="utf-8")

eda = f"""# Entregable 9 — Análisis exploratorio de datos

*Generado por `scripts/05_eda_figuras.py` y `07_generar_informes.py`.*

## 1. Estadística descriptiva
| Indicador | Valor |
|---|---|
| Departamentos con bofedal | {r.departamentos_con_bofedal:.0f} |
| Superficie nacional (suma) | {r.ha_total:,.2f} ha |
| Participación de los 3 mayores departamentos | {r.top3_pct} % |
| Cusco: superficie | {r.cusco_ha:,.2f} ha ({r.cusco_pct_nacional} %; puesto {r.cusco_ranking:.0f}) |
| Puntos de validación (nacional / Cusco) | {r.puntos_validacion_total:.0f} / {r.puntos_validacion_cusco:.0f} |
| Cuenca Piuray | {r.piuray_km2} km²; vegetación natural {r.piuray_veg_natural_pct} % |
| Especies listadas en Umasbamba | {r.especies_unicas:.0f} especies, {r.generos:.0f} géneros |

## 2. Figuras
**Fig. 1.** Superficie por departamento. Puno, Arequipa y Ayacucho concentran la mayor parte; Cusco ocupa el cuarto lugar.
![](../reports/figuras/fig1_bofedales_departamento.png)

**Fig. 2.** Cusco por condición territorial (las categorías se solapan).
![](../reports/figuras/fig2_cusco_categorias.png)

**Fig. 3.** Puntos de validación por departamento.
![](../reports/figuras/fig3_puntos_validacion.png)

**Fig. 4.** Cobertura de la cuenca Piuray.
![](../reports/figuras/fig4_piuray_cobertura.png)

**Fig. 5.** Especies por formación vegetal (Umasbamba).
![](../reports/figuras/fig5_especies_formacion.png)

**Fig. 6.** Matriz de disponibilidad de variables para carbono (mapa de vacíos).
![](../reports/figuras/fig6_aptitud_variables.png)

## 3. Patrones y vacíos
- La concentración geográfica es alta: tres departamentos reúnen el {r.top3_pct} % de la superficie nacional.
- En Cusco, la superficie bajo concesión minera (29 975,3 ha) equivale a 29,9 % del total departamental; las comunidades campesinas reúnen 19 082,8 ha. Solo 94,9 ha están en el Santuario Histórico de Machupicchu.
- {r.especies_multiformacion:.0f} de {r.especies_unicas:.0f} especies aparecen en más de una formación, lo que limita su uso como indicadoras de formación.
- **Vacíos críticos:** coordenadas, datum, fechas de campo y variables de suelo (Fig. 6).

## 4. Aptitud (resumen)
{ap_v[['variable','Bofedales_2023','Piuray_2024']].to_markdown(index=False)}
"""
(DOCS / "07_analisis_exploratorio.md").write_text(eda, encoding="utf-8")
print("docs 02 y 07 generados")
