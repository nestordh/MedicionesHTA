from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout
)

from models.usuario import Usuario


class Login(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "HTA GLU MEDICION - Login"
        )

        self.resize(350, 285)

        layout = QVBoxLayout()

        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText(
            "Usuario"
        )

        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "Contraseña"
        )

        self.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        ingresar = QPushButton(
            "Ingresar"
        )

        ingresar.clicked.connect(
            self.login
        )

        crear_usuario = QPushButton(
            "Crear usuario"
        )
        crear_usuario.clicked.connect(
            self.mostrar_dialogo_crear_usuario
        )

        layout.addWidget(
            QLabel("Usuario")
        )

        layout.addWidget(
            self.usuario
        )

        layout.addWidget(
            QLabel("Contraseña")
        )

        layout.addWidget(
            self.password
        )

        layout.addWidget(
            ingresar
        )

        layout.addWidget(
            crear_usuario
        )

        self.setLayout(layout)

    def mostrar_dialogo_crear_usuario(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Crear usuario")

        formulario = QFormLayout(dialogo)

        usuario = QLineEdit(
            self.usuario.text().strip() or "admin"
        )

        password = QLineEdit()
        password.setEchoMode(QLineEdit.EchoMode.Password)

        confirmar_password = QLineEdit()
        confirmar_password.setEchoMode(QLineEdit.EchoMode.Password)

        formulario.addRow("Usuario", usuario)
        formulario.addRow("Contraseña", password)
        formulario.addRow("Confirmar contraseña", confirmar_password)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        botones.accepted.connect(dialogo.accept)
        botones.rejected.connect(dialogo.reject)
        formulario.addRow(botones)

        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return

        nombre = usuario.text().strip()
        clave = password.text()

        if not nombre or not clave:
            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Ingrese un nombre de usuario y una contraseña."
            )
            return

        if clave != confirmar_password.text():
            QMessageBox.warning(
                self,
                "Contraseña diferente",
                "Las contraseñas no coinciden."
            )
            return

        try:
            Usuario.crear_usuario(nombre, clave)
            self.usuario.setText(nombre)
            self.password.clear()
            QMessageBox.information(
                self,
                "Usuario creado",
                f"El usuario {nombre} fue creado correctamente."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def login(self):

        from views.principal import VentanaPrincipal

        usuario = self.usuario.text().strip()
        password = self.password.text()

        try:

            if Usuario.login(
                usuario,
                password
            ):
                usuario_id = Usuario.obtener_id(usuario)
                if usuario_id is None:
                    raise ValueError(
                        "No se encontró el identificador del usuario."
                    )

                self.ventana = VentanaPrincipal(usuario, usuario_id)

                self.ventana.show()

                self.close()

            else:

                QMessageBox.warning(
                    self,
                    "Error",
                    "Usuario o contraseña incorrectos"
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )