# plugin_loader.py
from qgis.utils import plugins, reloadPlugin, startPlugin, iface
import traceback

PLUGIN_NAME = 'Validadores_de_calidad'

def load_or_reload_plugin():
    try:
        if PLUGIN_NAME in plugins:
            reloadPlugin(PLUGIN_NAME)
            iface.messageBar().pushSuccess("Plugin Recargado", f"✅ '{PLUGIN_NAME}' se recargó exitosamente.")
            print(f"✅ Plugin '{PLUGIN_NAME}' recargado exitosamente.")
        else:
            startPlugin(PLUGIN_NAME)
            iface.messageBar().pushSuccess("Plugin Cargado", f"✅ '{PLUGIN_NAME}' se cargó exitosamente.")
            print(f"✅ Plugin '{PLUGIN_NAME}' cargado exitosamente.")
    except Exception as e:
        iface.messageBar().pushCritical("Error al cargar plugin", str(e))
        print("❌ Error al cargar o recargar el plugin:")
        print(traceback.format_exc())

load_or_reload_plugin()
