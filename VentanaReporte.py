# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VentanaReporte.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VentanaReporte(object):
    def setupUi(self, VentanaReporte):
        VentanaReporte.setObjectName("VentanaReporte")
        self.mainLayout = QtWidgets.QVBoxLayout(VentanaReporte)
        self.mainLayout.setObjectName("mainLayout")
        self.contenedorTarjetas = QtWidgets.QWidget(VentanaReporte)
        self.contenedorTarjetas.setObjectName("contenedorTarjetas")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.contenedorTarjetas)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainLayout.addWidget(self.contenedorTarjetas)
        self.botonera = QtWidgets.QHBoxLayout()
        self.botonera.setObjectName("botonera")
        self.btnExportarPDF = QtWidgets.QPushButton(VentanaReporte)
        self.btnExportarPDF.setObjectName("btnExportarPDF")
        self.botonera.addWidget(self.btnExportarPDF)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.botonera.addItem(spacerItem)
        self.btnCerrar = QtWidgets.QPushButton(VentanaReporte)
        self.btnCerrar.setObjectName("btnCerrar")
        self.botonera.addWidget(self.btnCerrar)
        self.mainLayout.addLayout(self.botonera)

        self.retranslateUi(VentanaReporte)
        QtCore.QMetaObject.connectSlotsByName(VentanaReporte)

    def retranslateUi(self, VentanaReporte):
        _translate = QtCore.QCoreApplication.translate
        VentanaReporte.setWindowTitle(_translate("VentanaReporte", "Resumen de Validación"))
        self.btnExportarPDF.setText(_translate("VentanaReporte", "Exportar PDF"))
        self.btnCerrar.setText(_translate("VentanaReporte", "Cerrar"))
