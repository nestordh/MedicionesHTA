from pathlib import Path
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def exportar_pdf(datos):

    if not datos:
        raise Exception(
            "No hay datos para exportar."
        )

    archivo = (
        Path.home()
        / "Documents"
        / "mediciones.pdf"
    )

    pdf = SimpleDocTemplate(
        str(archivo)
    )

    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph(
            "Informe HTA MEDICION",
            styles["Title"]
        )
    )

    elementos.append(
        Spacer(1, 20)
    )

    tabla = [[
        "Fecha",
        "Hora",
        "SIS",
        "DIA",
        "PUL",
        "GLU (mg/dL)",
        "Ingresado por",
        "Obs"
    ]]

    for r in datos:

        tabla.append([
            r[1],
            r[2],
            r[3],
            r[4],
            r[5],
            r[6],
            r[7],
            r[8]
        ])

    tabla_pdf = Table(tabla)

    tabla_pdf.setStyle(
        TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.grey),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),1,colors.black)
        ])
    )

    elementos.append(
        tabla_pdf
    )

    pdf.build(
        elementos
    )

    return str(archivo)