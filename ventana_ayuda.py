from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QMessageBox
import os 
import sys
from .VentanaAyuda import Ui_Dialog

class VentanaAyuda(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(VentanaAyuda, self).__init__(parent)
        self.setWindowTitle("Ayuda - Manual de Usuario")
        self.setMinimumSize(400, 150)

        layout = QVBoxLayout()

        label = QLabel("Presione el boton para abrir el manual de usuario en formato PDF.")
        layout.addWidget(label)

        boton_abrir_pdf = QPushButton("Abrir Manual de usuario")
        boton_abrir_pdf.clicked.connect(self.abrir_pdf)
        layout.addWidget(boton_abrir_pdf)

        boton_cerrar = QPushButton("cerrar")
        boton_cerrar.clicked.connect(self.close)
        layout.addWidget(boton_cerrar)

        self.setLayout(layout)

    def abrir_pdf(self):
        ruta_pdf = os.path.join(os.path.dirname(__file__), "manual_usuario.pdf")
        if not os.path.exists(ruta_pdf):
            QMessageBox.critical(self, "Error", "El manual de usuario no se encuentra disponible.")
            return
        
        if sys.platform.startswith('linux'):
            os.system(f'open"{ruta_pdf}"')
        elif os.name == 'nt': 
             os.startfile(ruta_pdf)
        elif os.name == 'posix':
             os.system(f'xdg-open "{ruta_pdf}"')




        

