#!/bin/bash

echo "===================================================================="
echo "Generador de Archivo ODS desde PDFs de Faltas"
echo "===================================================================="
echo ""
echo "Buscando archivos PDF en esta carpeta..."
echo ""

python3 generar_faltas_ods.py

echo ""
echo "===================================================================="
echo "Proceso completado!"
echo "===================================================================="
echo ""
echo "Si el proceso fue exitoso, encontrarás el archivo"
echo "\"faltas_consolidado.ods\" en esta carpeta."
echo ""
echo "Puedes abrirlo con Excel, Numbers o LibreOffice Calc."
echo ""
