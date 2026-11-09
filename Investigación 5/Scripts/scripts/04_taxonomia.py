"""Genera la tabla de verificación taxonómica (23 nombres). NO asigna nombres aceptados:
hay que consultarlos en World Flora Online (worldfloraonline.org) o Plants of the World Online (powo.science.kew.org),
anotando fecha de consulta. Mientras verificado = no, el nombre registrado es el que se usa."""
import pandas as pd
from config import *
asegurar()
e = pd.read_csv(PROCESSED / "especies_umasbamba_curado.csv")
t = (e.groupby("especie_registrada")
       .agg(genero=("genero", "first"), epiteto=("epiteto", "first"), autoria=("autoria", "first"),
            formaciones=("formacion_vegetal", lambda s: "; ".join(sorted(s))), n_formaciones=("n_formaciones", "first"))
       .reset_index().rename(columns={"especie_registrada": "nombre_registrado"}))
t["nombre_aceptado"] = ""; t["estado"] = ""; t["fuente_consultada"] = ""; t["fecha_consulta"] = ""; t["verificado"] = "no"
t = t.sort_values(["genero", "epiteto"])
t.to_csv(EXTERNAL / "equivalencias_taxonomicas.csv", index=False, encoding="utf-8")
print(len(t), "nombres por verificar ->", EXTERNAL / "equivalencias_taxonomicas.csv")
print("Géneros únicos:", t.genero.nunique())
