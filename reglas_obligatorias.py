from qgis.core import QgsProject, QgsSpatialIndex, QgsGeometry, QgsFeatureRequest, QgsPointXY


def obtener_capas_relevantes():
    capas = {}
    nombre_objetivo = {
        "A_Predio", "derecho_interesado_fuente"
    }

    for clave_logica, nombre_real in nombre_objetivo.items():
        capa = QgsProject.instance().mapLayersByName(nombre_real)
        if capa:
            capas[clave_logica] = capa[0]

    return capas

def aplicar_reglas(capas):
    resultados = {}  

    for codigo_regla, funcion_regla in codigos_funciones.items():
        print(f"Ejecutando regla {codigo_regla}...")  
        resultado = funcion_regla(layer_dict=capas)
        resultados[codigo_regla] = resultado

    return resultados


# ----------------------- OBLIGATORIAS -----------------------

def regla_7001(layer_dict=None):
    """El tipo de predio no debe ser null"""
    print(">>> Ejecuntando regla 7001")
    codigo = "7001"
    capa = "A_Predio"
    campo_tipo = "tipo"
    
    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no está cargada en el proyecto."
        }
    
    predio = predios_list[0]
    errores = []

    for feature in predio.getFeatures():
        aid = feature["id_operacion"]
        tipo_predio = feature[campo_tipo]

        if tipo_predio is None or str(tipo_predio).strip() == "":
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_tipo}' no puede ser null o vacío.",
                "capa": capa,
                "regla": codigo
            })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} errores: el tipo de predio no puede ser null." if errores else "No se encontraron errores."
    }

def regla_7002(layer_dict = None):
    """La condición del predio no puede ser null"""
    print(">>> Ejecuntando regla 7002")
    codigo = "7002"
    capa = "A_Predio"
    campo_condicion = "condicion_predio"

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta cargada en el proyecto."
        }
    
    predios = predios_list[0]
    errores = []

    for feutere in predios.getFeatures():
        aid = feutere["id_operacion"]
        condicion_predio = feutere[campo_condicion]

        if condicion_predio is None or str(condicion_predio).strip() == "":
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_condicion}' no puede ser null o vacio.",
                "capa": capa,
                "regla": codigo
            })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} la condición del predio no puede ser null." if errores else "No se encontraron errores."
    }

def regla_7003(layer_dict = None):
    """La destinación económica no debe ser null"""
    print(">>> Ejecuntando regla 7003")
    codigo = "7003"
    capa = "A_Predio"
    campo_destinacion = "destinacion_economica"

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta caragada en el proyecto."
        }
    
    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        destinacion_economica = feature[campo_destinacion]

        if destinacion_economica is None or str(destinacion_economica).strip() == "":
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_destinacion}' no puede se null o vacio",
                "capa": capa,
                "regla": codigo 
            })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores) } la destinacion economica no puede ser null." if errores else "No se encontraron errores."
    }

def regla_7004(layer_dict = None):
    """La fecha  de la visita predial no debe null"""
    print(">>> Ejecutando regla 7004")
    codigo = "7004"
    capa = "A_Predio"
    campo_fecha_vista = "fecha_visita_predial"

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta cargada en el proyecto."
        }
    
    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        fecha_visita = feature[campo_fecha_vista]

        if not fecha_visita:
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_fecha_vista}' no puede ser null o vacio.",
                "capa": capa,
                "regla": codigo
            })
    
    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} la fecha de la visita predial no pude ser null." if errores else "No se encontraron errores."
    }

def regla_7005(layer_dict = None):
    """El resulatdo de la visita al predio no debe ser null"""
    print(">>> Ejecutando regla 7005")
    codigo = "7005"
    capa = "A_Predio"
    campo_resultado = "resultado_visita"

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta cargada en el proyecto."
        }
    
    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        resultado_visita = feature[campo_resultado]

        if resultado_visita is None or str(resultado_visita).strip() == "":
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_resultado}' no puede sel null o vacio.",
                "capa": capa,
                "regla": codigo
            })
    
    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se dectectaron {len(errores)} el resultado de la visita al predio no puede sel null." if errores else "No se encontaron errores."
    }

def regla_7006(layer_dict = None): 
    """el atributo tine área registral del  atributo no debe ser null"""
    print(">>> Ejecutando regla 7006")
    codigo = "7006"
    capa = "A_Predio"
    campo_area = "Area_Registral_m2"

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta cargada en el proyecto."
        }
    
    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        area_registral = feature[campo_area]

        if not area_registral:
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_area}' no puede ser null o vacio.",
                "capa": capa,
                "regla": codigo
            })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} el atributo área registral no puede ser null." if errores else "No se encontraron errores."
    }

def regla_7007(layer_dict =None):
    """el atributo tiene FMI  no debe ser null"""
    print(">>> Ejecutando regla 7007")
    codigo = "7007"
    capa = "A_Predio"
    campo_FMI = "matricula_inmobiliaria"

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta caragda en el proyecto."
        }
    
    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        matricula_inmobiliaria = feature[campo_FMI]

        if not matricula_inmobiliaria:
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_FMI}' no puede ser null o vacio.",
                "capa": capa,
                "regla": codigo
            })

    return {
        "cumple": len(errores) == 0, 
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} el atributo FMI no puede ser null." if errores else "No se encontaron errores."
    }

def regla_7008(layer_dict = None):
    """el tipo de documento de quien atendio la visita no debe se null"""
    print(">>> Ejecutando regla 7008")
    codigo = "7008"
    capa = "A_Predio"
    campo_tipo_documento = "tipo_documento_quien_atendio"

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta cargada en el proyecto."
        }
    
    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        tipo_documento = feature[campo_tipo_documento]

        if not tipo_documento:
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_tipo_documento}' no puede ser null o vacio.",
                "capa": capa,
                "regla": codigo
            })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} el tipo de documento no puede ser null." if errores else "No se encontraron errores."
    }

def regla_7009(layer_dict = None): 
    """el número de documento de quien atendio la visita no debe ser null"""
    print(">>> Ejecuntando regla 7009")
    codigo = "7009"
    capa = "A_Predio"
    campo_numero_documento = "numero_documento_quien_atendio"

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta cargada en el proyecto."
        }
    
    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures ():
        aid = feature["id_operacion"]
        numero_documento = feature[campo_numero_documento]

        if numero_documento is None or str(numero_documento).strip() == "":
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_numero_documento}' no puede ser null o vacio.",
                "capa": capa,
                "regla": codigo
            })
    
    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se dectactoron {len(errores)} el numero de documento no puede ser null." if errores else "No se encontraron errores."
    }


def regla_7010(layer_dict = None):
    """el nombre de quien atendio la visita no debe ser null """
    print(">>> Ejecuntando regla 7010")
    codigo = "7010"
    capa = "A_Predio"
    campo_nombre = "nombres_apellidos_quien_atendio"

    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta cargada en el proyecto."
        }
    
    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        nombres_apellidos = feature[campo_nombre]

        if nombres_apellidos is None or str(nombres_apellidos).strip() == "":
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_nombre}' no puede ser null o vacio.",
                "capa": capa,
                "regla": codigo
            })
    
    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} el nombre de quien atendio la visita no puede ser null." if errores else "No se encontraron errores."
    }


def regla_7011(layer_dict = None):
    """el departamento de residencia del interesado no debe ser null"""
    print(">>> Ejecutando regla 7011")
    codigo = "7011"
    capa = "derecho_interesado_fuente"
    campo_departamento = "ic_departamento"

    derecho_interesado_list = QgsProject.instance().mapLayersByName(capa)

    if not derecho_interesado_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}'no esta cargada en el proyecto."
        }
    
    derecho_interesado = derecho_interesado_list[0]
    errores = []

    for feature in derecho_interesado.getFeatures():
        aid = feature["id_operacion"]
        departamento = feature[campo_departamento]

        if departamento is None or str(departamento).strip() == "":
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_departamento}' no puede ser null o vacio.",
                "capa": capa,
                "regla": codigo
            })

    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se detectaron {len(errores)} el departamento de residencia no puede ser null." if errores else "No se encontraron errores."
    }

def regla_7012(layer_dict = None): 
    """el municipio de residencia del interesado no debe ser null"""
    print(">>> Ejecutando regla 7012")
    codigo = "7012"
    capa = "derecho_interesado_fuente"
    campo_municipio = "ic_municipio"

    derecho_interesdo_list = QgsProject.instance().mapLayersByName(capa)

    if not derecho_interesdo_list:
        return {
            "cumple": False,
            "errores": [],
            "mensaje": f"La capa '{capa}' no esta cargada en el proyecto."
        }
    
    derecho_interesado = derecho_interesdo_list[0]
    errores = []

    for feature in derecho_interesado.getFeatures():
        aid = feature["id_operacion"]
        municipio = feature[campo_municipio]

        if municipio is None or str(municipio).strip() == "":
            errores.append({
                "aid": aid,
                "descripcion": f"El campo '{campo_municipio}' no puede ser null o vacio.",
                "capa": capa,
                "regla": codigo
            })
    
    return {
        "cumple": len(errores) == 0,
        "errores": errores,
        "mensaje": f"Se dectectaron {len(errores)} el municpio de residencia no puede ser null" if errores else "No se dectectaron errores"
    }

codigos_funciones = {
    "7001": regla_7001,
    "7002": regla_7002,
    "7003": regla_7003,
    "7004": regla_7004,
    "7005": regla_7005,
    "7006": regla_7006,
    "7007": regla_7007,
    "7008": regla_7008,
    "7009": regla_7009,
    "7010": regla_7010,
    "7011": regla_7011,
    "7012": regla_7012
}

clases_con_reglas = {
    "El tipo de predio no debe ser null": ["7001"],
    "La condición del predio no puede ser null": ["7002"],
    "La destinación económica no debe ser null": ["7003"],
    "La fecha  de la visita predial no debe null": ["7004"],
    "El resulatdo de la visita al predio no debe ser null": ["7005"],
    "El atributo tine área registral del  atributo no debe ser null": ["7006"],
    "El atributo tiene FMI  no debe ser null": ["7007"],
    "El tipo de documento de quien atendio la visita no debe se null": ["7008"],
    "El número de documento de quien atendio la visita no debe ser null": ["7009"],
    "El nombre de quien atendio la visita no debe ser null": ["7010"],
    "El departamento de residencia del interesado no debe ser null": ["7011"],
    "El municipio de residencia del interesado no debe ser null": ["7012"]
}