from qgis.core import QgsProject, QgsSpatialIndex,  QgsGeometry, QgsFeatureRequest, QgsPointXY

def obtener_capas_relevantes():
    capas = {}
    nombres_objetivo = {        
        "A_Predio"
    }

    for clave_logica, nombre_real in nombres_objetivo.items():
        capa = QgsProject.instance().mapLayersByName(nombre_real)
        if capa:
            capas[clave_logica] = capa[0]
    return capa

def aplicar_reglas(capas):
    resultados = {}

    for codigo_regla, funcion_regla in codigos_funciones.items():
        resultado = funcion_regla(layer_dict = capas)
        resultados[codigo_regla] = resultado
    
    return resultados


# ------------------------ BLOQUE 5000 - CONDICION --------------------

def regla_5001(layer_dict=None):
    """Si la condición es PH matriz la posición 22 del número predial debe ser 9"""
    print(">>> Ejecuntado regla 5001") 
    codigo = "5001"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    PH_matriz = 1

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {"cumple": False, "errores": [], "mensaje": f"La capa '{capa}' no está cargada."}

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == PH_matriz:
            if len(numero_predial) < 22 or numero_predial[21] != "9":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición PH matriz.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }


def regla_5002(layer_dict=None):
    """Si la condición es condominio unidad predial la posición 22 debe ser 8"""
    print(">>> Ejecuntando regka 5002")
    codigo = "5002"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    Condominio_unidad_predial = 2

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {"cumple": False, "errores": [], "mensaje": f"La capa '{capa}' no está cargada."}

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == Condominio_unidad_predial:
            if len(numero_predial) < 22 or numero_predial[21] != "8":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición condominio.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }


def regla_5003(layer_dict=None):
    """Si la condición es bien de uso público, la posición 22 debe ser 3"""
    print(">>> Ejecuntando regla 5003")
    codigo = "5003"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    bien_uso_publico = 3

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {"cumple": False, "errores": [], "mensaje": f"La capa '{capa}' no está cargada."}

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == bien_uso_publico:
            if len(numero_predial) < 22 or numero_predial[21] != "3":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición bien de uso público.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }


def regla_5004 (layer_dict = None):
    """si la condicion es PH unidad predial la posicion 22 del numero predial debe ser 9"""
    print(">>> Ejecuntando regla 5004")
    codigo = "5004"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    PH_unidad_predial = 4

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {
            "cumple": False, 
            "errores": [], 
            "mensaje": f"La capa '{capa}' no está cargada."
            }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == PH_unidad_predial:
            if len(numero_predial) < 22 or numero_predial[21] != "9":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición PH unidad predial.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }

def regla_5005(layer_dict = None):
    """si la condicion es condominio matriz la posicion 22 del numero predial debe ser 8"""
    print(">>> Ejecuntando regla 5005")
    codigo = "5005"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    condominio_matriz = 5

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {
            "cumple": False, 
            "errores": [], 
            "mensaje": f"La capa '{capa}' no está cargada."
            }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == condominio_matriz:
            if len(numero_predial) < 22 or numero_predial[21] != "8":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición condominio matriz.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }

def regla_5006(layer_dict = None):
    """si la condicion es parque cemementerio matriz la posicion 22 del numero predial debe ser 7"""
    print(">>> Ejecuntando regla 5006")
    codigo = "5006"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    parque_cemementerio_matriz = 6

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {
            "cumple": False, 
            "errores": [], 
            "mensaje": f"La capa '{capa}' no está cargada."
            }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == parque_cemementerio_matriz:
            if len(numero_predial) < 22 or numero_predial[21] != "7":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición parque cemementerio matriz.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }

def regla_5007(layer_dict = None):
    """si la condicion es NPH la posiicion 22 del numero predial debe ser 0"""
    print(">>> Ejecuntando regla 5007")
    codigo = "5007"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    NPH = 7

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {
            "cumple": False, 
            "errores": [], 
            "mensaje": f"La capa '{capa}' no está cargada."
            }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == NPH:
            if len(numero_predial) < 22 or numero_predial[21] != "0":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición NPH.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }

def regla_5008(layer_dict = None):
    """si la condicion es informal la posicion 22 del numero predial debe ser 2"""
    print(">>> Ejecutando regla 5008")
    codigo = "5008"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    informal = 8

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {
            "cumple": False, 
            "errores": [], 
            "mensaje": f"La capa '{capa}' no está cargada."
            }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == informal:
            if len(numero_predial) < 22 or numero_predial[21] != "2":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición informal.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }

def regla_5009(layer_dict = None):
    """si la condicion es parque cemementerio unidad predial la posicion 22 del numero predial debe ser 7"""
    print(">>> Ejecuntando regla 5009")
    codigo = "5009"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    parque_cemementerio_unidad_predial = 9

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {
            "cumple": False, 
            "errores": [], 
            "mensaje": f"La capa '{capa}' no está cargada."
            }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == parque_cemementerio_unidad_predial:
            if len(numero_predial) < 22 or numero_predial[21] != "7":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición parque cemementerio unidad predial.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }

def regla_5010(layer_dict = None):
    """si la condicion es via la posicion 22 del numero predial debeb ser 4"""
    print(">>> Ejecutando regla 5010")
    codigo = "5010"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"
    campo_predial = "numero_predial"
    via = 10

    predios_list = QgsProject.instance().mapLayersByName(capa)
    if not predios_list:
        return {
            "cumple": False, 
            "errores": [], 
            "mensaje": f"La capa '{capa}' no está cargada."
            }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = feature[campo_condicion]

        if condicion == via:
            if len(numero_predial) < 22 or numero_predial[21] != "4":
                errores.append({
                    "aid": aid,
                    "descripcion": f"El número predial '{numero_predial}' no coincide con la condición vía.",
                    "capa": capa,
                    "regla": codigo
                })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }

 #------------------------- BLOQUE 6000 - ESTRUCTURA--------------------

def regla_6001(layer_dict=None):
    """La posición 22 a la 30 del número predial no cumple con la estructura esperada para una unidad predial en PH"""
    print(">>> Ejecuntando regla 6001")
    codigo = "6001"
    capa = "A_Predio"
    campo_predial = "numero_predial"
    campo_condicion = "condicion_predio"
    PH_unidad_predial = 4
    PH_matriz = 1 

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta cargada en el proyecto"
        }
    
    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo_predial]).strip()
        condicion = str(feature[campo_condicion]).strip().upper() if feature[campo_condicion] else ""

        if condicion not in [PH_unidad_predial, PH_matriz]:
            continue

        if not numero_predial:
            errores.append({
                "aid": aid,
                "descripcion": "El número predial está vacío o es nulo.",
                "capa": capa,
                "regla": codigo
            })
            continue

        if len(numero_predial) < 30:
            errores.append({
                "aid": aid,
                "descripcion": f"El número predial tiene menos de 30 caracteres: '{numero_predial}'.",
                "capa": capa,
                "regla": codigo
            })
            continue

        if  len(numero_predial) < 30:
            errores.append({
                "aid": id,
                "mensaje": f"El numero predial '{numero_predial}' debe tener al menos 30 caracteres.",
                "capa": capa,
                "regla": codigo
            })

        if numero_predial[21] != "9":
            errores.append({
                "aid": id ,
                "mensaje": f"El número predial '{numero_predial}' no coincide con la condición PH matriz.",
                "capa": capa,
                "regla": codigo
            })
        
        ultimos_8_caracteres = numero_predial[22:30]
        if all ( c == "0" for c in ultimos_8_caracteres):
            errores.append({
                "aid": id,
                "mensaje": f"Los ultimos 8 caracteres del numero predial '{numero_predial}' no pueden ser todos 0 ",
                "capa": capa,
                "regla": codigo
            })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} inconsistencias." if errores else "Sin inconsistencias."
    }


codigos_funciones = {
    "5001": regla_5001,
    "5002": regla_5002,
    "5003": regla_5003,
    "5004": regla_5004,
    "5005": regla_5005,
    "5006": regla_5006,
    "5007": regla_5007,
    "5008": regla_5008,
    "5009": regla_5009,
    "5010": regla_5010,
    "6001": regla_6001, 
}

clases_con_reglas = {
    "La posicion 22 a la 30 del número predial debe coincidir  con la condición del predio": ["5001", "5002", "5003", "5004", "5005", "5006", "5007", "5008", "5009", "5010"],
    "La posición 22 a la 30 del número predial no cumple con la estructura esperada para una unidad predial en PH": ["6001"]
}
