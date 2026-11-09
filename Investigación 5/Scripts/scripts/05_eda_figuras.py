"""Análisis exploratorio: tablas resumen y figuras (reports/figuras)."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from config import *
asegurar()
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
VERDE, GRIS, NARANJA = "#3b7d4f", "#b8b8b8", "#d9822b"

d = pd.read_csv(PROCESSED / "bofedales_superficie_departamento_curado.csv")
v = pd.read_csv(PROCESSED / "puntos_validacion_curado.csv")
c = pd.read_csv(PROCESSED / "bofedales_cusco_categorias_curado.csv")
p = pd.read_csv(PROCESSED / "piuray_cobertura_curado.csv")
e = pd.read_csv(PROCESSED / "especies_umasbamba_curado.csv")

# Fig 1: superficie por departamento
fig, ax = plt.subplots(figsize=(7, 4.6)); dd = d.sort_values("superficie_ha")
ax.barh(dd.departamento, dd.superficie_ha / 1000, color=[NARANJA if x else VERDE for x in dd.flag_cusco])
ax.set_xlabel("Superficie de bofedales (miles de ha)"); ax.set_title("Bofedales por departamento (Cusco resaltado)")
plt.tight_layout(); plt.savefig(FIGS / "fig1_bofedales_departamento.png", dpi=150); plt.close()

# Fig 2: Cusco por categoría
tot = float(d.loc[d.departamento == "Cusco", "superficie_ha"].iloc[0])
cat = pd.DataFrame({"categoria": ["Total Cusco"] + c.categoria.tolist(), "ha": [tot] + c.superficie_ha.tolist()})
fig, ax = plt.subplots(figsize=(7, 3.2)); ax.barh(cat.categoria[::-1], cat.ha[::-1], color=[GRIS] * 3 + [VERDE])
for y, h in enumerate(cat.ha[::-1]): ax.text(h, y, f" {h:,.1f}", va="center")
ax.set_xlim(0, tot * 1.2); ax.set_xlabel("ha (categorías solapadas: no sumar)"); ax.set_title("Bofedales de Cusco por condición territorial")
plt.tight_layout(); plt.savefig(FIGS / "fig2_cusco_categorias.png", dpi=150); plt.close()

# Fig 3: puntos de validación (cobertura de verdad de campo)
fig, ax = plt.subplots(figsize=(7, 4)); vv = v.sort_values("total_adoptado")
ax.barh(vv.departamento, vv.bofedal, color=VERDE, label="Bofedal"); ax.barh(vv.departamento, vv.no_bofedal, left=vv.bofedal, color=GRIS, label="No bofedal")
ax.set_xlabel("Puntos de validación"); ax.set_title("Puntos de validación por departamento (totales recalculados)"); ax.legend(frameon=False)
plt.tight_layout(); plt.savefig(FIGS / "fig3_puntos_validacion.png", dpi=150); plt.close()

# Fig 4: cobertura Piuray
fig, ax = plt.subplots(figsize=(7, 3.4)); pp = p.sort_values("area_km2")
ax.barh(pp.cobertura, pp.area_km2, color=VERDE); ax.set_xlabel("Área (km²)"); ax.set_title(f"Cobertura de la cuenca Piuray (total {p.area_km2.sum():.2f} km²)")
plt.tight_layout(); plt.savefig(FIGS / "fig4_piuray_cobertura.png", dpi=150); plt.close()

# Fig 5: presencia de especies por formación
m = e.assign(v=1).pivot_table(index="especie_registrada", columns="formacion_vegetal", values="v", fill_value=0)
m = m.loc[m.sum(axis=1).sort_values(ascending=False).index]
fig, ax = plt.subplots(figsize=(7.5, 7)); ax.imshow(m.values, cmap="Greens", aspect="auto", vmin=0, vmax=1.3)
ax.set_xticks(range(m.shape[1]), m.columns, rotation=30, ha="right"); ax.set_yticks(range(m.shape[0]), [" ".join(s.split()[:2]) for s in m.index], fontsize=7)
ax.set_title("Especies más abundantes por formación (Umasbamba)"); plt.tight_layout(); plt.savefig(FIGS / "fig5_especies_formacion.png", dpi=150); plt.close()

# Tablas resumen
res = {"departamentos_con_bofedal": len(d), "ha_total": round(d.superficie_ha.sum(), 2),
       "top3_pct": round(d.nlargest(3, "superficie_ha").pct_nacional.sum(), 2), "cusco_ha": tot,
       "cusco_ranking": int(d.loc[d.flag_cusco, "ranking_nacional"].iloc[0]),
       "cusco_pct_nacional": float(d.loc[d.flag_cusco, "pct_nacional"].iloc[0]),
       "piuray_km2": round(p.area_km2.sum(), 2),
       "piuray_veg_natural_pct": round(p.loc[p.flag_vegetacion_natural, "area_km2"].sum() / p.area_km2.sum() * 100, 1),
       "especies_unicas": e.especie_registrada.nunique(), "generos": e.genero.nunique(),
       "especies_multiformacion": int((e.groupby("especie_registrada").formacion_vegetal.nunique() > 1).sum()),
       "puntos_validacion_total": int(v.total_adoptado.sum()), "puntos_validacion_cusco": int(v.loc[v.departamento == "Cusco", "total_adoptado"].iloc[0]),
       "puntos_validacion_cusco_bofedal": int(v.loc[v.departamento == "Cusco", "bofedal"].iloc[0])}
pd.Series(res).to_csv(REPORTS / "resumen_eda.csv", header=["valor"], index_label="indicador")
print(pd.Series(res).to_string())
