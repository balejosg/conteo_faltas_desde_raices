@echo off
echo ====================================================================
echo Generador de Archivo ODS desde PDFs de Faltas
echo ====================================================================
echo.
echo Buscando archivos PDF en esta carpeta...
echo.

python generar_faltas_ods.py

echo.
echo ====================================================================
echo Proceso completado!
echo ====================================================================
echo.
echo Si el proceso fue exitoso, encontraras el archivo
echo "faltas_consolidado.ods" en esta carpeta.
echo.
echo Puedes abrirlo con Excel o LibreOffice Calc.
echo.
pause
