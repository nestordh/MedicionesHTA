import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.conexion import (
    asignar_mediciones_anteriores_a_admin,
    crear_bd
)
from models.usuario import Usuario

from views.login import Login


def main():

    crear_bd()

    Usuario.crear_admin()
    asignar_mediciones_anteriores_a_admin()

    app = QApplication(sys.argv)

    with open(
        BASE_DIR / "assets" / "style.qss",
        "r",
        encoding="utf-8"
    ) as f:

        app.setStyleSheet(
            f.read()
        )
        
    ventana = Login()

    ventana.show()

    sys.exit(
        app.exec()
    )



if __name__ == "__main__":
    main()