from PyQt5.QtCore import Qt
from qgis.core import QgsProject
from PyQt5.QtGui import QColor
from .import reglas_genericas  
from . import reglas_logicas
from . import reglas_obligatorias

def obtener_capas_dict():
    """ carga las cpas su nombre y devuelve un diccionariocon las capas"""
     
    nombres = [
        "B_Marca_Predial","C_Direccion","D_Unidad_de_Construccion","E_Terreno","A_Predio","adjuntos","derecho_interesado_fuente",
        "registro_fotografico", "caracteristicas_calificacion", "Novedad_Numero_Predial", "Novedad_FMI","adjunto_fuente_admi",
        "adjunto_interesado"
    ]
    
    capas = {}
    for nombre in nombres:
        capa = QgsProject.instance().mapLayersByName(nombre)
        if capa:
            capas[nombre] = capa[0]
    return capas


def validar_todo(tree, boton_validar, iface):
    total_items = tree.topLevelItemCount()
    errores_globales = 0
    resultados = []

    capas = obtener_capas_dict()

    modulos_por_categoria = {
        "Reglas de Calidad Genericas": reglas_genericas,
        "Reglas de Calidad Logicas": reglas_logicas,
        "Reglas de Calidad Obligatorias": reglas_obligatorias,
    }

    for i in range(total_items):
        categoria_item = tree.topLevelItem(i)
        nombre_categoria = categoria_item.text(0)
        modulo = modulos_por_categoria.get(nombre_categoria)

        if modulo:
            for j in range(categoria_item.childCount()):
                sub_item = categoria_item.child(j)
                nombre_subcategoria = sub_item.data(0, Qt.UserRole)
                errores_subcategoria = 0

                if nombre_subcategoria in modulo.clases_con_reglas:
                    codigos = modulo.clases_con_reglas[nombre_subcategoria]
                    for codigo in codigos:
                        funcion = modulo.codigos_funciones.get(codigo)
                        if funcion:
                            try:
                                resultado = funcion(capas)
                                if resultado and not resultado["cumple"]:
                                    for err in resultado.get("errores", []):
                                        resultados.append({
                                            "codigo": f"ERR_{codigo}_{err.get('aid', 'sin_aid')}",
                                            "aid": err.get("aid", "sin_aid"),
                                            "capa": err.get("capa", "sin_capa"),
                                            "regla": codigo,
                                            "descripcion": err.get("descripcion", "Sin descripción")
                                        })
                                    errores_subcategoria += len(resultado["errores"])
                            except Exception as e:
                                iface.messageBar().pushWarning("Error de validación", f"Regla {codigo} falló: {e}")

                if errores_subcategoria == 0:
                    sub_item.setText(1, "✔️")
                    sub_item.setBackground(1, QColor("#96f8bf"))
                else:
                    sub_item.setText(1, f"❌ {errores_subcategoria} errores")
                    sub_item.setBackground(1, QColor( "#ed6657" ))
                    errores_globales += errores_subcategoria
        else:
            for j in range(categoria_item.childCount()):
                sub_item = categoria_item.child(j)
                sub_item.setText(1, "No aplica")
                sub_item.setBackground(1, QColor("#dfd928"))

    if errores_globales == 0:
        boton_validar.setText("100%")
        boton_validar.setStyleSheet("background-color: blue; color: white;")
    else:
        boton_validar.setText("Validar")
        boton_validar.setStyleSheet("")

    iface.messageBar().pushMessage("Validación completa", f"Errores totales encontrados: {errores_globales}", level=0)
    return resultados

def ejecutar_todas_las_reglas():
    resultados = []
    capas = obtener_capas_dict()

    for modulo in [reglas_genericas, reglas_logicas, reglas_obligatorias]:
        for codigo, funcion in modulo.codigos_funciones.items():
            if not callable(funcion):
                continue

            try:
                resultado = funcion(capas)
                descripcion = funcion.__doc__.strip() if funcion.__doc__ else f"Validación de la regla {codigo}"

                resultados.append({
                    "regla": codigo,
                    "descripcion": descripcion,
                    "errores": resultado.get("errores", [])
                })
            except Exception as e:
                resultados.append({
                    "regla": codigo,
                    "descripcion": f"⚠️ Error al ejecutar la regla {codigo}: {str(e)}",
                    "errores": [{"aid": "N/A", "descripcion": str(e), "capa": "desconocida", "regla": codigo}]
                })

    return resultados
