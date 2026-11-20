from pathlib import Path
import pandas as pd


def exportar_excel(datos):

    if not datos:
        raise Exception(
            "No existen datos para exportar."
        )

    columnas = [
        "ID",
        "Fecha",
        "Hora",
        "Sistólica",
        "Diastólica",
        "Pulsaciones",
        "Glucosa (mg/dL)",
        "Ingresado por",
        "Observación",
        "Fecha Creación"
    ]

    df = pd.DataFrame(
        datos,
        columns=columnas
    )

    # carpeta = Path.home() / "Documents"
    carpeta = Path.home() / "Descargas"

    archivo = carpeta / "mediciones.xlsx"

    df.to_excel(
        archivo,
        index=False
    )

    return str(archivo)