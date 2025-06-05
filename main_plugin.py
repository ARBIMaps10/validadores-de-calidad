from qgis.PyQt.QtWidgets import ( QDialog, QTreeWidgetItem, QVBoxLayout, QPushButton, QTreeWidget, QLabel,QWidget, QHBoxLayout, QHeaderView, QDockWidget, QMessageBox, QTableWidgetItem,QAction)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject
import os

from .Validadores_de_Calidad_Base import Ui_Validador
from .VentanaReporte import Ui_VentanaReporte
from .VentanaErrores import Ui_Dialog
from .VentanaAyuda import Ui_Dialog
from .ventana_errores import VentanaErrores 
from .ventana_reporte import VentanaReporte
from .ventana_ayuda import VentanaAyuda
from .validador_logica import validar_todo as ejecutar_validacion
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .import reglas_genericas 
from .import reglas_logicas
from .import reglas_obligatorias
from .validador_logica import ejecutar_todas_las_reglas


class Validador(QWidget, Ui_Validador):
    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.setupUi(self)
        self.proyecto = QgsProject.instance()
        

        if self.proyecto.isDirty():
            print("El proyecto tiene cambios pendientes.")
        else:
            print("Proyecto cargado correctamente.")

        layout_botones = QHBoxLayout()
        layout_izquierda = QHBoxLayout()
        for btn in [self.btnAyuda, self.btnreporte]:
            btn.setFixedSize(110, 30)
            layout_izquierda.addWidget(btn)
            layout_izquierda.addSpacing(10)

        layout_derecha = QHBoxLayout()
        for btn in [self.btnerrores, self.btnValidar]:
            btn.setFixedSize(110, 30)
            layout_derecha.addWidget(btn)
            layout_derecha.addSpacing(10)

        layout_botones.addLayout(layout_izquierda)
        layout_botones.addStretch()
        layout_botones.addLayout(layout_derecha)

        self.layout().addLayout(layout_botones)

        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Reglas de calidad", "Estado"])
        self.tree.setMinimumHeight(300)
        self.tree.itemCollapsed.connect(lambda item: self.tree.setItemExpanded(item, True))

        self.crear_arbol_validacion()
        self.tree.expandAll()
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)

        self.btnValidar.clicked.connect(self.validar_todo)
        self.btnreporte.clicked.connect(self.abrir_reporte)
        self.btnerrores.clicked.connect(self.ver_resultado)
        self.btnAyuda.clicked.connect(self.mostrar_ayuda)

        self.resultados = []  
        self.resultados_resumen = []


    def crear_arbol_validacion(self):
        categorias = [
            ("Reglas de Calidad Genéricas", [
                "Los datos deben corresponder a su modelo (ilivalidator)",
            ]),
            ("Reglas de Calidad Lógicas", [
                "La posición 22 a la 30 del número predial debe coincidir con la condición del predio",
                "La posición 22 a la 30 del número predial no cumple con la estructura esperada para una unidad predial en PH",
            ]),
            ("Reglas de Calidad Obligatorias", [
                "El tipo de predio no debe ser null",
                "La condición del predio no puede ser null",
                "La destinación económica no debe ser null",
                "La fecha de la visita predial no debe null",
                "El resultado de la visita al predio no debe ser null",
                "El atributo tiene área registral del atributo no debe ser null",
                "El atributo tiene FMI no debe ser null",
                "El tipo de documento de quien atendió la visita no debe se null",
                "El número de documento de quien atendió la visita no debe ser null",
                "El nombre de quien atendió la visita no debe ser null",
                "El departamento de residencia del interesado no debe ser null",
                "El municipio de residencia del interesado no debe ser null",
            ])
        ]

        for categoria, subcategorias in categorias:
            item_categoria = QTreeWidgetItem(self.tree)
            item_categoria.setText(0, categoria)
            for subcategoria in subcategorias:
                item_subcategoria = QTreeWidgetItem(item_categoria)
                item_subcategoria.setText(0, subcategoria)
                item_subcategoria.setData(0, Qt.UserRole, subcategoria)

    def validar_todo(self):
        self.resultados = ejecutar_validacion(self.tree, self.btnValidar, self.iface)

    
    def abrir_reporte(self):
        item = self.tree.currentItem()
        if not item:
            QMessageBox.information(self, "Sin selección", "Selecciona una subcategoría para abrir el reporte.")
            return
        
        subcategoria = item.data(0, Qt.UserRole)
        if not subcategoria:
            QMessageBox.information(self, "Elemento inválido", "Selecciona una subcategoría válida.")
            return
        
        self.resultados_resumen = ejecutar_todas_las_reglas()

        
        for m in [reglas_genericas, reglas_logicas, reglas_obligatorias]:
            if subcategoria in m.clases_con_reglas:
                modulo_encontrado = m
                break
        
        codigos_esperados = modulo_encontrado.clases_con_reglas.get(subcategoria, [])
        
        resultados_filtrados = [r for r in self.resultados_resumen if r["regla"] in codigos_esperados]

        if not resultados_filtrados:
            QMessageBox.information(self, "sin resultados", f"No hay resultados para la subcategoria: {subcategoria}")
            return
        
        ventana = VentanaReporte(resultados_filtrados)
        ventana.exec_()

    def ver_resultado(self):
        item = self.tree.currentItem()
        if not item:
           QMessageBox.information(self, "Sin selección", "Selecciona una subcategoría para ver errores.")
           return

        subcategoria = item.data(0, Qt.UserRole)
        if not subcategoria:
            QMessageBox.information(self, "Elemento inválido", "Selecciona una subcategoría válida.")
            return

        modulo = None
        for m in [reglas_genericas, reglas_logicas, reglas_obligatorias]:
            if subcategoria in m.clases_con_reglas:
                modulo = m
                break
        
        if not modulo:
            QMessageBox.information(self, "Elemento inválido", "No se encontró un módulo válido para la subcategoría seleccionada.")
            return
        
        errores_filtrados = []
        codigos_subcategoria = modulo.clases_con_reglas.get(subcategoria, [])

        for errors in self.resultados:
            if errors["regla"] in codigos_subcategoria:
                errores_filtrados.append(errors)

        if errores_filtrados:
           ventana = VentanaErrores(errores_filtrados, self)
           ventana.exec_()

        else:
            QMessageBox.information(self, "Sin errores", f"No se encontraron errores en la subcategoría seleccionada: {subcategoria}")


    def mostrar_ayuda(self):
        self.ventana_ayuda = VentanaAyuda(self)
        self.ventana_ayuda.exec_()


class ValidadoresPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dock_widget = None
        self.validador_widget = None
        self.action = None
        self.proyecto = QgsProject.instance()

    def initGui(self):
        self.validador_widget = Validador(self.iface)
        self.dock_widget = QDockWidget("Validadores de Calidad", self.iface.mainWindow())
        self.dock_widget.setWidget(self.validador_widget)

       
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        self.action = QAction(QIcon(icon_path), "Validadores de Calidad", self.iface.mainWindow())
        self.action.triggered.connect(self.mostrar_dock)

        self.iface.addPluginToMenu("Validadores", self.action)
        self.iface.addToolBarIcon(self.action)

        print(f"Plugin cargado. Proyecto: {self.proyecto.fileName()}")

    def unload(self):
        if self.dock_widget:
            self.iface.removeDockWidget(self.dock_widget)
        if self.action:
            self.iface.removePluginMenu("Validadores", self.action)
            self.iface.removeToolBarIcon(self.action)

    def mostrar_dock(self):
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget)
        self.dock_widget.show()

def classFactory(iface):
    return ValidadoresPlugin(iface)
