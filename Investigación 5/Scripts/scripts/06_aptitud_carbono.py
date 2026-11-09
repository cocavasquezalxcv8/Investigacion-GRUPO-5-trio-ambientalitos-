"""Diagnóstico de aptitud de los datos para carbono: qué magnitud se puede estimar y cuál no.
Los valores de cada celda salen de la revisión documental de los dos informes (docs/02a y docs/05)."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from config import *
asegurar()

# Disponibilidad de variables en lo PUBLICADO (SI / PARCIAL / NO PUBLICADA / NO)
vars_ = ["Superficie del ecosistema (ha)", "Coordenadas por parcela", "Datum declarado", "Fecha de campo por parcela",
         "DAP y altura (árboles)", "Profundidad de turba", "Densidad aparente", "Carbono orgánico (%)", "Remedición del mismo sitio"]
bof = ["SI", "NO", "PARCIAL", "NO", "NO APLICA", "NO", "NO", "NO", "NO"]
piu = ["NO", "NO", "NO", "NO", "NO APLICA", "NO PUBLICADA", "NO PUBLICADA", "NO PUBLICADA", "NO PUBLICADA"]
nota = ["Bofedales: Tabla 5.1 (19 dptos.). Piuray: solo coberturas, sin clase 'bofedal'",
        "Ninguna tabla trae coordenadas por registro",
        "Bofedales: WGS84 geográfico solo en los mapas. Piuray: no declarado",
        "Solo años de referencia (inventario 2023; cobertura 2021; parcelas 2021 y 2023)",
        "Ecosistema herbáceo/turboso: no aplica biomasa arbórea",
        "Bofedales: la menciona como tema; Piuray: no publica valores",
        "Piuray lista la variable (Cuadros 16 y 19) sin valores",
        "Piuray lista materia orgánica (%) como variable monitoreada, sin valores",
        "Piuray: monitoreo semestral/4 años descrito, datos no publicados"]
A = pd.DataFrame({"variable": vars_, "Bofedales_2023": bof, "Piuray_2024": piu, "observacion": nota})
A.to_csv(REPORTS / "aptitud_variables.csv", index=False, encoding="utf-8")

# Magnitudes
M = pd.DataFrame([
 ("Extensión del ecosistema (ha)", "SI (departamental)", "Bofedales T5.1: Cusco 100 393.01 ha", "Resolución provincial/distrital o geometría (shapefile)"),
 ("Reserva de carbono del suelo (Mg C/ha)", "NO", "No hay profundidad, densidad aparente ni %C", "Perfiles de suelo/turba con esas tres variables, por parcela"),
 ("Reserva de carbono total (Mg C)", "NO", "Requiere reserva por ha × superficie", "Lo anterior + superficie por tipo de bofedal"),
 ("Cambio de existencias (Mg C/año)", "NO", "No hay remediciones publicadas", "≥2 mediciones del mismo sitio con método comparable"),
 ("Secuestro neto / tasa de captura", "NO", "Requiere cambio de existencias o flujos", "Series temporales o cámaras de flujo, línea base"),
 ("Emisiones (inventario GEI)", "NO", "No hay datos de actividad ni factores de emisión", "Datos de actividad de degradación/drenaje y factores"),
 ("Elegibilidad en estándares (adicionalidad, permanencia)", "NO EVALUABLE", "No se emiten créditos; fuera del alcance", "Línea base y proyecto definido"),
], columns=["magnitud", "estimable_con_datos_publicados", "motivo", "dato_necesario"])
M.to_csv(REPORTS / "aptitud_magnitudes.csv", index=False, encoding="utf-8")

# Figura: matriz de disponibilidad
col = {"SI": "#3b7d4f", "PARCIAL": "#e6c65c", "NO PUBLICADA": "#d9822b", "NO": "#c0504d", "NO APLICA": "#d9d9d9"}
fig, ax = plt.subplots(figsize=(7.4, 4.4))
for j, fuente in enumerate(("Bofedales_2023", "Piuray_2024")):
    for i, val in enumerate(A[fuente]):
        ax.add_patch(plt.Rectangle((j, len(A) - 1 - i), 1, 1, color=col[val], ec="white")); ax.text(j + .5, len(A) - 1 - i + .5, val, ha="center", va="center", fontsize=8, color="white" if val in ("SI", "NO") else "black")
ax.set_xlim(0, 2); ax.set_ylim(0, len(A)); ax.set_xticks([.5, 1.5], ["Inventario de\nBofedales 2023", "Piuray\n2024"])
ax.set_yticks([i + .5 for i in range(len(A))], A.variable[::-1]); ax.xaxis.tick_top(); ax.tick_params(length=0)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title("Variables disponibles para estimar carbono (lo publicado)", pad=34, fontsize=10, loc="left", x=-0.45)
plt.tight_layout(); plt.savefig(FIGS / "fig6_aptitud_variables.png", dpi=150); plt.close()
print(M[["magnitud", "estimable_con_datos_publicados"]].to_string(index=False))
