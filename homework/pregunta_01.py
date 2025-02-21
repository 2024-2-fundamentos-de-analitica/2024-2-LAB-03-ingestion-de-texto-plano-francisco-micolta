"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
import re


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    
    
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip()]

    regex_inicio = re.compile(r"^(\d+)\s+(\d+)\s+(\d+,\d+)\s*%\s+(.*)")

    data = []
    cluster_id = None
    cant_palabras = None
    porc = None
    palabras_clave = []

    for line in lines:
        match = regex_inicio.match(line)
        if match:
            if cluster_id is not None:
                # Procesar el cluster anterior
                all_keywords = " ".join(palabras_clave)
                all_keywords = re.sub(r"\s+", " ", all_keywords)
                kw_split = [k.strip() for k in all_keywords.split(",") if k.strip()]
                all_keywords = ", ".join(kw_split)

                # Eliminar punto final (si existe)
                all_keywords = all_keywords.strip()
                if all_keywords.endswith("."):
                    all_keywords = all_keywords[:-1]

                data.append([cluster_id, cant_palabras, porc, all_keywords])

            # Nuevo cluster
            cluster_id = int(match.group(1))
            cant_palabras = int(match.group(2))
            porc_str = match.group(3).replace(",", ".")
            porc = float(porc_str)

            palabras_clave = [match.group(4)]
        else:
            # Continuación de palabras clave
            if cluster_id is not None:
                palabras_clave.append(line)

    # Último cluster
    if cluster_id is not None:
        all_keywords = " ".join(palabras_clave)
        all_keywords = re.sub(r"\s+", " ", all_keywords)
        kw_split = [k.strip() for k in all_keywords.split(",") if k.strip()]
        all_keywords = ", ".join(kw_split)

        # Eliminar punto final (si existe)
        all_keywords = all_keywords.strip()
        if all_keywords.endswith("."):
            all_keywords = all_keywords[:-1]

        data.append([cluster_id, cant_palabras, porc, all_keywords])

    df = pd.DataFrame(
        data,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )

    return df