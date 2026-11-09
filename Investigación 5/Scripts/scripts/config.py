"""Configuración común. Rutas relativas a la raíz del repositorio."""
import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RAW, INTERIM, PROCESSED, EXTERNAL = (RAIZ / "data" / d for d in ("raw", "interim", "processed", "external"))
REPORTS, FIGS, DOCS = RAIZ / "reports", RAIZ / "reports" / "figuras", RAIZ / "docs"
TOL_PCT_NACIONAL = 0.02   # tolerancia (puntos porcentuales) al recalcular % nacional (redondeo a 2 decimales)
TOL_PCT_REDONDEO = 0.5    # tolerancia al recalcular % de cobertura (la fuente redondea a enteros)

def asegurar():
    for d in (PROCESSED, REPORTS, FIGS):
        d.mkdir(parents=True, exist_ok=True)

def log_decision(script, regla, afectado, accion, justificacion):
    """Registro auditable de cada decisión de curaduría."""
    asegurar()
    ruta = REPORTS / "decisiones_curaduria.csv"
    nuevo = not ruta.exists()
    with open(ruta, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["script", "regla", "id_afectado", "accion", "justificacion"])
        w.writerow([script, regla, afectado, accion, justificacion])
