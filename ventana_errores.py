from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import os
import csv
import shutil
import subprocess
import sys
from .VentanaErrores import Ui_Dialog

class VentanaErrores(QDialog, Ui_Dialog):
    def __init__(self, resultados, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setSizeGripEnabled(True)
        self.setMinimumSize(600, 400)
        
        self.btncerrar.setDefault(False)
        self.btncerrar.setAutoDefault(False)
        self.btnayuda.setDefault(False)
        self.btnayuda.setAutoDefault(False)
        self.btnLimpiarBusqueda.setDefault(False)

        self.resultados = resultados
        self.resultados_originales = list(resultados)

        self.cargar_tabla()
        self.btncerrar.clicked.connect(self.confirmar_cierre)
        self.lineaBusqueda.returnPressed.connect(self.filtrar_tabla)
        self.btnLimpiarBusqueda.clicked.connect(self.limpiar_filtro)
        self.btnayuda.clicked.connect(self.descargar_pdf_ayuda)
        self.btnExportar.clicked.connect(self.exportar_excel)

    def cargar_tabla(self):
    
      resultados_ordenados = sorted(self.resultados, key=lambda x: x.get("aid", ""))
  
      self.tablaResultados.setRowCount(len(resultados_ordenados))
      self.tablaResultados.setColumnCount(5)
      self.tablaResultados.setHorizontalHeaderLabels(["Código", "AID", "Capa", "Regla", "Descripción"])

      for fila, resultado in enumerate(resultados_ordenados):
          self.tablaResultados.setItem(fila, 0, QTableWidgetItem(str(resultado["codigo"])))
          self.tablaResultados.setItem(fila, 1, QTableWidgetItem(str(resultado["aid"])))
          self.tablaResultados.setItem(fila, 2, QTableWidgetItem(str(resultado["capa"])))
          self.tablaResultados.setItem(fila, 3, QTableWidgetItem(str(resultado["regla"])))
          self.tablaResultados.setItem(fila, 4, QTableWidgetItem(str(resultado["descripcion"])))

          cumple = resultado.get("cumple", True)
          color = QColor(144, 238, 144) if cumple else QColor(255, 182, 193)

          for col in range(5):
              item = self.tablaResultados.item(fila, col)
              if item:
                 item.setBackground(color)

      self.tablaResultados.resizeColumnsToContents()
      self.tablaResultados.horizontalHeader().setStretchLastSection(True)
      self.tablaResultados.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
    
    def filtrar_tabla(self):
        texto = self.lineaBusqueda.text().lower()
        print(f"filtrado por {texto}")

        if not texto:
            return
        
        resultados_filtrados = [
            resultado for resultado in self.resultados_originales
            if texto in str(resultado["regla"]).lower()
        ]

        self.resultados = resultados_filtrados
        self.cargar_tabla()
    
    def limpiar_filtro(self):
        self.lineaBusqueda.clear()
        self.resultados = list(self.resultados_originales)
        self.cargar_tabla()

    def confirmar_cierre(self):
        respuesta = QMessageBox.question(self, "Confirmar cierre",
                                         "¿Estás seguro de que deseas cerrar esta ventana?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            self.accept()

    def descargar_pdf_ayuda(self):
        ruta_origen = os.path.join(os.path.dirname(__file__), "manual_ayuda.pdf")
        if not os.path.exists(ruta_origen):
            QMessageBox.critical(self, "Error", "El archivo PDF de ayuda no se encuentra.")
            return

        ruta_destino, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "manual_ayuda.pdf", "Archivos PDF (*.pdf)")
        if ruta_destino:
            try:
                shutil.copyfile(ruta_origen, ruta_destino)
                QMessageBox.information(self, "Éxito", "El archivo se guardó correctamente.")

                abrir = QMessageBox.question(
                    self,
                    "Abrir PDF",
                    "¿Deseas abrir el PDF ahora?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )

                if abrir == QMessageBox.Yes:
                    self.abrir_pdf(ruta_destino)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{str(e)}")

    def abrir_pdf(self, ruta):
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', ruta))
            elif os.name == 'nt':
                os.startfile(ruta)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', ruta))
        except Exception as e:
            QMessageBox.warning(self, "Error al abrir PDF", f"No se pudo abrir el PDF:\n{str(e)}")

    def exportar_excel(self):
        path, _ = QFileDialog.getSaveFileName(
            self,"Guardar como Exel", "errores_validacion.csv", "csv (*.csv)"
        )
        if not path:
            return
        
        if not path.lower().endswith('.csv'):
            path += '.csv'
        
        try:
            with open(path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer =csv.writer(file, delimiter=',')
                headers = ["Codigo", "AID", "Capa","Regla", "Descripcion"]
                writer.writerow(headers)

                row_count = self.tablaResultados.rowCount()
                col_count = self.tablaResultados.columnCount()


                for i in range(row_count):
                    fila = []
                    for j in range(col_count):
                        item = self.tablaResultados.item(i, j)
                        valor = item.text() if item else ""
                        fila.append(valor)
                    writer.writerow(fila)

            respuesta = QMessageBox.question(
                self,
                "Archivo guarddo",
                f"El archivo se gurado correctamente en:\n{path}\n\n¿Deseas abrirlo ahora?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                try: 
                    if os.name == 'nt':
                        os.startfile(path)
                    elif os.name == 'posix':
                        subprocess.call(['xdg-open', path])
                except Exception as e:
                    QMessageBox.warnig(self, "Aviso", "No se pudo abrir el archivo: \n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{str(e)}")