@echo off
echo ====================================================================
echo Instalador para el Generador de ODS desde PDFs de Faltas
echo ====================================================================
echo.
echo Instalando pdfplumber...
echo.

python -m pip install --upgrade pip
python -m pip install pdfplumber

echo.
echo ====================================================================
echo Instalacion completada!
echo ====================================================================
echo.
echo Ahora puedes usar el programa haciendo doble clic en:
echo EJECUTAR_WINDOWS.bat
echo.
pause
