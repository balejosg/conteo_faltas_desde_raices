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

def extraer_periodo(texto):
    """Extrae el período (fechas) del documento PDF"""
    lineas = texto.split('\n')

    for linea in lineas:
        # Buscar el patrón "Periodo: (DD/MM/YYYY - DD/MM/YYYY)"
        match = re.search(r'Periodo:\s*\((\d{2}/\d{2}/\d{4}\s*-\s*\d{2}/\d{2}/\d{4})\)', linea)
        if match:
            return match.group(1).strip()

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
    """Procesa un PDF y devuelve el nombre de la materia, el período y los datos"""
    print(f"Procesando: {pdf_path.name}")

    # Extraer texto del PDF
    texto = extraer_texto_pdf(pdf_path)
    if not texto:
        return None, None, None

    # Extraer nombre de la materia
    nombre_materia = extraer_nombre_materia(texto)
    if not nombre_materia:
        print(f"  ⚠ No se pudo encontrar el nombre de la materia")
        return None, None, None

    # Extraer período
    periodo = extraer_periodo(texto)
    if not periodo:
        print(f"  ⚠ No se pudo encontrar el período")
        return None, None, None

    # Parsear la tabla
    datos = parsear_tabla(texto)

    if not datos:
        print(f"  ⚠ No se encontraron datos")
        return None, None, None

    print(f"  ✓ Materia: '{nombre_materia}' - Período: '{periodo}' ({len(datos)} alumnos)")
    return nombre_materia, periodo, datos

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

def leer_ods_existente(filename):
    """Lee un archivo ODS existente y extrae su estructura"""
    from xml.etree import ElementTree as ET

    if not Path(filename).exists():
        return None

    try:
        hojas_existentes = {}

        with zipfile.ZipFile(filename, 'r') as zf:
            content_xml = zf.read('content.xml')
            root = ET.fromstring(content_xml)

            # Namespaces
            ns = {
                'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
                'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
                'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
            }

            # Buscar todas las tablas (hojas)
            tables = root.findall('.//table:table', ns)

            for table in tables:
                nombre_hoja = table.get('{%s}name' % ns['table'])
                rows = table.findall('.//table:table-row', ns)

                if not rows:
                    continue

                # Primera fila: cabeceras
                header_row = rows[0]
                cabeceras = []
                for cell in header_row.findall('.//table:table-cell', ns):
                    text_elem = cell.find('.//text:p', ns)
                    if text_elem is not None and text_elem.text:
                        cabeceras.append(text_elem.text)
                    else:
                        cabeceras.append("")

                # Extraer períodos de las cabeceras
                periodos = []
                for cabecera in cabeceras:
                    # Buscar patrón (DD/MM/YYYY - DD/MM/YYYY)
                    match = re.search(r'\((\d{2}/\d{2}/\d{4}\s*-\s*\d{2}/\d{2}/\d{4})\)', cabecera)
                    if match and match.group(1) not in periodos:
                        periodos.append(match.group(1))

                # Resto de filas: datos de alumnos
                alumnos = {}
                for row in rows[1:]:
                    cells = row.findall('.//table:table-cell', ns)
                    if not cells:
                        continue

                    # Primera celda: nombre del alumno
                    nombre_cell = cells[0].find('.//text:p', ns)
                    if nombre_cell is None or not nombre_cell.text:
                        continue

                    nombre_alumno = nombre_cell.text
                    valores = []

                    # Resto de celdas: valores (excluyendo columnas TOTAL)
                    for idx, cell in enumerate(cells[1:], start=1):
                        # Saltar columnas TOTAL
                        if idx < len(cabeceras) and 'TOTAL' in cabeceras[idx]:
                            continue

                        value = cell.get('{%s}value' % ns['office'])
                        if value is not None:
                            valores.append(value)
                        else:
                            text_elem = cell.find('.//text:p', ns)
                            if text_elem is not None and text_elem.text:
                                valores.append(text_elem.text)
                            else:
                                valores.append("")

                    alumnos[nombre_alumno] = valores

                hojas_existentes[nombre_hoja] = {
                    'cabeceras': cabeceras,
                    'periodos': periodos,
                    'alumnos': alumnos
                }

        return hojas_existentes

    except Exception as e:
        print(f"⚠ Error al leer ODS existente: {e}")
        return None

def fusionar_datos_hoja(hoja_existente, periodo_nuevo, datos_nuevos):
    """Fusiona datos nuevos con una hoja existente - AGRUPADO POR TIPO"""

    # Si no existe hoja, crear estructura nueva
    if hoja_existente is None:
        cabeceras = [
            'Alumno/a',
            f'Justificadas ({periodo_nuevo})',
            f'Injustificadas ({periodo_nuevo})',
            f'Retrasos ({periodo_nuevo})',
            'TOTAL Justificadas y Injustificadas',
            'TOTAL Retrasos'
        ]
        alumnos = {}
        for nombre, fj, fi, r in datos_nuevos:
            # Estructura: [just(p1), inj(p1), ret(p1)]
            alumnos[nombre] = [fj, fi, r]

        return {
            'cabeceras': cabeceras,
            'periodos': [periodo_nuevo],
            'alumnos': alumnos
        }

    # Hoja existente: fusionar datos
    cabeceras = list(hoja_existente['cabeceras'])
    periodos = list(hoja_existente['periodos'])
    alumnos = dict(hoja_existente['alumnos'])

    # Verificar si el período ya existe
    periodo_existe = periodo_nuevo in periodos
    num_periodos = len(periodos)

    if periodo_existe:
        # Sobrescribir: encontrar posiciones de este período
        idx_periodo = periodos.index(periodo_nuevo)

        # Posiciones en estructura agrupada por tipo:
        # Just: índices 0 hasta num_periodos-1
        # Inj: índices num_periodos hasta 2*num_periodos-1
        # Ret: índices 2*num_periodos hasta 3*num_periodos-1
        pos_just = idx_periodo
        pos_inj = num_periodos + idx_periodo
        pos_ret = 2 * num_periodos + idx_periodo

        # Actualizar/añadir alumnos
        for nombre, fj, fi, r in datos_nuevos:
            if nombre in alumnos:
                valores = list(alumnos[nombre])
                while len(valores) < 3 * num_periodos:
                    valores.append("")
                valores[pos_just] = fj
                valores[pos_inj] = fi
                valores[pos_ret] = r
                alumnos[nombre] = valores
            else:
                # Alumno nuevo
                valores = [""] * (3 * num_periodos)
                valores[pos_just] = fj
                valores[pos_inj] = fi
                valores[pos_ret] = r
                alumnos[nombre] = valores
    else:
        # Añadir nuevo período
        periodos.append(periodo_nuevo)
        num_periodos_nuevo = len(periodos)

        # Construir nuevas cabeceras agrupadas por tipo
        nuevas_cabeceras = ['Alumno/a']

        # Añadir todas las Justificadas
        for p in periodos:
            nuevas_cabeceras.append(f'Justificadas ({p})')

        # Añadir todas las Injustificadas
        for p in periodos:
            nuevas_cabeceras.append(f'Injustificadas ({p})')

        # Añadir todos los Retrasos
        for p in periodos:
            nuevas_cabeceras.append(f'Retrasos ({p})')

        # Añadir columnas TOTAL
        nuevas_cabeceras.append('TOTAL Justificadas y Injustificadas')
        nuevas_cabeceras.append('TOTAL Retrasos')

        cabeceras = nuevas_cabeceras

        # Reorganizar datos de alumnos a nueva estructura
        nuevos_alumnos = {}
        for nombre, valores_antiguos in alumnos.items():
            # Reorganizar de estructura antigua a nueva
            # Antigua (1 período): [just1, inj1, ret1]
            # Nueva (2 períodos): [just1, just2, inj1, inj2, ret1, ret2]

            # Extraer valores por tipo del formato antiguo
            justs = []
            injs = []
            rets = []

            # Si hay 1 período previo, estructura antigua era [j, i, r]
            if num_periodos_nuevo == 2:
                justs = [valores_antiguos[0] if len(valores_antiguos) > 0 else ""]
                injs = [valores_antiguos[1] if len(valores_antiguos) > 1 else ""]
                rets = [valores_antiguos[2] if len(valores_antiguos) > 2 else ""]
            else:
                # Ya estaba en estructura correcta, extraer valores
                for i in range(num_periodos - 1):
                    justs.append(valores_antiguos[i] if i < len(valores_antiguos) else "")
                for i in range(num_periodos - 1):
                    idx = (num_periodos - 1) + i
                    injs.append(valores_antiguos[idx] if idx < len(valores_antiguos) else "")
                for i in range(num_periodos - 1):
                    idx = 2 * (num_periodos - 1) + i
                    rets.append(valores_antiguos[idx] if idx < len(valores_antiguos) else "")

            # Añadir espacio para nuevo período
            justs.append("")
            injs.append("")
            rets.append("")

            # Construir nueva estructura: todas Just, todas Inj, todos Ret
            valores_nuevos = justs + injs + rets
            nuevos_alumnos[nombre] = valores_nuevos

        alumnos = nuevos_alumnos

        # Añadir datos del nuevo período
        pos_just = num_periodos_nuevo - 1
        pos_inj = num_periodos_nuevo + (num_periodos_nuevo - 1)
        pos_ret = 2 * num_periodos_nuevo + (num_periodos_nuevo - 1)

        for nombre, fj, fi, r in datos_nuevos:
            if nombre in alumnos:
                valores = list(alumnos[nombre])
                valores[pos_just] = fj
                valores[pos_inj] = fi
                valores[pos_ret] = r
                alumnos[nombre] = valores
            else:
                # Alumno nuevo
                valores = [""] * (3 * num_periodos_nuevo)
                valores[pos_just] = fj
                valores[pos_inj] = fi
                valores[pos_ret] = r
                alumnos[nombre] = valores

    return {
        'cabeceras': cabeceras,
        'periodos': periodos,
        'alumnos': alumnos
    }

def crear_ods(hojas_fusionadas, output_filename):
    """Crear un archivo ODS con múltiples hojas (nueva versión con estructura fusionada)"""

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
    for nombre_hoja, hoja_data in hojas_fusionadas.items():
        # Limitar nombre de la hoja a 31 caracteres
        sheet_name = nombre_hoja[:31]

        # Crear la tabla (hoja)
        table = SubElement(spreadsheet, "{%s}table" % table_ns)
        table.set("{%s}name" % table_ns, escape_xml(sheet_name))

        # Obtener estructura de la hoja
        cabeceras = hoja_data['cabeceras']
        alumnos = hoja_data['alumnos']

        # Identificar columnas de Justificadas, Injustificadas y Retrasos para las fórmulas TOTAL
        cols_justificadas = []
        cols_injustificadas = []
        cols_retrasos = []
        for idx, header in enumerate(cabeceras):
            col_letter = chr(65 + idx)  # A=65 en ASCII (columna A es Alumno/a)
            if 'TOTAL' in header:
                # Saltar columnas TOTAL
                continue
            elif 'Justificadas' in header:
                cols_justificadas.append(col_letter)
            elif 'Injustificadas' in header:
                cols_injustificadas.append(col_letter)
            elif 'Retrasos' in header:
                cols_retrasos.append(col_letter)

        # Añadir fila de cabecera
        header_row = SubElement(table, "{%s}table-row" % table_ns)
        for header in cabeceras:
            table_cell = SubElement(header_row, "{%s}table-cell" % table_ns)
            table_cell.set("{%s}value-type" % office_ns, "string")
            p = SubElement(table_cell, "{%s}p" % text_ns)
            p.text = escape_xml(header)

        # Añadir las filas de datos de alumnos
        for row_num, (nombre_alumno, valores) in enumerate(alumnos.items(), start=2):
            table_row = SubElement(table, "{%s}table-row" % table_ns)

            # Primera celda: nombre del alumno
            name_cell = SubElement(table_row, "{%s}table-cell" % table_ns)
            name_cell.set("{%s}value-type" % office_ns, "string")
            p = SubElement(name_cell, "{%s}p" % text_ns)
            p.text = escape_xml(nombre_alumno)

            # Resto de celdas: valores numéricos (excepto TOTAL)
            for cell_value in valores:
                table_cell = SubElement(table_row, "{%s}table-cell" % table_ns)
                if cell_value == "" or cell_value is None:
                    # Celda vacía
                    p = SubElement(table_cell, "{%s}p" % text_ns)
                    p.text = ""
                else:
                    # Valor numérico
                    table_cell.set("{%s}value-type" % office_ns, "float")
                    table_cell.set("{%s}value" % office_ns, str(cell_value))
                    p = SubElement(table_cell, "{%s}p" % text_ns)
                    p.text = str(cell_value)

            # Añadir columna TOTAL Justificadas y Injustificadas
            total_ji_cell = SubElement(table_row, "{%s}table-cell" % table_ns)
            total_ji_cell.set("{%s}value-type" % office_ns, "float")

            # Construir fórmula: suma de todas las Just + todas las Inj
            formula_ji_parts = []
            for col in cols_justificadas + cols_injustificadas:
                formula_ji_parts.append(f"[.{col}{row_num}]")

            formula_ji = f"of:={'+'.join(formula_ji_parts)}" if formula_ji_parts else "of:=0"
            total_ji_cell.set("{%s}formula" % table_ns, formula_ji)

            # No pre-calcular valor, la fórmula lo hará
            p = SubElement(total_ji_cell, "{%s}p" % text_ns)
            p.text = ""

            # Añadir columna TOTAL Retrasos
            total_r_cell = SubElement(table_row, "{%s}table-cell" % table_ns)
            total_r_cell.set("{%s}value-type" % office_ns, "float")

            # Construir fórmula: suma de todos los Retrasos
            formula_r_parts = []
            for col in cols_retrasos:
                formula_r_parts.append(f"[.{col}{row_num}]")

            formula_r = f"of:={'+'.join(formula_r_parts)}" if formula_r_parts else "of:=0"
            total_r_cell.set("{%s}formula" % table_ns, formula_r)

            # No pre-calcular valor, la fórmula lo hará
            p = SubElement(total_r_cell, "{%s}p" % text_ns)
            p.text = ""

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

    # Leer archivo ODS existente si existe
    archivo_ods = directorio_actual / NOMBRE_SALIDA
    hojas_existentes = leer_ods_existente(archivo_ods)

    if hojas_existentes:
        print(f"✓ Archivo existente encontrado: {NOMBRE_SALIDA}")
        print(f"  - {len(hojas_existentes)} hojas existentes")
        print(f"  - Se actualizarán con los nuevos datos\n")
    else:
        print(f"  - No se encontró archivo existente, se creará uno nuevo\n")
        hojas_existentes = {}

    # Procesar cada PDF y fusionar con datos existentes
    hojas_fusionadas = dict(hojas_existentes)
    archivos_procesados = 0

    for pdf_path in pdf_files:
        nombre_materia, periodo, datos = procesar_pdf(pdf_path)
        if nombre_materia and periodo and datos:
            # Buscar hoja existente por nombre
            hoja_existente = hojas_fusionadas.get(nombre_materia, None)

            # Fusionar datos
            hoja_fusionada = fusionar_datos_hoja(hoja_existente, periodo, datos)
            hojas_fusionadas[nombre_materia] = hoja_fusionada

            archivos_procesados += 1
        print()

    if not hojas_fusionadas:
        print("⚠ No se pudo procesar ningún archivo")
        return

    # Crear el archivo ODS
    print("=" * 70)
    print(f"Creando archivo ODS: {NOMBRE_SALIDA}")
    print("=" * 70)
    crear_ods(hojas_fusionadas, NOMBRE_SALIDA)

    print(f"\n✓ Archivo '{NOMBRE_SALIDA}' creado exitosamente!")
    print(f"  - {len(hojas_fusionadas)} hojas en total")
    print(f"  - {archivos_procesados}/{len(pdf_files)} archivos procesados")
    print(f"\nPuedes abrirlo con LibreOffice Calc, Excel u otro programa de hojas de cálculo.")

if __name__ == "__main__":
    main()
