"""Curaduría. Regla de oro:
  ERROR VERIFICABLE -> se corrige o excluye con justificación (el original se conserva en data/interim).
  VALOR INUSUAL/INCIERTO -> solo se marca con bandera; no se modifica.
Salida: data/processed/*.csv y reports/decisiones_curaduria.csv"""
import re, pandas as pd, numpy as np
from config import *
asegurar()
(REPORTS / "decisiones_curaduria.csv").unlink(missing_ok=True)

# --- 1. Bofedales por departamento (T5.1)
d = pd.read_csv(INTERIM / "bofedales_tabla_5_1_superficie_departamento.csv")
tot = d.superficie_ha.sum()
d["pct_nacional_recalculado"] = (d.superficie_ha / tot * 100).round(2)
d["flag_pct_difiere"] = (d.pct_nacional_recalculado - d.pct_nacional).abs() > TOL_PCT_NACIONAL
d["flag_cusco"] = d.departamento.eq("Cusco")
d.to_csv(PROCESSED / "bofedales_superficie_departamento_curado.csv", index=False, encoding="utf-8")
log_decision("03", "C1_pct_nacional", "Tabla 5.1", "verificado, sin cambios",
             f"% nacional recalculado coincide con el impreso en las 19 filas (tolerancia {TOL_PCT_NACIONAL} pp). Suma impresa 99.99 por redondeo.")

# --- 2. Puntos de validación (T4.8): error verificable en 3 totales
v = pd.read_csv(INTERIM / "bofedales_tabla_4_8_puntos_validacion.csv")
v["flag_total_impreso_inconsistente"] = ~v.total_coincide
v["total_adoptado"] = v.total_recalculado
for r in v[v.flag_total_impreso_inconsistente].itertuples():
    log_decision("03", "C2_total_inconsistente", f"T4.8-{r.departamento}", "adoptar total recalculado (original conservado)",
        f"Total impreso {r.total_impreso} ≠ {r.bofedal}+{r.no_bofedal}={r.total_recalculado}. Las columnas bofedal (910) y no bofedal (627) suman el total general impreso (1537), "
        "por lo que el error está en el total de la fila y no en los componentes. Confirmar con INAIGEM si es posible.")
v.drop(columns=["total_coincide"]).to_csv(PROCESSED / "puntos_validacion_curado.csv", index=False, encoding="utf-8")

# --- 3. Cusco por categoría (categorías que se solapan: no se suman)
c = pd.read_csv(INTERIM / "bofedales_cusco_superficie_por_categoria.csv")
cus_ha = float(d.loc[d.departamento == "Cusco", "superficie_ha"].iloc[0])
c["pct_del_total_cusco_recalculado"] = (c.superficie_ha / cus_ha * 100).round(2)
c["flag_no_sumar"] = True
c.to_csv(PROCESSED / "bofedales_cusco_categorias_curado.csv", index=False, encoding="utf-8")
log_decision("03", "C3_categorias_solapadas", "Cusco 5.3/5.6/5.7", "marcar flag_no_sumar",
             "ANP, comunidades y concesiones se solapan espacialmente; sumarlas generaría doble conteo.")

# --- 4. Piuray cobertura (C7)
p = pd.read_csv(INTERIM / "piuray_cuadro_7_cobertura.csv")
p["flag_redondeo"] = (p.porcentaje_recalculado - p.porcentaje_impreso).abs().between(0.25, TOL_PCT_REDONDEO)
p["flag_vegetacion_natural"] = p.cobertura.isin(["Pastizales andinos", "Matorral Andino"])   # coherente con el texto del informe: vegetación natural < 50 % de la cuenca
p.to_csv(PROCESSED / "piuray_cobertura_curado.csv", index=False, encoding="utf-8")
log_decision("03", "C4_redondeo_pct", "Piuray C7", "sin cambios; bandera",
             "La fuente redondea porcentajes a enteros; las diferencias con el recálculo son ≤ 0.5 pp.")

# --- 5. Piuray especies (C8): parseo de nombre, sin decidir taxonomía
e = pd.read_csv(INTERIM / "piuray_cuadro_8_especies_umasbamba.csv")
def parse(n):
    m = re.match(r"^([A-Z][a-z]+) ([a-z\-]+)\s*(.*)$", n)
    return (m.group(1), m.group(2), m.group(3)) if m else (None, None, None)
e[["genero", "epiteto", "autoria"]] = e.especie_registrada.apply(lambda s: pd.Series(parse(s)))
e["n_formaciones"] = e.groupby("especie_registrada").formacion_vegetal.transform("nunique")
e["flag_tax_pendiente"] = True
e.to_csv(PROCESSED / "especies_umasbamba_curado.csv", index=False, encoding="utf-8")
log_decision("03", "C5_taxonomia", "Piuray C8 (23 spp.)", "marcar flag_tax_pendiente",
             "No se asigna nombre aceptado sin consultar World Flora Online / Plants of the World Online; ver data/external/equivalencias_taxonomicas.csv.")

# --- 6. Base integrada en formato largo (indicadores)
filas = []
def ind(fuente, tabla, pg, ambito, indicador, valor, unidad, ref):
    filas.append(dict(fuente=fuente, tabla=tabla, pagina_pdf=pg, ambito=ambito, indicador=indicador, valor=valor, unidad=unidad, referencia_temporal=ref))
B, P = "Inventario Nacional de Bofedales 2023", "Piuray 2024"
cu = d[d.departamento == "Cusco"].iloc[0]
ind(B, "T5.1", 99, "Cusco", "Superficie de bofedales", cu.superficie_ha, "ha", "inventario 2023")
ind(B, "T5.1", 99, "Cusco", "Participación en el total nacional", cu.pct_nacional, "%", "inventario 2023")
ind(B, "T5.1", 99, "Cusco", "Ranking nacional por superficie", cu.ranking_nacional, "posición", "inventario 2023")
ind(B, "T5.1", 99, "Perú", "Superficie total (suma de 19 departamentos)", round(tot, 2), "ha", "inventario 2023")
for r in c.itertuples():
    ind(B, r.tabla.replace("Tabla ", "T"), r.pagina_pdf, "Cusco", f"Bofedales en {r.categoria}", r.superficie_ha, "ha", "inventario 2023")
vc = v[v.departamento == "Cusco"].iloc[0]
ind(B, "T4.8", 93, "Cusco", "Puntos de validación en bofedal", vc.bofedal, "puntos", "inventario 2023")
ind(B, "T4.8", 93, "Cusco", "Puntos de validación total (recalculado)", vc.total_adoptado, "puntos", "inventario 2023")
for r in p.itertuples():
    ind(P, "Cuadro 7", 16, "Cuenca Piuray", f"Cobertura: {r.cobertura}", r.area_km2, "km2", "cobertura al 2021 (según Figura 10 del informe)")
ind(P, "Cuadro 8", 16, "Quebrada Umasbamba", "Especies listadas como más abundantes", e.especie_registrada.nunique(), "especies", "no declarado")
pd.DataFrame(filas).to_csv(PROCESSED / "indicadores_altoandino_cusco.csv", index=False, encoding="utf-8")
print(len(filas), "indicadores integrados")
print(pd.read_csv(REPORTS / "decisiones_curaduria.csv")[["regla", "id_afectado", "accion"]].to_string(index=False))
