#!/usr/bin/env python3
"""
Script para convertir PDFs de faltas a un archivo ODS con múltiples hojas.
Procesa todos los PDFs en el directorio actual y genera un archivo ODS.
"""
import re
import zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import pdfplumber

# Configuración
NOMBRE_SALIDA = "faltas_consolidado.ods"

def extraer_texto_pdf(pdf_path):
    """Extrae el texto de un PDF usando pdfplumber"""
    try:
        texto_completo = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                texto = page.extract_text()
                if texto:
                    texto_completo.append(texto)
        return '\n'.join(texto_completo)
    except Exception as e:
        print(f"  ⚠ Error al extraer texto: {e}")
        return None

def extraer_nombre_materia(texto):
    """Extrae el nombre de la materia de la cabecera de la tabla"""
    lineas = texto.split('\n')

    for linea in lineas:
        # Buscar la línea que contiene "Alumno/a" y "TOTAL"
        if 'Alumno/a' in linea and 'TOTAL' in linea:
            # Extraer el texto entre "Alumno/a" y "TOTAL"
            match = re.search(r'Alumno/a\s+(.+?)\s+TOTAL', linea)
            if match:
                nombre_materia = match.group(1).strip()
                # Limpiar espacios múltiples
                nombre_materia = re.sub(r'\s+', ' ', nombre_materia)
                return nombre_materia

    return None

def parsear_tabla(texto):
    """Parsea el texto extraído para obtener los datos de la tabla"""
    lineas = texto.split('\n')
    datos = []

    for linea in lineas:
        # Saltar líneas vacías o de totales
        if not linea.strip() or 'TOTALES' in linea:
            continue

        # Buscar líneas que contengan nombres de alumnos
        # El patrón es: Nombre (puede contener comas y espacios) + números separados por espacios
        match = re.search(r'^(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$', linea.strip())

        if match:
            nombre = match.group(1).strip()
            fj = match.group(2)
            fi = match.group(3)
            r = match.group(4)

            # Filtrar nombres que parecen ser encabezados o texto no relevante
            if nombre and not any(palabra in nombre.lower() for palabra in
                ['alumno', 'año académico', 'curso', 'profesor', 'fecha', 'cód.centro', 'ref.doc']):
                datos.append([nombre, fj, fi, r])

    return datos

def procesar_pdf(pdf_path):
    """Procesa un PDF y devuelve el nombre de la materia y los datos"""
    print(f"Procesando: {pdf_path.name}")

    # Extraer texto del PDF
    texto = extraer_texto_pdf(pdf_path)
    if not texto:
        return None, None

    # Extraer nombre de la materia
    nombre_materia = extraer_nombre_materia(texto)
    if not nombre_materia:
        print(f"  ⚠ No se pudo encontrar el nombre de la materia")
        return None, None

    # Parsear la tabla
    datos = parsear_tabla(texto)

    if not datos:
        print(f"  ⚠ No se encontraron datos")
        return None, None

    print(f"  ✓ Materia: '{nombre_materia}' ({len(datos)} alumnos)")
    return nombre_materia, datos

def escape_xml(text):
    """Escapar caracteres especiales XML"""
    if text is None:
        return ""
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text

def crear_ods(hojas_datos, output_filename):
    """Crear un archivo ODS con múltiples hojas"""

    # Crear el contenido XML del archivo content.xml
    office_ns = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    table_ns = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    text_ns = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"

    # Raíz del documento
    root = Element("{%s}document-content" % office_ns)
    root.set("{%s}version" % office_ns, "1.2")
    root.set("xmlns:office", office_ns)
    root.set("xmlns:table", table_ns)
    root.set("xmlns:text", text_ns)

    # Cuerpo del documento
    body = SubElement(root, "{%s}body" % office_ns)
    spreadsheet = SubElement(body, "{%s}spreadsheet" % office_ns)

    # Procesar cada hoja
    for nombre_hoja, datos in hojas_datos:
        # Limitar nombre de la hoja a 31 caracteres
        sheet_name = nombre_hoja[:31]

        # Crear la tabla (hoja)
        table = SubElement(spreadsheet, "{%s}table" % table_ns)
        table.set("{%s}name" % table_ns, escape_xml(sheet_name))

        # Añadir fila de cabecera
        header_row = SubElement(table, "{%s}table-row" % table_ns)
        for header in ['Alumno/a', 'FJ', 'FI', 'R']:
            table_cell = SubElement(header_row, "{%s}table-cell" % table_ns)
            table_cell.set("{%s}value-type" % office_ns, "string")
            p = SubElement(table_cell, "{%s}p" % text_ns)
            p.text = escape_xml(header)

        # Añadir las filas de datos
        for row in datos:
            table_row = SubElement(table, "{%s}table-row" % table_ns)
            for idx, cell_value in enumerate(row):
                table_cell = SubElement(table_row, "{%s}table-cell" % table_ns)

                # Primera columna (nombre) es texto, el resto son números
                if idx == 0:
                    table_cell.set("{%s}value-type" % office_ns, "string")
                    p = SubElement(table_cell, "{%s}p" % text_ns)
                    p.text = escape_xml(cell_value)
                else:
                    # Columnas numéricas (FJ, FI, R)
                    table_cell.set("{%s}value-type" % office_ns, "float")
                    table_cell.set("{%s}value" % office_ns, str(cell_value))
                    p = SubElement(table_cell, "{%s}p" % text_ns)
                    p.text = str(cell_value)

    # Convertir a string XML
    xml_str = tostring(root, encoding='utf-8')

    # Formatear el XML
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(encoding='utf-8')

    # Crear el archivo ODS (es un archivo ZIP)
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype (sin comprimir)
        zf.writestr('mimetype', 'application/vnd.oasis.opendocument.spreadsheet',
                   compress_type=zipfile.ZIP_STORED)

        # META-INF/manifest.xml
        manifest = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.spreadsheet" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
</manifest:manifest>'''
        zf.writestr('META-INF/manifest.xml', manifest)

        # content.xml
        zf.writestr('content.xml', pretty_xml)

def main():
    """Función principal"""
    print("=" * 70)
    print("Generador de archivo ODS desde PDFs de faltas")
    print("=" * 70)
    print()

    # Obtener directorio actual
    directorio_actual = Path.cwd()

    # Obtener todos los PDFs del directorio actual
    pdf_files = sorted(directorio_actual.glob("*.pdf"))

    # Filtrar PDFs que no queremos procesar
    pdf_files = [pdf for pdf in pdf_files]

    if not pdf_files:
        print("⚠ No se encontraron archivos PDF para procesar en el directorio actual")
        return

    print(f"Encontrados {len(pdf_files)} archivos PDF\n")

    # Procesar cada PDF
    hojas_datos = []
    archivos_procesados = 0

    for pdf_path in pdf_files:
        nombre_materia, datos = procesar_pdf(pdf_path)
        if nombre_materia and datos:
            hojas_datos.append((nombre_materia, datos))
            archivos_procesados += 1
        print()

    if not hojas_datos:
        print("⚠ No se pudo procesar ningún archivo")
        return

    # Crear el archivo ODS
    print("=" * 70)
    print(f"Creando archivo ODS: {NOMBRE_SALIDA}")
    print("=" * 70)
    crear_ods(hojas_datos, NOMBRE_SALIDA)

    print(f"\n✓ Archivo '{NOMBRE_SALIDA}' creado exitosamente!")
    print(f"  - {len(hojas_datos)} hojas generadas")
    print(f"  - {archivos_procesados}/{len(pdf_files)} archivos procesados")
    print(f"\nPuedes abrirlo con LibreOffice Calc, Excel u otro programa de hojas de cálculo.")

if __name__ == "__main__":
    main()
