"""Inventario de archivos con hash SHA-256 (demuestra que los originales no fueron alterados)."""
import hashlib, pandas as pd
from config import *
asegurar()
filas = []
for carpeta in (RAW, INTERIM):
    for p in sorted(carpeta.glob("*")):
        if p.name.startswith(".") or p.suffix.lower() == ".md":
            continue
        n_f = n_c = None
        if p.suffix.lower() == ".csv":
            d = pd.read_csv(p); n_f, n_c = d.shape
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        filas.append(dict(carpeta=carpeta.name, archivo=p.name, bytes=p.stat().st_size, filas=n_f, columnas=n_c, sha256=h))
out = pd.DataFrame(filas)
out.to_csv(REPORTS / "inventario_archivos.csv", index=False)
print(out[["carpeta", "archivo", "filas", "columnas"]].to_string(index=False))
