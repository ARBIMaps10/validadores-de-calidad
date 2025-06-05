from qgis.core import QgsProject, QgsSpatialIndex,  QgsGeometry, QgsFeatureRequest, QgsPointXY

def obtener_capas_relevantes():
    capas = {}
    nombres_objetivo = {        
        "B_Marca_Predial","C_Direccion","D_Unidad_de_Construccion","E_Terreno","A_Predio","adjuntos","derecho_interesado_fuente",
        "registro_fotografico", "caracteristicas_calificacion", "Novedad_Numero_Predial", "Novedad_FMI","adjunto_fuente_admi",
        "adjunto_interesado"
    }

    for clave_logica, nombre_real in nombres_objetivo.items():
        capa = QgsProject.instance().mapLayersByName(nombre_real)
        if capa:
            capas[clave_logica] = capa[0]
    return capas

def aplicar_reglas(capas):
    resultados = {}

    for codigo_regla, funcion_regla in codigos_funciones.items():
        resultado = funcion_regla(layer_dict = capas)
        resultados[codigo_regla] = resultado
    
    return resultados

# ------------------------------- BLOQUE 1000 - PUNTOS -------------------------------

def regla_1001(layer_dict):
    """Los Puntos de Lindero no deben superponerse"""
    print(">>> Ejecutando la regla 1001")
    codigo = "1001"
    nombre_capa = "B_Marca_Predial"
    layer = layer_dict.get(nombre_capa)
    if not layer:
        return {'cumple': True, 'errores': [], 'mensaje': f"Regla {codigo} omitida: capa '{nombre_capa}' no disponible."}
    index = QgsSpatialIndex(layer.getFeatures())
    errores = []
    for f in layer.getFeatures():
        geom = f.geometry()
        ids = index.intersects(geom.boundingBox())
        ids = [i for i in ids if i != f.id()]
        for i in ids:
            if geom.equals(layer.getFeature(i).geometry()):
                errores.append({
                    "aid": f["id_operacion"] if "id_operacion" in f.fields().names() else str(f.id()),
                    "descripcion": "Punto de Lindero se superpone con otro punto.",
                    "capa": nombre_capa,
                    "regla": codigo 
                })
                break
    return {
        'cumple': len(errores) == 0, 
        'errores': errores, 
        'mensaje': f"Regla {codigo} ejecutada: {len(errores)} superposiciones encontradas." if errores else "No hay superposiciones."
        }

def regla_1002(layer_dict):# las capas no se encuentran en el proyecto
    """Los Puntos de Control no deben superponerse"""
    print(">>> Ejecutando la regla 1002")
    codigo = "1002"
    nombre_capa = "PuntosDeControl"
    layer = layer_dict.get(nombre_capa)
    if not layer:
        return {
            'cumple': True,
            'errores': [],
            'mensaje': f"Regla {codigo} omitida: capa '{nombre_capa}' no disponible."
        }

    index = QgsSpatialIndex(layer.getFeatures())
    errores = []

    for f in layer.getFeatures():
        geom = f.geometry()
        ids = index.intersects(geom.boundingBox())
        ids = [i for i in ids if i != f.id()]
        if ids:
            errores.append({
                "aid": f["AID"] if "AID" in f.fields().names() else str(f.id()),
                "descripcion": "Punto de Control se superpone con otro punto.",
                "capa": nombre_capa,
                "regla": codigo 
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Regla {codigo} ejecutada: {len(errores)} superposiciones encontradas." if errores else "No hay superposiciones."
    }


def regla_1003(layer_dict):
    """Los Puntos de Lindero deben estar cubiertos por nodos de Lindero"""
    print(">>> Ejecutando laregla 1003")
    codigo = "1003"
    capa_puntos = "B_Marca_Predial"
    capa_nodos = "B_Marca_Predial"
    puntos = layer_dict.get(capa_puntos)
    nodos = layer_dict.get(capa_nodos)
    if not puntos or not nodos:
        return {'cumple': True, 'errores': [], 'mensaje': f"Regla {codigo} omitida: capas '{capa_puntos}' o '{capa_nodos}' no disponibles."}
    errores = []
    for punto in puntos.getFeatures():
        punto_geom = punto.geometry()
        cubierto = False
        for nodo in nodos.getFeatures():
            if punto.id() == nodo.id():
                continue
            if punto_geom.equals(nodo.geometry()):
                cubierto = True
                break
        if not cubierto:
            errores.append({
                "aid": punto["id_operacion"] if "id_operacion" in punto.fields().names() else str(punto.id()),
                "descripcion": "Punto de Lindero no está cubierto por otro nodo.",
                "capa": capa_puntos,
                "regla": codigo 
            })
    return {
        'cumple': len(errores) == 0, 
        'errores': errores, 
        'mensaje': f"Regla {codigo} ejecutada correctamente."
        }

def regla_1004(layer_dict):
    """Los Puntos de Lindero deben estar cubiertos por nodos de Terreno"""
    print(">>> Ejecutando la regla 1004")
    codigo = "1004"
    capa_puntos = "B_Marca_Predial"
    capa_nodos = "B_Marca_Predial"
    puntos = layer_dict.get(capa_puntos)
    nodos = layer_dict.get(capa_nodos)
    if not puntos or not nodos:
        return {'cumple': True, 'errores': [], 'mensaje': f"Regla {codigo} omitida: capas no disponibles."}
    errores = []
    for punto in puntos.getFeatures():
        punto_geom = punto.geometry()
        cubierto = any(
            punto.id() != nodo.id() and punto_geom.equals(nodo.geometry())
            for nodo in nodos.getFeatures()
        )
        if not cubierto:
            errores.append({
                "aid": punto["id_operacion"] if "id_operacion" in punto.fields().names() else str(punto.id()),
                "descripcion": "Punto de Lindero no está cubierto por nodo de terreno.",
                "capa": capa_puntos,
                "regla": codigo 
            })
    return {'cumple': len(errores) == 0, 
            'errores': errores,
            'mensaje': f"{len(errores)} puntos no cubiertos." if errores else "Todos los puntos cubiertos."
            }

    
# ------------------------------- BLOQUE 2000 - LÍNEAS -------------------------------

def regla_2001(layer_dict):
    """Los Linderos no deben superponerse"""
    print(">>> Ejecutando la regla 2001")
    codigo = "2001"
    nombre_capa = "E_Terreno"
    layer = layer_dict.get(nombre_capa)
    if not layer:
        return {'cumple': True, 'errores': [], 'mensaje': f"Regla {codigo} omitida: capa '{nombre_capa}' no disponible."}
    index = QgsSpatialIndex(layer.getFeatures())
    errores = []
    for f in layer.getFeatures():
        geom = f.geometry()
        if geom.type() != 1:  # Sólo líneas
            continue
        ids = index.intersects(geom.boundingBox())
        ids = [i for i in ids if i != f.id()]
        for i in ids:
            if geom.equals(layer.getFeature(i).geometry()):
                errores.append({
                    "aid": f["id_operacion"] if "id_operacion" in f.fields().names() else str(f.id()),
                    "descripcion": "Lindero se superpone con otro lindero.",
                    "capa": nombre_capa,
                    "regla": codigo 
                })
                break
    return {
        'cumple': len(errores) == 0, 
        'errores': errores, 
        'mensaje': f"Regla {codigo} ejecutada correctamente."
        }

def regla_2002(layer_dict): #las capas no se encuentran en el proyecto
    """Los Linderos deben terminar en cambio de colindancia"""
    print(">>> Ejecutando la regla 2002")
    codigo = "2002"
    nombre_capa = "Linderos"
    layer = layer_dict.get(nombre_capa)

    if not layer:
        return {
            'cumple': True,
            'errores': [],
            'mensaje': f"Regla {codigo} omitida: capa '{nombre_capa}' no disponible."
        }

    index = QgsSpatialIndex(layer.getFeatures())
    errores = []

    for f in layer.getFeatures():
        geom = f.geometry()
        if geom.isMultipart():
            lineas = geom.asMultiPolyline()
        else:
            lineas = [geom.asPolyline()]
        
        for linea in lineas:
            if not linea:
                continue

            extremos = [QgsPointXY(linea[0]), QgsPointXY(linea[-1])]
            nodos_conectados = 0

            for extremo in extremos:
                punto_geom = QgsGeometry.fromPointXY(extremo)
                bbox = punto_geom.buffer(0.1, 5).boundingBox()
                posibles_ids = index.intersects(bbox)

                conectado = False
                for fid in posibles_ids:
                    if fid == f.id():
                        continue
                    otro = layer.getFeature(fid)
                    if otro.geometry().intersects(punto_geom):
                        conectado = True
                        break

                if conectado:
                    nodos_conectados += 1

            if nodos_conectados < 2:
                errores.append({
                    "aid": f["AID"] if "AID" in f.fields().names() else str(f.id()),
                    "descripcion": f"Lindero no termina correctamente en cambio de colindancia (conexiones: {nodos_conectados}/2).",
                    "capa": nombre_capa,
                    "regla": codigo 
                })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Regla {codigo} ejecutada: {len(errores)} linderos no terminan correctamente." if errores else "Todos los linderos terminan correctamente."
    }



def regla_2003(layer_dict): 
    """Los Linderos deben estar cubiertos por límites de Terrenos"""
    print(">>> Ejecutando la regla 2003")
    codigo = "2003"
    capa_linderos = "E_Terreno"
    capa_terrenos = "E_Terreno"
    linderos = layer_dict.get(capa_linderos)
    terrenos = layer_dict.get(capa_terrenos)
    if not linderos or not terrenos:
        return {'cumple': True, 'errores': [], 'mensaje': f"Regla {codigo} omitida: capas no disponibles."}
    errores = []
    for lindero in linderos.getFeatures():
        if lindero.geometry().type() != 1:  # tipo línea
            continue
        cubierto = any(
            lindero.geometry().within(terreno.geometry())
            for terreno in terrenos.getFeatures()
        )
        if not cubierto:
            errores.append({
                "aid": lindero["id_operacion"] if "id_operacion" in lindero.fields().names() else str(lindero.id()),
                "descripcion": "Lindero no está cubierto por los límites de Terreno.",
                "capa": capa_linderos,
                "regla": codigo 
            })
    return {'cumple': len(errores) == 0, 
            'errores': errores,
            'mensaje': f"{len(errores)} linderos no cubiertos." if errores else "Todos cubiertos."
            }


def regla_2004(layer_dict): 
    """Los nodos de Lindero deben estar cubiertos por Puntos de Lindero"""
    print(">>> Ejecutando la regla 2004")
    codigo = "2004"
    capa_nodos = "B_Marca_Predial"
    capa_puntos = "B_Marca_Predial"
    nodos = layer_dict.get(capa_nodos)
    puntos = layer_dict.get(capa_puntos)
    if not nodos or not puntos:
        return {'cumple': True, 'errores': [], 'mensaje': f"Regla {codigo} omitida: capas no disponibles."}
    errores = []
    for nodo in nodos.getFeatures():
        nodo_geom = nodo.geometry()
        cubierto = any(
            nodo.id() != punto.id() and nodo_geom.equals(punto.geometry())
            for punto in puntos.getFeatures()
        )
        if not cubierto:
            errores.append({
                "aid": nodo["id_operacion"] if "id_operacion" in nodo.fields().names() else str(nodo.id()),
                "descripcion": "Nodo de Lindero no está cubierto por un Punto de Lindero.",
                "capa": capa_nodos,
                "regla": codigo 
            })
    return {'cumple': len(errores) == 0, 
            'errores': errores,
            'mensaje': f"{len(errores)} nodos no cubiertos." if errores else "Todos los nodos están cubiertos."
            }


def regla_2005(layer_dict): 
    """Los Linderos no deben tener nodos sin conectar"""
    print(">>> Ejecutando la regla 2005")
    codigo = "2005"
    nombre_capa = "E_Terreno"
    layer = layer_dict.get(nombre_capa)
    if not layer:
        return {'cumple': True, 'errores': [], 'mensaje': f"Regla {codigo} omitida: capa no disponible."}
    errores = []
    for f in layer.getFeatures():
        if f.geometry().type() != 1:  # solo líneas
            continue
        if not f.geometry().isGeosValid():
            errores.append({
                "aid": f["id_operacion"] if "id_operacion" in f.fields().names() else str(f.id()),
                "descripcion": "Lindero tiene nodos sin conectar (geometría inválida).",
                "capa": nombre_capa,
                "regla": codigo 
            })
    return {'cumple': len(errores) == 0, 
            'errores': errores,
            'mensaje': f"{len(errores)} linderos con geometría inválida." if errores else "Todos los linderos válidos."
            }


# ------------------------------- BLOQUE 3000 - GEOMÉTRICAS --------------------------

def regla_3001(layer_dict=None):
    """Los Terrenos no deben superponerse"""
    print(">>> Ejecutando la regla 3001")
    codigo = "3001"
    nombre_capa = "E_Terreno"
    capa = QgsProject.instance().mapLayersByName(nombre_capa)
    if not capa:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{nombre_capa}' no está cargada en el proyecto."
        }

    layer = capa[0]
    index = QgsSpatialIndex(layer.getFeatures())
    errores = []

    for feature in layer.getFeatures():
        geom = feature.geometry()
        aid = feature["etiqueta"]
        posibles_ids = index.intersects(geom.boundingBox())

        for fid in posibles_ids:
            if fid == feature.id():
                continue
            other_feat = layer.getFeature(fid)
            if geom.intersects(other_feat.geometry()):
                errores.append({
                    "aid": aid,
                    "descripcion": f"El terreno con código predial {aid} se superpone con otro terreno.",
                    "capa": nombre_capa,
                    "regla": codigo 
                })
                break

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se detectaron {len(errores)} terrenos superpuestos." if errores else "Los terrenos no se superponen."
    }


def regla_3002(layer_dict=None):
    """Las Construcciones no deben superponerse"""
    print(">>> Ejecutando la regla 3002")
    codigo = "3002"
    nombre_capa = "D_Unidad_de_Construccion"
    capa = QgsProject.instance().mapLayersByName(nombre_capa)
    if not capa:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{nombre_capa}' no está cargada en el proyecto."
        }

    layer = capa[0]
    index = QgsSpatialIndex(layer.getFeatures())
    errores = []

    for feature in layer.getFeatures():
        geom = feature.geometry()
        aid = feature["id_operacion"]
        posibles_ids = index.intersects(geom.boundingBox())

        for fid in posibles_ids:
            if fid == feature.id():
                continue
            other_feat = layer.getFeature(fid)
            if geom.intersects(other_feat.geometry()):
                errores.append({
                    "aid": aid,
                    "descripcion": f"La construcción con código predial {aid} se superpone con otra construcción.",
                    "capa": nombre_capa,
                    "regla": codigo 
                })
                break

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se detectaron {len(errores)} construcciones superpuestas." if errores else "Las construcciones no se superponen."
    }


def regla_3003(layer_dict=None):
    """Las Servidumbres de Tránsito no deben superponerse"""
    print(">>> Ejecutando la regla 3003")
    codigo = "3003"
    nombre_capa = "E_Terreno"
    capa = QgsProject.instance().mapLayersByName(nombre_capa)
    if not capa:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{nombre_capa}' no está cargada en el proyecto."
        }

    layer = capa[0]
    index = QgsSpatialIndex(layer.getFeatures())
    errores = []

    for feature in layer.getFeatures():
        geom = feature.geometry()
        aid = feature["etiqueta"]
        posibles_ids = index.intersects(geom.boundingBox())

        for fid in posibles_ids:
            if fid == feature.id():
                continue
            other_feat = layer.getFeature(fid)
            if geom.intersects(other_feat.geometry()):
                errores.append({
                    "aid": aid,
                    "descripcion": f"La servidumbre con código predial {aid} se superpone con otra servidumbre.",
                    "capa": nombre_capa,
                    "regla": codigo 
                })
                break

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se detectaron {len(errores)} servidumbres superpuestas." if errores else "Las servidumbres no se superponen."
    }


def regla_3004(layer_dict=None):
    """Los límites de Terreno deben estar cubiertos por Linderos"""
    print(">>> Ejecutando la regla 3004")
    codigo = "3004"
    nombre_capa = "E_Terreno"
    capa = QgsProject.instance().mapLayersByName(nombre_capa)
    if not capa:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{nombre_capa}' no está cargada en el proyecto."
        }

    layer = capa[0]
    index = QgsSpatialIndex(layer.getFeatures())
    errores = []

    for feuture in layer.getFeatures():
        geom = feuture.geometry()
        aid = feuture["etiqueta"]
        posibles_ids = index.intersects(geom.boundingBox())

        for fid in posibles_ids:
            if fid == feuture.id():
                continue
            other_feat = layer.getFeature(fid)
            if geom.intersects(other_feat.geometry()):
                errores.append({
                    "aid": aid,
                    "descripcion": f"El límite de terreno con código predial {aid} no está cubierto por un lindero.",
                    "capa": nombre_capa,
                    "regla": codigo 
                })
                break

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se detectaron {len(errores)} límites de terreno no cubiertos por linderos." if errores else "Los límites de terreno están cubiertos por linderos."
    }


def regla_3005(layer_dict=None):
    """Las Servidumbres de Tránsito no se deben superponer con Construcciones"""
    print(">>> Ejecutando la regla 3005")
    codigo = "3005"
    capa_terreno = "E_Terreno"
    capa_construccion = "D_Unidad_de_Construccion"

    terrenos_list = QgsProject.instance().mapLayersByName(capa_terreno)
    construcciones_list = QgsProject.instance().mapLayersByName(capa_construccion)

    if not terrenos_list or not construcciones_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"Las capas '{capa_terreno}' o '{capa_construccion}' no están cargadas en el proyecto."
        }

    terrenos = terrenos_list[0]
    construcciones = construcciones_list[0]
    index_construcciones = QgsSpatialIndex(construcciones.getFeatures())

    errores = []

    for terreno in terrenos.getFeatures():
        geom_terreno = terreno.geometry()
        aid = terreno["etiqueta"]
        posibles_ids = index_construcciones.intersects(geom_terreno.boundingBox())

        for fid in posibles_ids:
            construccion = construcciones.getFeature(fid)
            if geom_terreno.intersects(construccion.geometry()):
                errores.append({
                    "aid": aid,
                    "descripcion": f"El terreno con código predial {aid} se superpone con una construcción.",
                    "capa": capa_terreno,
                    "regla": codigo 
                })
                break

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se detectaron {len(errores)} servidumbres superpuestas con construcciones." if errores else "No hay superposiciones con construcciones."
    }


def regla_3006(layer_dict=None):
    """No deben haber huecos entre Terrenos"""
    print(">>> Ejecutando la regla 3006")
    codigo = "3006"
    nombre_capa = "E_Terreno"
    terrenos_list = QgsProject.instance().mapLayersByName(nombre_capa)
    if not terrenos_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{nombre_capa}' no está cargada en el proyecto."
        }

    layer = terrenos_list[0]
    geometria_total = None

    for feature in layer.getFeatures():
        geom = feature.geometry()
        if geometria_total is None:
            geometria_total = QgsGeometry(geom)
        else:
            geometria_total = geometria_total.combine(geom)

    errores = []
    if geometria_total and geometria_total.isGeosValid():
        if geometria_total.isMultipart():
            multipoligono = geometria_total.asMultiPolygon()
        else:
            multipoligono = [geometria_total.asPolygon()]

        for parte in multipoligono:
            if len(parte) > 1:
                for ring in parte[1:]:
                    errores.append({
                        "aid": "sin_id",
                        "descripcion": "Se detectó un hueco entre terrenos.",
                        "capa": nombre_capa,
                        "regla": codigo 
                    })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se detectaron {len(errores)} huecos entre terrenos." if errores else "No hay huecos entre terrenos."
    }


def regla_3007(layer_dict=None):
    """Las servidumbres de Tránsito no deben tener geometrías multiparte"""
    print(">>> Ejecutando la regla 3007")
    codigo = "3007"
    nombre_capa = "E_Terreno"  
    capa = QgsProject.instance().mapLayersByName(nombre_capa)
    if not capa:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{nombre_capa}' no está cargada en el proyecto."
        }

    layer = capa[0]
    errores = []

    for feature in layer.getFeatures():
        geom = feature.geometry()
        aid = feature["etiqueta"]

        if geom.isMultipart():
            errores.append({
                "aid": aid,
                "descripcion": f"La servidumbre con código predial {aid} tiene geometría multiparte.",
                "capa": nombre_capa,
                "regla": codigo 
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se detectaron {len(errores)} servidumbres con geometrías multiparte." if errores else "No hay geometrías multiparte."
    }


def regla_3008(layer_dict=None):
    """Los nodos de Terrenos deben estar cubiertos por Puntos de Lindero"""
    print(">>> Ejecutando la regla 3008")
    codigo = "3008"
    capa_terrenos = "E_Terreno"
    capa_marcas = "B_Marca_Predial"
    terrenos_list = QgsProject.instance().mapLayersByName(capa_terrenos)
    marcas_list = QgsProject.instance().mapLayersByName(capa_marcas)

    if not terrenos_list or not marcas_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"Las capas '{capa_terrenos}' o '{capa_marcas}' no están cargadas en el proyecto."
        }

    terrenos = terrenos_list[0]
    marcas = marcas_list[0]
    index_marcas = QgsSpatialIndex(marcas.getFeatures())
    tolerancia = 0.2
    errores = []

    for terreno in terrenos.getFeatures():
        geom = terreno.geometry()
        aid = terreno["etiqueta"]
        for punto in geom.vertices():
            punto_xy = QgsPointXY(punto)
            bbox = QgsGeometry.fromPointXY(punto_xy).buffer(tolerancia, 5).boundingBox()
            posibles = index_marcas.intersects(bbox)

            if not any(
                marcas.getFeature(fid).geometry().distance(QgsGeometry.fromPointXY(punto_xy)) <= tolerancia
                for fid in posibles
            ):
                errores.append({
                    "aid": aid,
                    "descripcion": f"El nodo {punto_xy} del terreno con código predial {aid} no tiene punto de lindero cercano.",
                    "capa": capa_terrenos,
                    "regla": codigo 
                })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se encontraron {len(errores)} nodos de terreno sin punto de lindero." if errores else "Todos los nodos tienen punto cercano."
    }


def regla_3009(layer_dict=None):
    """Las Construcciones deben estar dentro de su Terreno correspondiente"""
    print(">>> Ejecutando la regla 3009")
    codigo = "3009"
    capa_construcciones = "D_Unidad_de_Construccion"
    capa_terrenos = "E_Terreno"

    construcciones_list = QgsProject.instance().mapLayersByName(capa_construcciones)
    terrenos_list = QgsProject.instance().mapLayersByName(capa_terrenos)

    if not construcciones_list or not terrenos_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"Las capas '{capa_construcciones}' o '{capa_terrenos}' no están cargadas en el proyecto."
        }

    construcciones = construcciones_list[0]
    terrenos = terrenos_list[0]
    index = QgsSpatialIndex(terrenos.getFeatures())
    errores = []

    for construccion in construcciones.getFeatures():
        geom_c = construccion.geometry()
        aid = construccion["id_operacion"]
        posibles = index.intersects(geom_c.boundingBox())

        if not any(terrenos.getFeature(fid).geometry().contains(geom_c) for fid in posibles):
            errores.append({
                "aid": aid,
                "descripcion": f"La construcción con código predial {aid} no está contenida dentro de ningún terreno.",
                "capa": capa_construcciones,
                "regla": codigo 
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se encontraron {len(errores)} construcciones fuera de su terreno." if errores else "Todas las construcciones están correctamente contenidas."
    }


def regla_3010(layer_dict=None):
    """Las Unidades de Construcción deben estar dentro de sus Terrenos correspondientes"""
    print(">>> Ejecutando la regla 3010")
    codigo = "3010"
    capa_unidades = "D_Unidad_de_Construccion"
    capa_terrenos = "E_Terreno"

    unidades_list = QgsProject.instance().mapLayersByName(capa_unidades)
    terrenos_list = QgsProject.instance().mapLayersByName(capa_terrenos)

    if not unidades_list or not terrenos_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"Las capas '{capa_unidades}' o '{capa_terrenos}' no están cargadas en el proyecto."
        }

    unidades = unidades_list[0]
    terrenos = terrenos_list[0]
    index = QgsSpatialIndex(terrenos.getFeatures())
    errores = []

    for unidad in unidades.getFeatures():
        geom_u = unidad.geometry()
        aid = unidad["id_operacion"]
        posibles = index.intersects(geom_u.boundingBox())

        if not any(terrenos.getFeature(fid).geometry().contains(geom_u) for fid in posibles):
            errores.append({
                "aid": aid,
                "descripcion": f"La unidad de construcción con código predial {aid} no está contenida dentro de ningún terreno.",
                "capa": capa_unidades,
                "regla": codigo 
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se encontraron {len(errores)} unidades fuera de sus terrenos." if errores else "Todas las unidades están correctamente contenidas."
    }


def regla_3011(layer_dict=None):
    """Las Unidades de Construcción deben estar dentro de sus Construcciones correspondientes"""
    print(">>> Ejecutando la regla 3011")
    codigo = "3011"
    nombre_capa = "D_Unidad_de_Construccion"
    unidades_list = QgsProject.instance().mapLayersByName(nombre_capa)
    if not unidades_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{nombre_capa}' no está cargada en el proyecto."
        }

    capa = unidades_list[0]
    index = QgsSpatialIndex(capa.getFeatures())
    errores = []

    for unidad in capa.getFeatures():
        aid = unidad["id_operacion"]
        geom_u = unidad.geometry()
        posibles = index.intersects(geom_u.boundingBox())

        contenido = False
        for fid in posibles:
            if fid == unidad.id():
                continue
            otra = capa.getFeature(fid)
            if otra.geometry().contains(geom_u):
                contenido = True
                break

        if not contenido:
            errores.append({
                "aid": aid,
                "descripcion": f"La unidad de construcción con código predial {aid} no está contenida dentro de ninguna otra construcción.",
                "capa": nombre_capa,
                "regla": codigo 
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se encontraron {len(errores)} unidades fuera de sus construcciones." if errores else "Todas las unidades están contenidas."
    }

# ------------------------------- BLOQUE 4000 - LOGICAS --------------------------

def regla_4001(layer_dict=None):
    """Los Predios deben tener Derecho asociado y pueden tener máximo un Derecho de tipo Dominio asociado"""
    print(">>> Ejecutando la reagla 4001")
    codigo = "4001"
    capa_predios = "A_Predio"
    capa_derechos = "derecho_interesado_fuente"
    
    predios_list = QgsProject.instance().mapLayersByName(capa_predios)
    derechos_list = QgsProject.instance().mapLayersByName(capa_derechos)
    
    if not predios_list or not derechos_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"Las capas '{capa_predios}' o '{capa_derechos}' no están cargadas en el proyecto."
        }

    predios = predios_list[0]
    derechos = derechos_list[0]

    derechos_por_predio = {}
    for d in derechos.getFeatures():
        predio_id = d['id_operacion']  
        tipo = d['tipo derecho']    
        if predio_id not in derechos_por_predio:
            derechos_por_predio[predio_id] = []
        derechos_por_predio[predio_id].append(tipo)

    errores = []
    for predio in predios.getFeatures():
        aid = predio['id_operacion']  
        tipos = derechos_por_predio.get(aid, [])
        if not tipos:
            errores.append({
                "aid": aid,
                "descripcion": f"El predio {aid} no tiene derechos asociados.",
                "capa": capa_predios,
                "regla": codigo
            })
        elif tipos.count('Dominio') > 1:
            errores.append({
                "aid": aid,
                "descripcion": f"El predio {aid} tiene más de un derecho de tipo Dominio.",
                "capa": capa_predios,
                "regla": codigo
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': f"Se detectaron {len(errores)} predios con errores de derechos." if errores else "Todos los predios cumplen con los derechos requeridos."
    }

def regla_4002(layer_dict=None): 
    """Las fracciones de las Agrupaciones de Interesados deben sumar uno (1)"""

def regla_4003(layer_dict=None):
    """Revisar que el campo departamento de la tabla Predio tiene dos caracteres numéricos"""
    print (">>>∟Ejecutando la regla 4003")
    codigo = "4003"
    capa = "A_Predio"
    campo = "Numero predial"
    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{capa}' no está cargada en el proyecto."
        }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]  
        numero_predial = str(feature[campo]).strip()

        if len(numero_predial) < 2 or not numero_predial[:2].isdigit():
            errores.append({
                "aid": aid,
                "descripcion": f"El predio con AID {aid} tiene un número predial cuyo código de departamento ('{numero_predial}') no es válido (deben ser 2 dígitos numéricos).",
                "capa": capa,
                "regla": codigo
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': (
            f"Se detectaron {len(errores)} predios con código de departamento no numérico en el número predial."
            if errores else "Todos los códigos de departamento en el número predial son válidos."
        )
    }

def regla_4004(layer_dict=None): 
    """Revisar que el campo municipio de la tabla Predio tiene tres caracteres numéricos"""
    print(">>> Ejecutando la regla 4004")
    codigo = "4004"
    capa = "A_Predio"
    campo = "Numero predial"
    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{capa}' no está cargada en el proyecto."
        }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo]).strip()

        municipio = numero_predial[2:5]  

        if len(municipio) != 3 or not municipio.isdigit():
            errores.append({
                "aid": aid,
                "descripcion": f"El predio con AID {aid} tiene un número predial cuyo código de de municipio ('{municipio}') no es válido (deben ser 3 dígitos numéricos).",
                "capa": capa,
                "regla": codigo
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': (
            f"Se detectaron {len(errores)} predios con código de municipio no numérico en el número predial."
            if errores else "Todos los códigos de municipio en el número predial son válidos."
        )

    }

def regla_4005(layer_dict=None): 
    """Revisar que el número predial tiene 30 caracteres numéricos"""
    print(">>> Ejecutando la regla 4005")
    codigo = "4005"
    capa = "A_Predio"
    campo = "Numero predial"
    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{capa}' no está cargada en el proyecto."
        }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_predial = str(feature[campo]).strip()

        if len(numero_predial) != 30 or not numero_predial.isdigit():
            errores.append({
                "aid": aid,
                "descripcion": (
                    f"El predio con AID {aid} tiene un número predial inválido ('{numero_predial}'): "
                    f"debe tener exactamente 30 caracteres numéricos."
                ),
                "capa": capa,
                "regla": codigo
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': (
            f"Se detectaron {len(errores)} predios con número predial que no cumple con los 30 caracteres numéricos."
            if errores else "Todos los números prediales tienen exactamente 30 caracteres numéricos válidos."
        )
    }

def regla_4006(layer_dict=None): 
    """Revisar que el número predial anterior tiene 20 caracteres numéricos"""
    print(">>> Ejecutando la regla 4006")
    codigo = "4006"
    capa = "A_Predio"
    campo = "Numero predial anterior"
    predios_list = QgsProject.instance().mapLayersByName(capa)

    if not predios_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{capa}' no está cargada en el proyecto."
        }

    predios = predios_list[0]
    errores = []

    for feature in predios.getFeatures():
        aid = feature["id_operacion"]
        numero_anterior = str(feature[campo]).strip()

        if len(numero_anterior) != 20 or not numero_anterior.isdigit():
            errores.append({
                "aid": aid,
                "descripcion": (
                    f"El predio con AID {aid} tiene un número predial anterior inválido ('{numero_anterior}'): "
                    f"debe tener exactamente 20 caracteres numéricos."
                ),
                "capa": capa,
                "regla": codigo
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': (
            f"Se detectaron {len(errores)} predios con número predial anterior inválido "
            f"(no cumple con los 20 caracteres numéricos)."
            if errores else "Todos los números prediales anteriores tienen exactamente 20 caracteres numéricos válidos."
        )
    }

def regla_4007(layer_dict=None):
    """Revisar que los interesados naturales no incluyan datos de interesados jurídicos"""
    print(">>> Ejecutando la regla 4007")
    codigo = "4007"
    capa = "derecho_interesado_fuente"
    campo_tipo = "i_tipo"  
    campo_doc = "i_tipo_documento"
    campo_razon = "i_razon_social"
    campos_obligatorios = ["i_primer_nombre", "i_primer_apellido", "i_sexo"]
    TIPO_PERSONA_NATURAL = 2 
  

    interesados_list = QgsProject.instance().mapLayersByName(capa)
    if not interesados_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{capa}' no está cargada en el proyecto."
        }

    interesados = interesados_list[0]
    errores = []

    for feature in interesados.getFeatures():
        try:
            aid = feature["id_operacion"]
            tipo_persona = feature[campo_tipo]

            if tipo_persona != TIPO_PERSONA_NATURAL:
                continue

            descripcion = []

            
            tipo_documento = str(feature[campo_doc]).strip().upper()
            if tipo_documento == "NIT":
                descripcion.append("tipo de documento inválido (NIT no permitido para personas naturales)")

       
            razon_social = feature[campo_razon]
            if razon_social and str(razon_social).strip() != "":
                descripcion.append("razón social no permitida para personas naturales")

            
            campos_faltantes = [
                campo for campo in campos_obligatorios
                if not feature[campo] or str(feature[campo]).strip() == ""
            ]
            if campos_faltantes:
                descripcion.append("campos obligatorios vacíos: " + ", ".join(campos_faltantes))

            
            if descripcion:
                errores.append({
                    "aid": aid,
                    "descripcion": f"El interesado es Persona_Natural pero presenta: " + "; ".join(descripcion),
                    "capa": capa,
                    "regla": codigo
                })

        except Exception as e:
            errores.append({
                "aid": "sin_id",
                "descripcion": f"Error al procesar el interesado: {str(e)}",
                "capa": capa,
                "regla": codigo
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': (
            f"Se detectaron {len(errores)} personas naturales con datos inválidos."
            if errores else "Todas las personas naturales están correctamente registradas."
        )
    }

          
def regla_4008(layer_dict=None):
    """Revisar que los interesados jurídicos no incluyan datos de interesados naturales"""
    print(">>> Ejecutando la regla 4008")
    codigo = "4008"
    capa = "derecho_interesado_fuente"
    campo_tipo = "i_tipo"
    campo_doc = "i_tipo_documento"
    campo_razon = "i_razon_social"
    campos_naturales = ["i_primer_nombre", "i_primer_apellido", "i_sexo"]
    TIPO_PERSONA_JURIDICA = 1

    interesados_list = QgsProject.instance().mapLayersByName(capa)
    if not interesados_list:
        return {
            'cumple': False,
            'errores': [],
            'mensaje': f"La capa '{capa}' no está cargada en el proyecto."
        }

    interesados = interesados_list[0]
    errores = []

    for feature in interesados.getFeatures():
        try:
            aid = feature["id_operacion"]
            tipo_persona = feature[campo_tipo]

            if tipo_persona != TIPO_PERSONA_JURIDICA:
                continue

            descripcion = []

            tipo_documento = str(feature[campo_doc]).strip().upper()
            if tipo_documento != "NIT":
                descripcion.append(f"tipo de documento inválido ('{tipo_documento}', debe ser 'NIT')")

            razon_social = feature[campo_razon]
            if not razon_social or str(razon_social).strip() == "":
                descripcion.append("razón social vacía")

            naturales_llenos = [
                campo for campo in campos_naturales
                if feature[campo] and str(feature[campo]).strip() != ""
            ]
            if naturales_llenos:
                descripcion.append("campos de persona natural llenos: " + ", ".join(naturales_llenos))

            if descripcion:
                errores.append({
                    "aid": aid,
                    "descripcion": f"El interesado es Persona_Juridica pero presenta: " + "; ".join(descripcion),
                    "capa": capa,
                    "regla": codigo
                })

        except Exception as e:
            errores.append({
                "aid": "sin_id",
                "descripcion": f"Error al procesar el interesado: {str(e)}",
                "capa": capa,
                "regla": codigo
            })

    return {
        'cumple': len(errores) == 0,
        'errores': errores,
        'mensaje': (
            f"Se detectaron {len(errores)} personas jurídicas con datos inválidos."
            if errores else "Todas las personas jurídicas tienen datos válidos."
        )
    }

def regla_4009(layer_dict=None): # reisar sise va a dejar o se va a eliminar
    """, Revisar que el tipo de Predio corresponde a la posición 22 del número predial"""

def regla_4010(layer_dict=None):#revisar porque no se entiende vien a lo que refiere,
    """Revisar que las Unidades Espaciales asociadas a Predios correspondan al tipo de Predio"""

def regla_4011(layer_dict=None):
    """Punto Lindero no debe tener registros duplicados"""

def regla_4012(layer_dict=None): 
    """Punto de Levantamiento no debe tener registros duplicados"""


def regla_4013(layer_dict=None):
    """Punto Control no debe tener registros duplicados"""

def regla_4014(layer_dict=None): 
    """Lindero no debe tener registros duplicados"""

def regla_4015(layer_dict=None): 
    """Terreno no debe tener registros duplicados"""

def regla_4016(layer_dict=None): 
    """Construcción no debe tener registros duplicados"""

def regla_4017(layer_dict=None): 
    """Unidad de Construcción no debe tener registros duplicados"""

def regla_4018(layer_dict=None):
    """Predio no debe tener registros duplicados"""

def regla_4019(layer_dict=None): # no se va definir por el momento
    """Interesado no debe tener registros duplicados"""

def regla_4020(layer_dict=None): # no se va definir por el momento
    """Derecho no debe tener registros duplicados"""

def regla_4021(layer_dict=None): # no se va definir por el momento
    """Restricción no debe tener registros duplicados"""

def regla_4022(layer_dict=None): # no se va definir por el momento
    """Fuente Administrativa no debe tener registros duplicados"""

categorias_reglas = {
    "Puntos (1000s)": ["1001", "1002", "1003", "1004"],
    "Líneas (2000s)": ["2001", "2002", "2003", "2004", "2005"],
    "Polígonos (3000s)": ["3001", "3002", "3003", "3004", "3005", "3006", "3007", "3008", "3009", "3010", "3011"],
    "Lógica Consistencia (4000s)": ["4001", "4002", "4003", "4004", "4005", "4006", "4007", "4008", "4009", "4010",
                                    "4011", "4012", "4013", "4014", "4015", "4016", "4017", "4018", "4019", "4020",
                                    "4021", "4022"]
}

clases_con_reglas = {
    "Los datos deben corresponder a su modelo (ilivalidator)": sum(categorias_reglas.values(), []),
}

codigos_funciones = {
    "1001": regla_1001,
    "1002": regla_1002,
    "1003": regla_1003,
    "1004": regla_1004,
    "2001": regla_2001,
    "2002": regla_2002,
    "2003": regla_2003,
    "2004": regla_2004,
    "2005": regla_2005,
    "3001": regla_3001,
    "3002": regla_3002,
    "3003": regla_3003,
    "3004": regla_3004,
    "3005": regla_3005,
    "3006": regla_3006,
    "3007": regla_3007,
    "3008": regla_3008,
    "3009": regla_3009,
    "3010": regla_3010,
    "3011": regla_3011,
    "4001": regla_4001,
    "4002": regla_4002,
    "4003": regla_4003,
    "4004": regla_4004,
    "4005": regla_4005,
    "4006": regla_4006,
    "4007": regla_4007,
    "4008": regla_4008,
    "4009": regla_4009,
    "4010": regla_4010,
    "4011": regla_4011,
    "4012": regla_4012,
    "4013": regla_4013,
    "4014": regla_4014,
    "4015": regla_4015,
    "4016": regla_4016,
    "4017": regla_4017,
    "4018": regla_4018,
    "4019": regla_4019,
    "4020": regla_4020,
    "4021": regla_4021,
    "4022": regla_4022,
}

