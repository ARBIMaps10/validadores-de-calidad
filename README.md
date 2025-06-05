# Validadores de Calidad para QGIS

**Versión 7**

Este plugin permite verificar automáticamente la calidad de los datos geográficos y alfanuméricos en QGIS, validando que cumplan con un conjunto de reglas agrupadas en tres bloques funcionales: **genéricas**, **lógicas** y **obligatorias**. Está diseñado para facilitar la evaluación técnica de cumplimiento respecto a modelos de datos como LADM-COL.

---

## 📌 Características principales

- Validación por bloques temáticos:
  - **Reglas genéricas** (bloques 1000 a 4000)
  - **Reglas lógicas** (bloques 5000 a 6000)
  - **Reglas obligatorias** (bloque 7000)
- Árbol visual de reglas con indicadores de estado por bloque y por regla.
- Ejecución automática de reglas mediante funciones Python.
- Resultados con porcentaje de cumplimiento por bloque.
- Visualización de errores por regla:
  - Código único
  - Descripción
  - Identificador (UUID o campo clave)
- Generación de reportes en PDF.

---

## 🧩 Estructura de Reglas

| Tipo de regla        | Rango de códigos  | 
|----------------------|-------------------|
| Reglas genéricas     | 1000–4000         | 
| Reglas lógicas       | 5000–6000         | 
| Reglas obligatorias  | 7000              |

---

## 📦 Requisitos

- QGIS 3.x
- Python 3.x (entorno de QGIS)
- PyQt5 (incluido en QGIS)

---

## 🚀 Instalación

1. Descarga el archivo `.zip` de este repositorio.
2. Abre QGIS.
3. Ve a **Complementos → Administrar e instalar complementos**.
4. Haz clic en **Instalar desde ZIP**.
5. Selecciona `Validadores_de_calidad.version 7.zip`.
6. Instala el plugin y accede a él desde la barra de herramientas como **Validadores de Calidad**.

---

## ⚙️ Cómo usarlo

1. Carga en QGIS las capas correspondientes a tu modelo.
2. Ejecuta el plugin desde el icono o menú.
3. Selecciona el bloque que deseas validar (genéricas, lógicas u obligatorias).
4. Haz clic en **"Validar bloque"**.
5. Consulta el resultado visual:
   - Verde: cumplimiento del 100%
   - Rojo: errores detectados
6. Abre la ventana de errores para más detalles.
7. Exporta un reporte en PDF si lo necesitas.

---

## 📁 Estructura del plugin


