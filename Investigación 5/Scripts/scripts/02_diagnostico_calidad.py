"""Diagnóstico inicial. NO modifica datos. Cada prueba devuelve OK o ALERTA con detalle."""
import re, pandas as pd, numpy as np
from config import *
asegurar()
res = []
def add(tabla, prueba, desc, n, detalle=""):
    res.append(dict(tabla=tabla, prueba=prueba, descripcion=desc, n_casos=int(n), detalle=detalle, resultado="OK" if n == 0 else "ALERTA"))

# ---------- Bofedales Tabla 5.1
d = pd.read_csv(INTERIM / "bofedales_tabla_5_1_superficie_departamento.csv")
add("Bof. T5.1", "P1", "Departamentos duplicados", d.departamento.duplicated().sum())
add("Bof. T5.1", "P2", "Valores faltantes", d[["superficie_ha", "pct_nacional"]].isna().sum().sum())
add("Bof. T5.1", "P3", "Superficies no positivas", (d.superficie_ha <= 0).sum())
add("Bof. T5.1", "P4", "Ranking no decreciente en superficie", (d.superficie_ha.diff().dropna() > 0).sum())
tot = d.superficie_ha.sum()
rec = d.superficie_ha / tot * 100
dif = (rec - d.pct_nacional).abs()
add("Bof. T5.1", "P5", f"% nacional recalculado difiere > {TOL_PCT_NACIONAL} pp (total {tot:,.2f} ha)", (dif > TOL_PCT_NACIONAL).sum(),
    ";".join(d.departamento[dif > TOL_PCT_NACIONAL]))
add("Bof. T5.1", "P6", "Suma de % nacional distinta de 100 (±0.05)", int(abs(d.pct_nacional.sum() - 100) > 0.05), f"suma={d.pct_nacional.sum():.2f}")

# ---------- Bofedales Tabla 4.8
v = pd.read_csv(INTERIM / "bofedales_tabla_4_8_puntos_validacion.csv")
bad = v[~v.total_coincide]
add("Bof. T4.8", "P1", "Total por departamento ≠ bofedal + no bofedal", len(bad),
    ";".join(f"{r.departamento}({r.total_impreso} vs {r.total_recalculado})" for r in bad.itertuples()))
add("Bof. T4.8", "P2", "Suma de columnas ≠ total general impreso (1537)", int(v.total_recalculado.sum() != 1537), f"suma b+nb={v.total_recalculado.sum()}; suma totales impresos={v.total_impreso.sum()}")

# ---------- Cusco por categoría
c = pd.read_csv(INTERIM / "bofedales_cusco_superficie_por_categoria.csv")
cus_ha = d.loc[d.departamento == "Cusco", "superficie_ha"].iloc[0]
add("Bof. Cusco", "P1", "Categoría con superficie mayor al total de Cusco", (c.superficie_ha > cus_ha).sum())
m = c[c.tabla == "Tabla 5.7"].iloc[0]
add("Bof. Cusco", "P2", "% departamental de concesiones recalculado difiere > 0.1", int(abs(m.superficie_ha / cus_ha * 100 - m.pct_departamental) > 0.1),
    f"recalculado={m.superficie_ha / cus_ha * 100:.2f}")

# ---------- Piuray Cuadro 7
p = pd.read_csv(INTERIM / "piuray_cuadro_7_cobertura.csv")
add("Piuray C7", "P1", "Suma de % impreso ≠ 100", int(p.porcentaje_impreso.sum() != 100), f"suma={p.porcentaje_impreso.sum()}")
dd = (p.porcentaje_recalculado - p.porcentaje_impreso).abs()
add("Piuray C7", "P2", f"% recalculado difiere > {TOL_PCT_REDONDEO} del impreso", (dd > TOL_PCT_REDONDEO).sum(), f"área total={p.area_km2.sum():.2f} km2")

vn = p.loc[p.cobertura.isin(["Pastizales andinos", "Matorral Andino"]), "area_km2"].sum() / p.area_km2.sum() * 100
add("Piuray C7", "P3", "Vegetación natural (pastizal+matorral) ≥ 50 % (el texto del informe afirma < 50 %)", int(vn >= 50), f"recalculado={vn:.1f} %")

# ---------- Piuray Cuadro 8
e = pd.read_csv(INTERIM / "piuray_cuadro_8_especies_umasbamba.csv")
add("Piuray C8", "P1", "Pares formación-especie duplicados", e.duplicated(["formacion_vegetal", "especie_registrada"]).sum())
patron = re.compile(r"^[A-Z][a-z]+ [a-z\-]+")
add("Piuray C8", "P2", "Nombres que no inician con binomio", (~e.especie_registrada.str.match(patron)).sum())
n_form = e.groupby("especie_registrada").formacion_vegetal.nunique()
add("Piuray C8", "P3", "Especies repetidas en varias formaciones (informativo)", (n_form > 1).sum(), f"únicas={len(n_form)} de {len(e)} filas")
add("Piuray C8", "P4", "Nombres aceptados verificados en WFO/POWO", len(n_form), "pendiente: verificación manual con fecha de consulta")

# ---------- Ausencia estructural de variables clave
requeridas = ["dap_cm", "altura_m", "area_parcela", "lat", "lon", "este", "norte", "datum", "fecha_campo", "profundidad_turba_cm", "densidad_aparente", "carbono_organico_pct"]
for nombre, df in (("Bof. T5.1", d), ("Bof. T4.8", v), ("Piuray C7", p), ("Piuray C8", e)):
    faltan = [r for r in requeridas if r not in df.columns]
    add(nombre, "P-VAR", f"Variables mínimas para carbono ausentes (de {len(requeridas)})", len(faltan), ",".join(faltan))

out = pd.DataFrame(res)
out.to_csv(REPORTS / "diagnostico_calidad.csv", index=False)
print(out[["tabla", "prueba", "n_casos", "resultado", "detalle"]].to_string(index=False))
