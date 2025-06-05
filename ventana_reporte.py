from PyQt5.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QFrame, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from .VentanaReporte import Ui_VentanaReporte
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas as canvas_module
from reportlab.platypus import KeepTogether
import os
import subprocess
import platform


class VentanaReporte(QDialog, Ui_VentanaReporte):
    def __init__(self, resultados, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setMinimumSize(800, 500)
        self.resize(1000, 600)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.scrollContent = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scrollArea.setWidget(self.scrollContent)

        self.verticalLayout.addWidget(self.scrollArea)

        self.btnCerrar.clicked.connect(self.close)
        self.btnExportarPDF.clicked.connect(self.descargar_pdf_informe)

        self.resultados = resultados
        self.mostrar_tarjetas(resultados)

    def mostrar_tarjetas(self, resultados):
        
        while self.scrollLayout.count():
            item = self.scrollLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deletlater()

        for r in resultados:
            regla = r.get("regla", "sin_regla")
            descripcion = r.get("descripcion", "sin_descripcion")
            errores_lista = r.get("errores", [])
            errores = len(errores_lista) if isinstance(errores_lista, list) else 0

            self.scrollLayout.addWidget(self.crear_tarjeta(regla, descripcion, errores))

    def crear_tarjeta(self, regla, descripcion, errores):
        tarjeta = QFrame()
        tarjeta.setFrameShape(QFrame.StyledPanel)
        tarjeta.setStyleSheet(self.estilo_tarjeta(errores))

        layout = QVBoxLayout(tarjeta)

        lblregla = QLabel(f"<b>Regla: {regla}</b>")
        lblregla.setStyleSheet("font-size: 16px; color: white; background-color: #006a86; padding: 6px;")
        layout.addWidget(lblregla)

        lblDescripcion = QLabel(f"<b>Descripción:</b><br>{descripcion}")
        lblDescripcion.setStyleSheet("font-size: 14px; padding: 8px;")
        lblDescripcion.setWordWrap(True)
        layout.addWidget(lblDescripcion)

        if errores > 0:
            lblErrores = QLabel(f"❌ Se identificaron {errores} error{'es' if errores > 1 else ''}")
            lblErrores.setStyleSheet("color: red; font-weight: bold; font-size: 14px; padding: 4px 8px;")
        else:
            lblErrores = QLabel("✔️ No se identificaron errores")
            lblErrores.setStyleSheet("color: green; font-weight: bold; font-size: 14px; padding: 4px 8px;")

        layout.addWidget(lblErrores)

        return tarjeta

    def estilo_tarjeta(self, errores):
        borde = "#e74c3c" if errores > 0 else "#2ecc71"
        return f"""
        QFrame {{
            border: 4px solid {borde};
            border-radius: 5px;
            margin: 10px;
            background-color: #fdfdfd;
        }}
        """

    def descargar_pdf_informe(self):
        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar reporte como", "reporte_validacion.pdf", "PDF Files (*.pdf)")
        if not ruta_archivo:
            return

        try:
            doc = SimpleDocTemplate(
                ruta_archivo,
                pagesize=A4,
                leftMargin=40,
                rightMargin=40,
                topMargin=50,
                bottomMargin=40
            )

            story = []
            styles = getSampleStyleSheet()

            estilo_titulo = ParagraphStyle(
                name="Titulo",
                fontSize=16,
                alignment=1,
                leading=22,
                spaceAfter=10,
                fontName="Helvetica-Bold"
            )

            estilo_regla = ParagraphStyle("ReglaTitulo", fontSize=12, leading=14, fontName="Helvetica-Bold")
            estilo_texto = ParagraphStyle("Texto", fontSize=10, leading=13)


            # Logo en la esquina superior derecha
            logo_path = os.path.join(os.path.dirname(__file__), "logo_arbitrium.png.png")
            if os.path.exists(logo_path):
                img_logo = Image(logo_path, width=100, height=40)
            else:
                img_logo = Paragraph("", styles["Normal"])

            header = Table([
                [Paragraph("", styles["Normal"]), img_logo]
            ], colWidths=[400, 100])

            header.setStyle(TableStyle([
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))

            story.append(header)
            story.append(Spacer(1, 10))
            story.append(Paragraph("Reporte de validación de reglas de calidad ", estilo_titulo))
            story.append(Spacer(1, 12))

            
            marco = Table([
                [Paragraph("El archivo XTF suministrado es válido "
                           "A continuación, se presentan los resultados de las reglas de calidad definidas para dicho modelo.",
                           styles["Normal"])]
            ], colWidths=[500])

            marco.setStyle(TableStyle([
                ("BOX", (0, 0), (-1, -1), 2, colors.HexColor("#006a86")),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]))

            story.append(marco)
            story.append(Spacer(1, 20))

            
            resumen = {}
            for r in self.resultados:
                regla = r.get("regla", "sin_regla")
                descripcion = r.get("descripcion", "sin_descripcion")
                errores_lista = r.get("errores", [])
                errores = len(errores_lista) if isinstance(errores_lista, list) else 0


                color_borde = colors.green if errores == 0 else colors.red
                color_fondo = colors.whitesmoke
                mensaje = (
                    "<b><font color='green'>✔️ No hay errores</font></b>"
                    if errores == 0 else
                    f"<b><font color='red'>❌ Se identificaron {errores} error{'es' if errores > 1 else ''}</font></b>"
                )

                tarjeta = Table([
                    [Paragraph(f"Regla: {regla}", estilo_regla)],
                    [Paragraph(f"<b>Descripción:</b> {descripcion}", estilo_texto)],
                    [Paragraph(mensaje, estilo_texto)]
                ], colWidths=[500])

                tarjeta.setStyle(TableStyle([
                    ("BOX", (0, 0), (-1, -1), 1.5, color_borde),
                    ("BACKGROUND", (0, 0), (-1, -1), color_fondo),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]))

                story.append(KeepTogether([tarjeta]))
                story.append(Spacer(1, 14))

            def dibujar_marco(canvas, doc):
                canvas.saveState()
                canvas.setStrokeColor(colors.HexColor("#006a86"))
                canvas.setLineWidth(3)
                canvas.rect(25, 25, A4[0] - 50, A4[1] - 50)  # Marco con 25 pt de margen
                canvas.restoreState()

            doc.build(story, onFirstPage=dibujar_marco, onLaterPages=dibujar_marco)

            abrir_pdf = QMessageBox.question(
                self,
                "PDF generado",
                f"El archivop se gurado como pdf:\n{ruta_archivo}\n\n¿Deseas abrirlo?",
                QMessageBox.Yes | QMessageBox.No,
            )

            if abrir_pdf == QMessageBox.Yes:
                if platform.system() == "Windows":
                    os.startfile(ruta_archivo)
                elif platform.system() == "Darwin":  
                    subprocess.call(["open", ruta_archivo])
                else:
                    subprocess.call(["xdg-open", ruta_archivo])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el PDF:\n{str(e)}")




            



