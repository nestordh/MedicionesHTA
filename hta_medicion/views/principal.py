
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTimeEdit,
    QToolBar,
    QWidget,
)
from PySide6.QtCore import QDate, QTime, Qt
from PySide6.QtGui import QAction, QFont, QColor, QIcon, QPainter, QPixmap

from models.medicion import Medicion
from models.usuario import Usuario
from exports.export_excel import exportar_excel
from views.graficos import GraficoPresion


class VentanaPrincipal(QMainWindow):

    def __init__(self, usuario, usuario_id):
        super().__init__()
        self.usuario_actual = usuario
        self.usuario_id = usuario_id
        self.usuario_id_vista = usuario_id
        self.selector_usuario = None
        self.id_actual = None
        self.columna_orden = 1
        self.orden_tabla = Qt.SortOrder.DescendingOrder
        self.setWindowTitle("HTA MEDICION")
        self.resize(1280, 740)
        self.lbl_total = QLabel()
        self.lbl_promedio = QLabel()
        self.lbl_maxima = QLabel()
        self.lbl_minima = QLabel()
        self.lbl_glucosa = QLabel()
        self.crear_interfaz()
        self.listar()


    def crear_interfaz(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QGridLayout()
        self.crear_barra_menu()

        self.fecha = QDateEdit()
        self.fecha.setDate(QDate.currentDate())

        self.hora = QTimeEdit()
        self.hora.setTime(QTime.currentTime())

        self.sistolica = QSpinBox()
        self.sistolica.setRange(70, 250)

        self.diastolica = QSpinBox()
        self.diastolica.setRange(40, 150)

        self.pulsaciones = QSpinBox()
        self.pulsaciones.setRange(35, 220)

        self.glucosa = QSpinBox()
        self.glucosa.setRange(40, 150)
        self.glucosa.setMaximumWidth(120)

        self.observacion = QTextEdit()
        self.observacion.setFixedHeight(90)
        self.observacion.setPlaceholderText("Ingrese una observación")

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(9)

        self.tabla.setHorizontalHeaderLabels([
            "ID",
            "Fecha ^",
            "Hora",
            "Sistolica ^ ",
            "Diastolica ^",
            "Pulsaciones",
            "Glucosa",
            "Ingresado por",
            "Observacion"
        ])

        self.tabla.cellClicked.connect(self.cargar)

        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tabla.horizontalHeader().setStretchLastSection(True)
        encabezado = self.tabla.horizontalHeader()
        encabezado.setSectionsClickable(True)
        encabezado.setSortIndicatorShown(True)
        encabezado.setSortIndicator(
            self.columna_orden,
            self.orden_tabla
        )
        encabezado.sectionClicked.connect(self.ordenar_por_columna)
        self.tabla.resizeColumnsToContents()

        self.fecha_desde = QDateEdit()
        self.fecha_desde.setDate(QDate.currentDate().addMonths(-1))

        self.fecha_hasta = QDateEdit()
        self.fecha_hasta.setDate(QDate.currentDate())

        btn_buscar = QPushButton("Buscar")

        btn_buscar.clicked.connect(self.buscar_por_fecha)

        guardar = QPushButton("Guardar")

        modificar = QPushButton("Modificar")

        eliminar = QPushButton("Eliminar")

        excel = QPushButton("Exportar Excel")

        grafico = QPushButton("Grafico")

        guardar.clicked.connect(self.guardar)

        modificar.clicked.connect(self.modificar)

        eliminar.clicked.connect(self.eliminar)

        excel.clicked.connect(self.exportar)

        grafico.clicked.connect(self.grafico)

        layout.addWidget(QLabel("Fecha"),0,0)
        layout.addWidget(self.fecha,0,1)

        layout.addWidget(QLabel("Hora"),1,0)
        layout.addWidget(self.hora,1,1)

        layout.addWidget(QLabel("Sistolica"),2,0)
        layout.addWidget(self.sistolica,2,1)

        layout.addWidget(QLabel("Diastolica"),3,0)
        layout.addWidget(self.diastolica,3,1)

        layout.addWidget(QLabel("Pulsaciones"),4,0)
        layout.addWidget(self.pulsaciones,4,1)

        layout.addWidget(QLabel("Glucosa"),5,0)
        layout.addWidget(self.glucosa,5,1)

        layout.addWidget(QLabel("Observación"),6,0,1,2)

        layout.addWidget(self.observacion,7,0,1,2)

        layout.addWidget(guardar,8,0)

        layout.addWidget(modificar,8,1)

        layout.addWidget(eliminar,9,0)

        layout.addWidget(excel,9,1)

        layout.addWidget(grafico,10,0)

        layout.addWidget(self.tabla,0,2,19,1)

        # Añadir boton Promedio Diario
        promedio = QPushButton("Promedio Diario")
        promedio.clicked.connect(self.mostrar_promedios)
        layout.addWidget(promedio,10,1)

        layout.addWidget(QLabel("Desde"),11,0)
        layout.addWidget(self.fecha_desde,11,1)
        layout.addWidget(QLabel("Hasta"),12,0)
        layout.addWidget(self.fecha_hasta,12,1)
        layout.addWidget(btn_buscar,13,0,1,2)

        layout.addWidget(self.lbl_total,14,0,1,2)
        layout.addWidget(self.lbl_promedio,15,0,1,2)
        layout.addWidget(self.lbl_maxima,16,0,1,2)
        layout.addWidget(self.lbl_minima,17,0,1,2)
        layout.addWidget(self.lbl_glucosa,18,0,1,2)

        central.setLayout(layout)

        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def crear_barra_menu(self):
        menu_abm = self.menuBar().addMenu("ABM de mediciones")
        for texto, funcion in (
            ("Alta / Guardar", self.guardar),
            ("Modificar", self.modificar),
            ("Baja / Eliminar", self.eliminar),
            ("Limpiar formulario", self.limpiar),
        ):
            accion = QAction(texto, self)
            accion.triggered.connect(
                lambda checked=False, callback=funcion: callback()
            )
            menu_abm.addAction(accion)

        menu_consultas = self.menuBar().addMenu("Consultas")
        for texto, funcion in (
            ("Buscar por fecha", self.buscar_por_fecha),
            ("Promedio diario", self.mostrar_promedios),
            ("Gráficos", self.grafico),
        ):
            accion = QAction(texto, self)
            accion.triggered.connect(
                lambda checked=False, callback=funcion: callback()
            )
            menu_consultas.addAction(accion)

        menu_exportar = self.menuBar().addMenu("Exportar")
        accion_excel = QAction("Exportar a Excel", self)
        accion_excel.triggered.connect(
            lambda checked=False: self.exportar()
        )
        menu_exportar.addAction(accion_excel)

        menu_usuario = self.menuBar().addMenu(
            self.crear_icono_avatar(self.usuario_actual),
            self.usuario_actual
        )
        sesion = menu_usuario.addAction(
            f"Sesión activa: {self.usuario_actual}"
        )
        sesion.setEnabled(False)

        if self.usuario_actual == "admin":
            barra_usuarios = QToolBar("Vista de usuario", self)
            barra_usuarios.setMovable(False)
            barra_usuarios.addWidget(QLabel("Mediciones de:"))

            self.selector_usuario = QComboBox()
            for usuario_id, nombre in Usuario.listar_usuarios():
                self.selector_usuario.addItem(nombre, usuario_id)

            indice_admin = self.selector_usuario.findData(
                self.usuario_id_vista
            )
            if indice_admin >= 0:
                self.selector_usuario.setCurrentIndex(indice_admin)

            self.selector_usuario.currentIndexChanged.connect(
                self.cambiar_usuario
            )
            barra_usuarios.addWidget(self.selector_usuario)
            self.addToolBar(Qt.ToolBarArea.TopToolBarArea, barra_usuarios)

    @staticmethod
    def crear_icono_avatar(nombre):
        partes = nombre.split()
        iniciales = "".join(parte[0] for parte in partes[:2]).upper() or "?"

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#0078d7"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(1, 1, 30, 30)
        painter.setPen(QColor("#ffffff"))

        fuente = QFont()
        fuente.setBold(True)
        fuente.setPointSize(10)
        painter.setFont(fuente)
        painter.drawText(
            pixmap.rect(),
            Qt.AlignmentFlag.AlignCenter,
            iniciales
        )
        painter.end()

        return QIcon(pixmap)


    def guardar(self):
        try:
            Medicion.guardar(
                self.fecha.date().toString("yyyy-MM-dd"),
                self.hora.time().toString("HH:mm:ss"),
                self.sistolica.value(),
                self.diastolica.value(),
                self.pulsaciones.value(),
                self.glucosa.value(),
                self.observacion.toPlainText(),
                self.usuario_id_vista,
                self.usuario_id
            )
            self.listar()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

        else:
            if (
                self.sistolica.value() >= 140
                or
                self.diastolica.value() >= 90
                and 
                self.glucosa.value() >= 200
            ):
                QMessageBox.warning(
                    self,
                    "Alerta",
                    "Presión arterial elevada."

                )

    
    def listar(self):
    #     datos = Medicion.listar()
    #     self.tabla.setRowCount(
    #         len(datos)
    #     )
    #     for fila, reg in enumerate(datos):
    #         for col, valor in enumerate(reg[:7]):
    #             self.tabla.setItem(
    #                 fila,
    #                 col,
    #                 QTableWidgetItem(
    #                     str(valor)
    #                 )
    #             )
        datos = Medicion.listar(self.usuario_id_vista)
        self.cargar_tabla(datos)
        self.actualizar_estadisticas()


    def cargar(self,row,col):
    #     self.id_actual = int(self.tabla.item(row,0).text())

        try:

            def texto(columna):
                item = self.tabla.item(row, columna)
                if item is None:
                    raise ValueError("Seleccione una fila válida.")
                return item.text()

            self.id_actual = int(texto(0))

            fecha = texto(1)
            hora = texto(2)

            self.fecha.setDate(
                QDate.fromString(
                    fecha,
                    "yyyy-MM-dd"
                )
            )

            self.hora.setTime(
                QTime.fromString(
                    hora,
                    "HH:mm:ss"
                )
            )

            self.sistolica.setValue(
                int(texto(3))
            )

            self.diastolica.setValue(
                int(texto(4))
            )

            self.pulsaciones.setValue(
                int(texto(5))
            )

            self.glucosa.setValue(
                int(texto(6))
            )

            self.observacion.setText(
                texto(8)
            )

        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )

   
    def modificar(self):
        ## pass
        if not self.id_actual:
            QMessageBox.warning(
                self,
                "Aviso",
                "Seleccione un registro."
            )
            return

        try:
            if Medicion.obtener(
                self.id_actual,
                self.usuario_id_vista
            ) is None:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Registro inexistente."
                )
                return

            Medicion.modificar(
                self.id_actual,
                self.fecha.date().toString(
                    "yyyy-MM-dd"
                ),
                self.hora.time().toString(
                    "HH:mm:ss"
                ),
                self.sistolica.value(),
                self.diastolica.value(),
                self.pulsaciones.value(),
                self.glucosa.value(),
                self.observacion.toPlainText(),
                self.usuario_id_vista
            )

            QMessageBox.information(
                self,
                "Correcto",
                "Registro actualizado."
            )
            self.listar()
            self.limpiar()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )


    def eliminar(self):
        if not self.id_actual:
            return
        Medicion.eliminar(
            self.id_actual,
            self.usuario_id_vista
        )
        self.listar()
        self.limpiar()


    def exportar(self):
        try:
            archivo = exportar_excel(
                Medicion.listar(self.usuario_id_vista)
            )
            QMessageBox.information(
                self,
                "Excel",
                f"Archivo generado:\n{archivo}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )


    def grafico(self):

        try:

            GraficoPresion.mostrar(self.usuario_id_vista)

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )


    def limpiar(self):

        self.id_actual = None

        self.fecha.setDate(
            QDate.currentDate()
        )

        self.hora.setTime(
            QTime.currentTime()
        )

        self.sistolica.setValue(
            120
        )

        self.diastolica.setValue(
            80
        )

        self.pulsaciones.setValue(
            70
        )

        self.glucosa.setValue(0)

        self.observacion.clear()       

    def cambiar_usuario(self, indice):
        if self.selector_usuario is None:
            return

        usuario_id = self.selector_usuario.itemData(indice)
        if usuario_id is None:
            return

        self.usuario_id_vista = int(usuario_id)
        self.limpiar()
        self.listar()

    def actualizar_fecha_hora(self):
        self.fecha.setDate(QDate.currentDate())
        self.hora.setTime(QTime.currentTime())

    # Búsqueda por fechas
    def buscar_por_fecha(self):
        try:
            datos = Medicion.buscar_por_fecha(
                self.fecha_desde.date().toString(
                    "yyyy-MM-dd"
                ),
                self.fecha_hasta.date().toString(
                    "yyyy-MM-dd"
                ),
                self.usuario_id_vista
            )
            self.cargar_tabla(
                datos
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    # Separar carga de tabla
    def cargar_tabla(self,datos):
        self.tabla.setSortingEnabled(False)
        self.tabla.setRowCount(len(datos))

        for fila, reg in enumerate(datos):
            # sistolica = reg[3]
            # diastolica = reg[4]
            sistolica = int(reg[3])
            diastolica = int(reg[4])

            color = None

            if sistolica >= 140 or diastolica >= 90: 
                color = QColor("#ff7070")
            # hipotension
            elif sistolica < 100:
                color = QColor("#7fc8ff")
            # normal
            elif sistolica < 120:
                color = QColor("#88ff88")
            elif sistolica >= 120:
                color = QColor("#ffd966")
            # elevada
            elif sistolica < 140:
                color = QColor("#ffe66d")
            else:
                # color = QColor("#7cff7c")
                color = QColor("#ff8080")


            if sistolica >= 145 or diastolica >= 90: 
                color = QColor("#ff7070")
            elif sistolica < 145:
                color = QColor("#C89263")
            elif sistolica < 120:
                color = QColor("#81C784")
            elif sistolica < 100: 
                color = QColor("#64B5F6")
            else:
                color = QColor("#4A4343")


            for col, valor in enumerate(reg[:9]):
                item = QTableWidgetItem()
                if col in (0, 3, 4, 5, 6):
                    item.setData(
                        Qt.ItemDataRole.DisplayRole,
                        int(valor)
                    )
                else:
                    item.setText(str(valor))

                item.setBackground(
                    color
                )

                self.tabla.setItem(
                    fila,
                    col,
                    item
                )

        self.tabla.sortItems(
            self.columna_orden,
            self.orden_tabla
        )

    def ordenar_por_columna(self, columna):
        if columna == self.columna_orden:
            self.orden_tabla = (
                Qt.SortOrder.AscendingOrder
                if self.orden_tabla == Qt.SortOrder.DescendingOrder
                else Qt.SortOrder.DescendingOrder
            )
        else:
            self.columna_orden = columna
            self.orden_tabla = Qt.SortOrder.DescendingOrder

        self.tabla.horizontalHeader().setSortIndicator(
            self.columna_orden,
            self.orden_tabla
        )
        self.tabla.sortItems(
            self.columna_orden,
            self.orden_tabla
        )

    # Función actualizar_estadisticas()
    def actualizar_estadisticas(self):
        # try:
        datos = Medicion.estadisticas(self.usuario_id_vista)
        if not datos:
            return
            # cantidad = datos[0] or 0
            # prom_sis = round(datos[1] or 0,1)
            # prom_dia = round(datos[2] or 0,1)
            # prom_pul = round(datos[3] or 0,1)

        total = datos[0]
        promedio_sis = round(datos[1] or 0, 1)
        promedio_dia = round(datos[2] or 0, 1)

        maxima = datos[4] or 0
        minima = datos[5] or 0
        promedio_glucosa = datos[6]

        self.lbl_total.setText(f"Total registros: {total}")
        self.lbl_promedio.setText(f"Promedio: {promedio_sis}/{promedio_dia} mmHg")
        self.lbl_maxima.setText(f"Máxima Sistólica: {maxima} mmHg")
        self.lbl_minima.setText(f"Mínima Sistólica: {minima} mmHg")
        glucosa_texto = (
            f"{round(promedio_glucosa, 1)} mg/dL"
            if promedio_glucosa is not None
            else "Sin datos"
        )
        self.lbl_glucosa.setText(
            f"Glucosa promedio: {glucosa_texto}"
        )


    # Metodo mostrar_promedios()
    def mostrar_promedios(self):
        datos = Medicion.promedio_diario(self.usuario_id_vista)
        texto = ""
        for d in datos:
            texto += (
                f"{d[0]}  "
                f"SIS:{d[1]} mmHg "
                f"DIA:{d[2]}  "
                f"PUL:{d[3]}  "
                f"GLU:{d[4] if d[4] is not None else 's/d'} mg/dL\n"
            )
        QMessageBox.information(
            self,
            "Promedios diarios",
            texto
        )  


    def crear_kpi(self, texto):
        label = QLabel(texto)
        label.setStyleSheet("""
            background:#2d2d30;
            border:1px solid #444;
            border-radius:12px;
            padding:15px;
            font-size:16px;
            font-weight:bold;
            color:white;
        """)
        return label










